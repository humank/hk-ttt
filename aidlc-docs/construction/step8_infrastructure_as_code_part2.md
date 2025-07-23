# Step 8: Implement Infrastructure as Code (Part 2)

## Network Stack Implementation

### VPC Construct

Create the VPC construct in `lib/constructs/vpc-construct.ts`:

```typescript
import * as cdk from '@aws-cdk/core';
import * as ec2 from '@aws-cdk/aws-ec2';

export interface VpcConstructProps {
  cidr: string;
  maxAzs: number;
  natGateways: number;
}

export class VpcConstruct extends cdk.Construct {
  public readonly vpc: ec2.Vpc;
  public readonly publicSubnets: ec2.ISubnet[];
  public readonly privateAppSubnets: ec2.ISubnet[];
  public readonly privateDataSubnets: ec2.ISubnet[];

  constructor(scope: cdk.Construct, id: string, props: VpcConstructProps) {
    super(scope, id);

    // Create VPC with 3 subnet groups
    this.vpc = new ec2.Vpc(this, 'OpportunityVpc', {
      cidr: props.cidr,
      maxAzs: props.maxAzs,
      natGateways: props.natGateways,
      subnetConfiguration: [
        {
          name: 'Public',
          subnetType: ec2.SubnetType.PUBLIC,
          cidrMask: 24,
        },
        {
          name: 'PrivateApp',
          subnetType: ec2.SubnetType.PRIVATE_WITH_NAT,
          cidrMask: 24,
        },
        {
          name: 'PrivateData',
          subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
          cidrMask: 24,
        },
      ],
    });

    // Store subnet references
    this.publicSubnets = this.vpc.publicSubnets;
    this.privateAppSubnets = this.vpc.privateSubnets;
    this.privateDataSubnets = this.vpc.isolatedSubnets;

    // Create VPC endpoints for AWS services
    this.createVpcEndpoints();

    // Output VPC ID
    new cdk.CfnOutput(this, 'VpcId', {
      value: this.vpc.vpcId,
      description: 'VPC ID',
      exportName: `${id}-vpc-id`,
    });
  }

  private createVpcEndpoints() {
    // S3 Gateway Endpoint
    this.vpc.addGatewayEndpoint('S3Endpoint', {
      service: ec2.GatewayVpcEndpointAwsService.S3,
    });

    // DynamoDB Gateway Endpoint
    this.vpc.addGatewayEndpoint('DynamoDbEndpoint', {
      service: ec2.GatewayVpcEndpointAwsService.DYNAMODB,
    });

    // Interface Endpoints
    const securityGroup = new ec2.SecurityGroup(this, 'VpcEndpointSG', {
      vpc: this.vpc,
      description: 'Security group for VPC endpoints',
      allowAllOutbound: true,
    });

    securityGroup.addIngressRule(
      ec2.Peer.ipv4(this.vpc.vpcCidrBlock),
      ec2.Port.tcp(443),
      'Allow HTTPS from within VPC'
    );

    // ECR Endpoints
    this.vpc.addInterfaceEndpoint('EcrDockerEndpoint', {
      service: ec2.InterfaceVpcEndpointAwsService.ECR_DOCKER,
      subnets: { subnetType: ec2.SubnetType.PRIVATE_WITH_NAT },
      securityGroups: [securityGroup],
    });

    this.vpc.addInterfaceEndpoint('EcrApiEndpoint', {
      service: ec2.InterfaceVpcEndpointAwsService.ECR,
      subnets: { subnetType: ec2.SubnetType.PRIVATE_WITH_NAT },
      securityGroups: [securityGroup],
    });

    // CloudWatch Logs Endpoint
    this.vpc.addInterfaceEndpoint('CloudWatchLogsEndpoint', {
      service: ec2.InterfaceVpcEndpointAwsService.CLOUDWATCH_LOGS,
      subnets: { subnetType: ec2.SubnetType.PRIVATE_WITH_NAT },
      securityGroups: [securityGroup],
    });

    // Secrets Manager Endpoint
    this.vpc.addInterfaceEndpoint('SecretsManagerEndpoint', {
      service: ec2.InterfaceVpcEndpointAwsService.SECRETS_MANAGER,
      subnets: { subnetType: ec2.SubnetType.PRIVATE_WITH_NAT },
      securityGroups: [securityGroup],
    });
  }
}
```

### Network Stack

Create the network stack in `lib/stacks/network-stack.ts`:

```typescript
import * as cdk from '@aws-cdk/core';
import * as ec2 from '@aws-cdk/aws-ec2';
import { VpcConstruct } from '../constructs/vpc-construct';

export interface NetworkStackProps extends cdk.StackProps {
  envConfig: any;
}

export class NetworkStack extends cdk.Stack {
  public readonly vpc: ec2.Vpc;

  constructor(scope: cdk.Construct, id: string, props: NetworkStackProps) {
    super(scope, id, props);

    // Create VPC
    const vpcConstruct = new VpcConstruct(this, 'VpcConstruct', {
      cidr: props.envConfig.vpcCidr,
      maxAzs: props.envConfig.availabilityZones.length,
      natGateways: props.envConfig.availabilityZones.length, // One NAT Gateway per AZ
    });

    this.vpc = vpcConstruct.vpc;

    // Create flow logs
    this.vpc.addFlowLog('FlowLogs', {
      destination: ec2.FlowLogDestination.toCloudWatchLogs(),
      trafficType: ec2.FlowLogTrafficType.ALL,
    });

    // Output subnet IDs
    props.envConfig.availabilityZones.forEach((az: string, index: number) => {
      new cdk.CfnOutput(this, `PublicSubnet${index + 1}Id`, {
        value: vpcConstruct.publicSubnets[index].subnetId,
        description: `Public Subnet ${index + 1} ID (${az})`,
      });

      new cdk.CfnOutput(this, `PrivateAppSubnet${index + 1}Id`, {
        value: vpcConstruct.privateAppSubnets[index].subnetId,
        description: `Private App Subnet ${index + 1} ID (${az})`,
      });

      new cdk.CfnOutput(this, `PrivateDataSubnet${index + 1}Id`, {
        value: vpcConstruct.privateDataSubnets[index].subnetId,
        description: `Private Data Subnet ${index + 1} ID (${az})`,
      });
    });
  }
}
```

## Data Stack Implementation

### Database Construct

Create the database construct in `lib/constructs/database-construct.ts`:

```typescript
import * as cdk from '@aws-cdk/core';
import * as ec2 from '@aws-cdk/aws-ec2';
import * as rds from '@aws-cdk/aws-rds';
import * as secretsmanager from '@aws-cdk/aws-secretsmanager';

export interface DatabaseConstructProps {
  vpc: ec2.Vpc;
  instanceType: ec2.InstanceType;
  allocatedStorage: number;
  maxAllocatedStorage: number;
  backupRetention: cdk.Duration;
  deletionProtection: boolean;
  multiAz: boolean;
}

export class DatabaseConstruct extends cdk.Construct {
  public readonly instance: rds.DatabaseInstance;
  public readonly securityGroup: ec2.SecurityGroup;
  public readonly secret: secretsmanager.Secret;

  constructor(scope: cdk.Construct, id: string, props: DatabaseConstructProps) {
    super(scope, id);

    // Create security group for database
    this.securityGroup = new ec2.SecurityGroup(this, 'DatabaseSG', {
      vpc: props.vpc,
      description: 'Security group for Opportunity Management Service database',
      allowAllOutbound: true,
    });

    // Create database credentials secret
    this.secret = new secretsmanager.Secret(this, 'DatabaseSecret', {
      description: 'Opportunity Management Service database credentials',
      generateSecretString: {
        secretStringTemplate: JSON.stringify({ username: 'admin' }),
        generateStringKey: 'password',
        excludePunctuation: true,
        includeSpace: false,
        passwordLength: 16,
      },
    });

    // Create parameter group
    const parameterGroup = new rds.ParameterGroup(this, 'ParameterGroup', {
      engine: rds.DatabaseInstanceEngine.postgres({
        version: rds.PostgresEngineVersion.VER_13,
      }),
      parameters: {
        'max_connections': '200',
        'shared_buffers': '256MB',
        'effective_cache_size': '768MB',
        'work_mem': '4MB',
        'maintenance_work_mem': '64MB',
        'min_wal_size': '1GB',
        'max_wal_size': '4GB',
        'checkpoint_completion_target': '0.9',
        'wal_buffers': '16MB',
        'default_statistics_target': '100',
      },
    });

    // Create database instance
    this.instance = new rds.DatabaseInstance(this, 'Database', {
      engine: rds.DatabaseInstanceEngine.postgres({
        version: rds.PostgresEngineVersion.VER_13,
      }),
      instanceType: props.instanceType,
      vpc: props.vpc,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
      },
      securityGroups: [this.securityGroup],
      allocatedStorage: props.allocatedStorage,
      maxAllocatedStorage: props.maxAllocatedStorage,
      storageType: rds.StorageType.GP2,
      backupRetention: props.backupRetention,
      deletionProtection: props.deletionProtection,
      multiAz: props.multiAz,
      autoMinorVersionUpgrade: true,
      parameterGroup: parameterGroup,
      credentials: rds.Credentials.fromSecret(this.secret),
      databaseName: 'opportunity',
      storageEncrypted: true,
      monitoringInterval: cdk.Duration.minutes(1),
      enablePerformanceInsights: true,
      performanceInsightRetention: rds.PerformanceInsightRetention.DEFAULT,
    });

    // Output database endpoint
    new cdk.CfnOutput(this, 'DatabaseEndpoint', {
      value: this.instance.dbInstanceEndpointAddress,
      description: 'Database endpoint',
      exportName: `${id}-database-endpoint`,
    });

    // Output database secret ARN
    new cdk.CfnOutput(this, 'DatabaseSecretArn', {
      value: this.secret.secretArn,
      description: 'Database secret ARN',
      exportName: `${id}-database-secret-arn`,
    });
  }
}
```

### Cache Construct

Create the cache construct in `lib/constructs/cache-construct.ts`:

```typescript
import * as cdk from '@aws-cdk/core';
import * as ec2 from '@aws-cdk/aws-ec2';
import * as elasticache from '@aws-cdk/aws-elasticache';

export interface CacheConstructProps {
  vpc: ec2.Vpc;
  nodeType: string;
  numShards: number;
  replicas: number;
}

export class CacheConstruct extends cdk.Construct {
  public readonly replicationGroup: elasticache.CfnReplicationGroup;
  public readonly securityGroup: ec2.SecurityGroup;

  constructor(scope: cdk.Construct, id: string, props: CacheConstructProps) {
    super(scope, id);

    // Create security group for Redis
    this.securityGroup = new ec2.SecurityGroup(this, 'RedisSG', {
      vpc: props.vpc,
      description: 'Security group for Opportunity Management Service Redis',
      allowAllOutbound: true,
    });

    // Create subnet group
    const subnetGroup = new elasticache.CfnSubnetGroup(this, 'RedisSubnetGroup', {
      description: 'Subnet group for Opportunity Management Service Redis',
      subnetIds: props.vpc.isolatedSubnets.map(subnet => subnet.subnetId),
    });

    // Create parameter group
    const parameterGroup = new elasticache.CfnParameterGroup(this, 'RedisParameterGroup', {
      cacheParameterGroupFamily: 'redis6.x',
      description: 'Parameter group for Opportunity Management Service Redis',
      properties: {
        'maxmemory-policy': 'volatile-lru',
        'notify-keyspace-events': 'Kgx',
      },
    });

    // Create Redis replication group
    this.replicationGroup = new elasticache.CfnReplicationGroup(this, 'Redis', {
      replicationGroupDescription: 'Opportunity Management Service Redis',
      cacheNodeType: props.nodeType,
      engine: 'redis',
      engineVersion: '6.x',
      numNodeGroups: props.numShards,
      replicasPerNodeGroup: props.replicas,
      automaticFailoverEnabled: true,
      multiAzEnabled: true,
      cacheParameterGroupName: parameterGroup.ref,
      cacheSubnetGroupName: subnetGroup.ref,
      securityGroupIds: [this.securityGroup.securityGroupId],
      atRestEncryptionEnabled: true,
      transitEncryptionEnabled: true,
      port: 6379,
    });

    // Output Redis endpoint
    new cdk.CfnOutput(this, 'RedisEndpoint', {
      value: this.replicationGroup.attrConfigurationEndPointAddress,
      description: 'Redis configuration endpoint',
      exportName: `${id}-redis-endpoint`,
    });
  }
}
```

### Data Stack

Create the data stack in `lib/stacks/data-stack.ts`:

```typescript
import * as cdk from '@aws-cdk/core';
import * as ec2 from '@aws-cdk/aws-ec2';
import * as rds from '@aws-cdk/aws-rds';
import { DatabaseConstruct } from '../constructs/database-construct';
import { CacheConstruct } from '../constructs/cache-construct';

export interface DataStackProps extends cdk.StackProps {
  envConfig: any;
  vpc: ec2.Vpc;
}

export class DataStack extends cdk.Stack {
  public readonly database: rds.DatabaseInstance;
  public readonly redis: elasticache.CfnReplicationGroup;

  constructor(scope: cdk.Construct, id: string, props: DataStackProps) {
    super(scope, id, props);

    // Create database
    const databaseConstruct = new DatabaseConstruct(this, 'DatabaseConstruct', {
      vpc: props.vpc,
      instanceType: ec2.InstanceType.of(
        ec2.InstanceClass.BURSTABLE3,
        ec2.InstanceSize.LARGE
      ),
      allocatedStorage: 100,
      maxAllocatedStorage: 500,
      backupRetention: cdk.Duration.days(7),
      deletionProtection: props.envConfig.env === 'prod',
      multiAz: true,
    });

    this.database = databaseConstruct.instance;

    // Create Redis cache
    const cacheConstruct = new CacheConstruct(this, 'CacheConstruct', {
      vpc: props.vpc,
      nodeType: props.envConfig.cacheNodeType,
      numShards: 2,
      replicas: 1,
    });

    this.redis = cacheConstruct.replicationGroup;

    // Allow ECS security group to access database and Redis
    // (We'll create this security group in the compute stack and update it later)
  }
}
```
