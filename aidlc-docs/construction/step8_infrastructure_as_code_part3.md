# Step 8: Implement Infrastructure as Code (Part 3)

## Compute Stack Implementation

### ECS Construct

Create the ECS construct in `lib/constructs/ecs-construct.ts`:

```typescript
import * as cdk from '@aws-cdk/core';
import * as ec2 from '@aws-cdk/aws-ec2';
import * as ecs from '@aws-cdk/aws-ecs';
import * as ecr from '@aws-cdk/aws-ecr';
import * as elbv2 from '@aws-cdk/aws-elasticloadbalancingv2';
import * as logs from '@aws-cdk/aws-logs';
import * as iam from '@aws-cdk/aws-iam';
import * as secretsmanager from '@aws-cdk/aws-secretsmanager';
import * as s3 from '@aws-cdk/aws-s3';
import * as rds from '@aws-cdk/aws-rds';
import * as elasticache from '@aws-cdk/aws-elasticache';
import * as cognito from '@aws-cdk/aws-cognito';

export interface EcsConstructProps {
  vpc: ec2.Vpc;
  database: rds.DatabaseInstance;
  databaseSecret: secretsmanager.Secret;
  redis: elasticache.CfnReplicationGroup;
  attachmentsBucket: s3.Bucket;
  userPool: cognito.UserPool;
  cpu: number;
  memory: number;
  minCapacity: number;
  maxCapacity: number;
  containerImage?: string;
}

export class EcsConstruct extends cdk.Construct {
  public readonly cluster: ecs.Cluster;
  public readonly service: ecs.FargateService;
  public readonly loadBalancer: elbv2.ApplicationLoadBalancer;
  public readonly securityGroup: ec2.SecurityGroup;

  constructor(scope: cdk.Construct, id: string, props: EcsConstructProps) {
    super(scope, id);

    // Create ECS cluster
    this.cluster = new ecs.Cluster(this, 'Cluster', {
      vpc: props.vpc,
      containerInsights: true,
    });

    // Create security group for ECS service
    this.securityGroup = new ec2.SecurityGroup(this, 'ServiceSG', {
      vpc: props.vpc,
      description: 'Security group for Opportunity Management Service ECS service',
      allowAllOutbound: true,
    });

    // Create load balancer
    this.loadBalancer = new elbv2.ApplicationLoadBalancer(this, 'ALB', {
      vpc: props.vpc,
      internetFacing: true,
      securityGroup: new ec2.SecurityGroup(this, 'ALBSG', {
        vpc: props.vpc,
        description: 'Security group for Opportunity Management Service ALB',
        allowAllOutbound: true,
      }),
    });

    // Allow HTTP traffic to ALB
    this.loadBalancer.securityGroup.addIngressRule(
      ec2.Peer.anyIpv4(),
      ec2.Port.tcp(80),
      'Allow HTTP traffic'
    );

    // Allow HTTPS traffic to ALB
    this.loadBalancer.securityGroup.addIngressRule(
      ec2.Peer.anyIpv4(),
      ec2.Port.tcp(443),
      'Allow HTTPS traffic'
    );

    // Allow traffic from ALB to ECS service
    this.securityGroup.addIngressRule(
      this.loadBalancer.securityGroup,
      ec2.Port.tcp(8000),
      'Allow traffic from ALB'
    );

    // Allow traffic from ECS service to database
    props.database.connections.allowFrom(
      this.securityGroup,
      ec2.Port.tcp(5432),
      'Allow traffic from ECS service to database'
    );

    // Allow traffic from ECS service to Redis
    props.redis.securityGroupIds.forEach(sgId => {
      const redisSg = ec2.SecurityGroup.fromSecurityGroupId(
        this,
        `ImportedRedisSG-${sgId}`,
        sgId
      );
      redisSg.addIngressRule(
        this.securityGroup,
        ec2.Port.tcp(6379),
        'Allow traffic from ECS service to Redis'
      );
    });

    // Create task execution role
    const executionRole = new iam.Role(this, 'TaskExecutionRole', {
      assumedBy: new iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
      managedPolicies: [
        iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AmazonECSTaskExecutionRolePolicy'),
      ],
    });

    // Create task role
    const taskRole = new iam.Role(this, 'TaskRole', {
      assumedBy: new iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
    });

    // Grant task role access to database secret
    props.databaseSecret.grantRead(taskRole);

    // Grant task role access to S3 bucket
    props.attachmentsBucket.grantReadWrite(taskRole);

    // Create log group
    const logGroup = new logs.LogGroup(this, 'ServiceLogs', {
      retention: logs.RetentionDays.ONE_MONTH,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    // Create task definition
    const taskDefinition = new ecs.FargateTaskDefinition(this, 'TaskDef', {
      cpu: props.cpu,
      memoryLimitMiB: props.memory,
      executionRole: executionRole,
      taskRole: taskRole,
    });

    // Create container image
    let containerImage: ecs.ContainerImage;
    if (props.containerImage) {
      containerImage = ecs.ContainerImage.fromRegistry(props.containerImage);
    } else {
      // Create ECR repository
      const repository = new ecr.Repository(this, 'Repository', {
        repositoryName: 'opportunity-management-service',
        removalPolicy: cdk.RemovalPolicy.RETAIN,
        lifecycleRules: [
          {
            maxImageCount: 10,
            description: 'Keep only the last 10 images',
          },
        ],
      });
      containerImage = ecs.ContainerImage.fromEcrRepository(repository, 'latest');
    }

    // Add container to task definition
    const container = taskDefinition.addContainer('AppContainer', {
      image: containerImage,
      logging: ecs.LogDrivers.awsLogs({
        streamPrefix: 'opportunity-service',
        logGroup: logGroup,
      }),
      environment: {
        NODE_ENV: 'production',
        PORT: '8000',
        REDIS_HOST: props.redis.attrConfigurationEndPointAddress,
        REDIS_PORT: '6379',
        S3_BUCKET: props.attachmentsBucket.bucketName,
        COGNITO_USER_POOL_ID: props.userPool.userPoolId,
        COGNITO_CLIENT_ID: props.userPool.userPoolClientId,
      },
      secrets: {
        DB_CONNECTION_STRING: ecs.Secret.fromSecretsManager(props.databaseSecret, 'connection_string'),
      },
      healthCheck: {
        command: ['CMD-SHELL', 'curl -f http://localhost:8000/health || exit 1'],
        interval: cdk.Duration.seconds(30),
        timeout: cdk.Duration.seconds(5),
        retries: 3,
        startPeriod: cdk.Duration.seconds(60),
      },
    });

    // Add port mapping
    container.addPortMappings({
      containerPort: 8000,
      protocol: ecs.Protocol.TCP,
    });

    // Add X-Ray sidecar container
    taskDefinition.addContainer('XRayDaemon', {
      image: ecs.ContainerImage.fromRegistry('amazon/aws-xray-daemon'),
      cpu: 32,
      memoryLimitMiB: 256,
      logging: ecs.LogDrivers.awsLogs({
        streamPrefix: 'xray-daemon',
        logGroup: logGroup,
      }),
      portMappings: [
        {
          containerPort: 2000,
          protocol: ecs.Protocol.UDP,
        },
      ],
    });

    // Create ECS service
    this.service = new ecs.FargateService(this, 'Service', {
      cluster: this.cluster,
      taskDefinition: taskDefinition,
      desiredCount: props.minCapacity,
      securityGroups: [this.securityGroup],
      assignPublicIp: false,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE_WITH_NAT,
      },
      healthCheckGracePeriod: cdk.Duration.seconds(60),
      minHealthyPercent: 50,
      maxHealthyPercent: 200,
      deploymentController: {
        type: ecs.DeploymentControllerType.ECS,
      },
      circuitBreaker: {
        rollback: true,
      },
    });

    // Create target group
    const targetGroup = new elbv2.ApplicationTargetGroup(this, 'TargetGroup', {
      vpc: props.vpc,
      port: 8000,
      protocol: elbv2.ApplicationProtocol.HTTP,
      targetType: elbv2.TargetType.IP,
      healthCheck: {
        path: '/health',
        interval: cdk.Duration.seconds(30),
        timeout: cdk.Duration.seconds(5),
        healthyThresholdCount: 2,
        unhealthyThresholdCount: 3,
        healthyHttpCodes: '200',
      },
    });

    // Add target group to service
    this.service.attachToApplicationTargetGroup(targetGroup);

    // Create HTTP listener
    const httpListener = this.loadBalancer.addListener('HttpListener', {
      port: 80,
      open: true,
      defaultAction: elbv2.ListenerAction.redirect({
        protocol: 'HTTPS',
        port: '443',
        permanent: true,
      }),
    });

    // Create HTTPS listener
    const httpsListener = this.loadBalancer.addListener('HttpsListener', {
      port: 443,
      certificates: [/* Certificate will be added in API stack */],
      defaultAction: elbv2.ListenerAction.forward([targetGroup]),
    });

    // Set up auto-scaling
    const scaling = this.service.autoScaleTaskCount({
      minCapacity: props.minCapacity,
      maxCapacity: props.maxCapacity,
    });

    // Scale based on CPU utilization
    scaling.scaleOnCpuUtilization('CpuScaling', {
      targetUtilizationPercent: 70,
      scaleInCooldown: cdk.Duration.seconds(300),
      scaleOutCooldown: cdk.Duration.seconds(60),
    });

    // Scale based on request count
    scaling.scaleOnRequestCount('RequestScaling', {
      requestsPerTarget: 1000,
      targetGroup: targetGroup,
      scaleInCooldown: cdk.Duration.seconds(300),
      scaleOutCooldown: cdk.Duration.seconds(60),
    });

    // Output load balancer DNS
    new cdk.CfnOutput(this, 'LoadBalancerDNS', {
      value: this.loadBalancer.loadBalancerDnsName,
      description: 'Load balancer DNS name',
      exportName: `${id}-lb-dns`,
    });

    // Output service name
    new cdk.CfnOutput(this, 'ServiceName', {
      value: this.service.serviceName,
      description: 'ECS service name',
      exportName: `${id}-service-name`,
    });
  }
}
```

### Compute Stack

Create the compute stack in `lib/stacks/compute-stack.ts`:

```typescript
import * as cdk from '@aws-cdk/core';
import * as ec2 from '@aws-cdk/aws-ec2';
import * as ecs from '@aws-cdk/aws-ecs';
import * as rds from '@aws-cdk/aws-rds';
import * as elasticache from '@aws-cdk/aws-elasticache';
import * as s3 from '@aws-cdk/aws-s3';
import * as cognito from '@aws-cdk/aws-cognito';
import { EcsConstruct } from '../constructs/ecs-construct';

export interface ComputeStackProps extends cdk.StackProps {
  envConfig: any;
  vpc: ec2.Vpc;
  database: rds.DatabaseInstance;
  redis: elasticache.CfnReplicationGroup;
  attachmentsBucket: s3.Bucket;
  userPool: cognito.UserPool;
}

export class ComputeStack extends cdk.Stack {
  public readonly ecsService: ecs.FargateService;

  constructor(scope: cdk.Construct, id: string, props: ComputeStackProps) {
    super(scope, id, props);

    // Create ECS service
    const ecsConstruct = new EcsConstruct(this, 'EcsConstruct', {
      vpc: props.vpc,
      database: props.database,
      databaseSecret: props.database.secret!,
      redis: props.redis,
      attachmentsBucket: props.attachmentsBucket,
      userPool: props.userPool,
      cpu: props.envConfig.ecsTaskCpu,
      memory: props.envConfig.ecsTaskMemory,
      minCapacity: props.envConfig.ecsMinCapacity,
      maxCapacity: props.envConfig.ecsMaxCapacity,
    });

    this.ecsService = ecsConstruct.service;
  }
}
```

## API Stack Implementation

### API Gateway Construct

Create the API Gateway construct in `lib/constructs/api-gateway-construct.ts`:

```typescript
import * as cdk from '@aws-cdk/core';
import * as ec2 from '@aws-cdk/aws-ec2';
import * as elbv2 from '@aws-cdk/aws-elasticloadbalancingv2';
import * as apigateway from '@aws-cdk/aws-apigateway';
import * as acm from '@aws-cdk/aws-certificatemanager';
import * as route53 from '@aws-cdk/aws-route53';
import * as targets from '@aws-cdk/aws-route53-targets';
import * as cognito from '@aws-cdk/aws-cognito';

export interface ApiGatewayConstructProps {
  vpc: ec2.Vpc;
  loadBalancer: elbv2.ApplicationLoadBalancer;
  userPool: cognito.UserPool;
  domainName: string;
  hostedZoneId?: string;
  hostedZoneName?: string;
}

export class ApiGatewayConstruct extends cdk.Construct {
  public readonly api: apigateway.RestApi;
  public readonly certificate: acm.Certificate;

  constructor(scope: cdk.Construct, id: string, props: ApiGatewayConstructProps) {
    super(scope, id);

    // Create certificate
    if (props.hostedZoneId && props.hostedZoneName) {
      const hostedZone = route53.HostedZone.fromHostedZoneAttributes(this, 'HostedZone', {
        hostedZoneId: props.hostedZoneId,
        zoneName: props.hostedZoneName,
      });

      this.certificate = new acm.Certificate(this, 'Certificate', {
        domainName: props.domainName,
        validation: acm.CertificateValidation.fromDns(hostedZone),
      });
    } else {
      this.certificate = new acm.Certificate(this, 'Certificate', {
        domainName: props.domainName,
        validation: acm.CertificateValidation.fromEmail(),
      });
    }

    // Create Cognito authorizer
    const authorizer = new apigateway.CognitoUserPoolsAuthorizer(this, 'Authorizer', {
      cognitoUserPools: [props.userPool],
    });

    // Create API Gateway
    this.api = new apigateway.RestApi(this, 'Api', {
      restApiName: 'Opportunity Management Service API',
      description: 'API for managing sales opportunities',
      deployOptions: {
        stageName: 'v1',
        metricsEnabled: true,
        loggingLevel: apigateway.MethodLoggingLevel.INFO,
        dataTraceEnabled: true,
        tracingEnabled: true,
      },
      defaultCorsPreflightOptions: {
        allowOrigins: apigateway.Cors.ALL_ORIGINS,
        allowMethods: apigateway.Cors.ALL_METHODS,
        allowHeaders: [
          'Content-Type',
          'X-Amz-Date',
          'Authorization',
          'X-Api-Key',
          'X-Amz-Security-Token',
          'X-Request-ID',
        ],
        maxAge: cdk.Duration.days(1),
      },
      domainName: {
        domainName: props.domainName,
        certificate: this.certificate,
        endpointType: apigateway.EndpointType.EDGE,
      },
    });

    // Create VPC link
    const vpcLink = new apigateway.VpcLink(this, 'VpcLink', {
      targets: [props.loadBalancer],
      description: 'VPC Link for Opportunity Management Service',
    });

    // Create API resources
    const opportunities = this.api.root.addResource('opportunities');
    
    // GET /opportunities
    opportunities.addMethod('GET', new apigateway.Integration({
      type: apigateway.IntegrationType.HTTP_PROXY,
      integrationHttpMethod: 'GET',
      options: {
        connectionType: apigateway.ConnectionType.VPC_LINK,
        vpcLink: vpcLink,
        uri: `http://${props.loadBalancer.loadBalancerDnsName}/api/v1/opportunities`,
      },
    }), {
      authorizer: authorizer,
      authorizationType: apigateway.AuthorizationType.COGNITO,
    });

    // POST /opportunities
    opportunities.addMethod('POST', new apigateway.Integration({
      type: apigateway.IntegrationType.HTTP_PROXY,
      integrationHttpMethod: 'POST',
      options: {
        connectionType: apigateway.ConnectionType.VPC_LINK,
        vpcLink: vpcLink,
        uri: `http://${props.loadBalancer.loadBalancerDnsName}/api/v1/opportunities`,
      },
    }), {
      authorizer: authorizer,
      authorizationType: apigateway.AuthorizationType.COGNITO,
    });

    // Create opportunity resource
    const opportunity = opportunities.addResource('{opportunityId}');
    
    // GET /opportunities/{opportunityId}
    opportunity.addMethod('GET', new apigateway.Integration({
      type: apigateway.IntegrationType.HTTP_PROXY,
      integrationHttpMethod: 'GET',
      options: {
        connectionType: apigateway.ConnectionType.VPC_LINK,
        vpcLink: vpcLink,
        uri: `http://${props.loadBalancer.loadBalancerDnsName}/api/v1/opportunities/{opportunityId}`,
        requestParameters: {
          'integration.request.path.opportunityId': 'method.request.path.opportunityId',
        },
      },
    }), {
      authorizer: authorizer,
      authorizationType: apigateway.AuthorizationType.COGNITO,
      requestParameters: {
        'method.request.path.opportunityId': true,
      },
    });

    // PUT /opportunities/{opportunityId}
    opportunity.addMethod('PUT', new apigateway.Integration({
      type: apigateway.IntegrationType.HTTP_PROXY,
      integrationHttpMethod: 'PUT',
      options: {
        connectionType: apigateway.ConnectionType.VPC_LINK,
        vpcLink: vpcLink,
        uri: `http://${props.loadBalancer.loadBalancerDnsName}/api/v1/opportunities/{opportunityId}`,
        requestParameters: {
          'integration.request.path.opportunityId': 'method.request.path.opportunityId',
        },
      },
    }), {
      authorizer: authorizer,
      authorizationType: apigateway.AuthorizationType.COGNITO,
      requestParameters: {
        'method.request.path.opportunityId': true,
      },
    });

    // DELETE /opportunities/{opportunityId}
    opportunity.addMethod('DELETE', new apigateway.Integration({
      type: apigateway.IntegrationType.HTTP_PROXY,
      integrationHttpMethod: 'DELETE',
      options: {
        connectionType: apigateway.ConnectionType.VPC_LINK,
        vpcLink: vpcLink,
        uri: `http://${props.loadBalancer.loadBalancerDnsName}/api/v1/opportunities/{opportunityId}`,
        requestParameters: {
          'integration.request.path.opportunityId': 'method.request.path.opportunityId',
        },
      },
    }), {
      authorizer: authorizer,
      authorizationType: apigateway.AuthorizationType.COGNITO,
      requestParameters: {
        'method.request.path.opportunityId': true,
      },
    });

    // Create status resource
    const status = opportunity.addResource('status');
    
    // POST /opportunities/{opportunityId}/status
    status.addMethod('POST', new apigateway.Integration({
      type: apigateway.IntegrationType.HTTP_PROXY,
      integrationHttpMethod: 'POST',
      options: {
        connectionType: apigateway.ConnectionType.VPC_LINK,
        vpcLink: vpcLink,
        uri: `http://${props.loadBalancer.loadBalancerDnsName}/api/v1/opportunities/{opportunityId}/status`,
        requestParameters: {
          'integration.request.path.opportunityId': 'method.request.path.opportunityId',
        },
      },
    }), {
      authorizer: authorizer,
      authorizationType: apigateway.AuthorizationType.COGNITO,
      requestParameters: {
        'method.request.path.opportunityId': true,
      },
    });

    // Create problem-statements resource
    const problemStatements = opportunity.addResource('problem-statements');
    
    // POST /opportunities/{opportunityId}/problem-statements
    problemStatements.addMethod('POST', new apigateway.Integration({
      type: apigateway.IntegrationType.HTTP_PROXY,
      integrationHttpMethod: 'POST',
      options: {
        connectionType: apigateway.ConnectionType.VPC_LINK,
        vpcLink: vpcLink,
        uri: `http://${props.loadBalancer.loadBalancerDnsName}/api/v1/opportunities/{opportunityId}/problem-statements`,
        requestParameters: {
          'integration.request.path.opportunityId': 'method.request.path.opportunityId',
        },
      },
    }), {
      authorizer: authorizer,
      authorizationType: apigateway.AuthorizationType.COGNITO,
      requestParameters: {
        'method.request.path.opportunityId': true,
      },
    });

    // Add more resources and methods for other endpoints...

    // Create health check endpoint (no authorization required)
    const health = this.api.root.addResource('health');
    health.addMethod('GET', new apigateway.Integration({
      type: apigateway.IntegrationType.HTTP_PROXY,
      integrationHttpMethod: 'GET',
      options: {
        connectionType: apigateway.ConnectionType.VPC_LINK,
        vpcLink: vpcLink,
        uri: `http://${props.loadBalancer.loadBalancerDnsName}/health`,
      },
    }));

    // Create Route53 record if hosted zone is provided
    if (props.hostedZoneId && props.hostedZoneName) {
      const hostedZone = route53.HostedZone.fromHostedZoneAttributes(this, 'HostedZone', {
        hostedZoneId: props.hostedZoneId,
        zoneName: props.hostedZoneName,
      });

      new route53.ARecord(this, 'ApiRecord', {
        zone: hostedZone,
        recordName: props.domainName,
        target: route53.RecordTarget.fromAlias(
          new targets.ApiGateway(this.api)
        ),
      });
    }

    // Output API URL
    new cdk.CfnOutput(this, 'ApiUrl', {
      value: this.api.url,
      description: 'API Gateway URL',
      exportName: `${id}-api-url`,
    });

    // Output custom domain URL
    new cdk.CfnOutput(this, 'CustomDomainUrl', {
      value: `https://${props.domainName}`,
      description: 'Custom domain URL',
      exportName: `${id}-custom-domain-url`,
    });
  }
}
```

### API Stack

Create the API stack in `lib/stacks/api-stack.ts`:

```typescript
import * as cdk from '@aws-cdk/core';
import * as ec2 from '@aws-cdk/aws-ec2';
import * as ecs from '@aws-cdk/aws-ecs';
import * as elbv2 from '@aws-cdk/aws-elasticloadbalancingv2';
import * as apigateway from '@aws-cdk/aws-apigateway';
import * as cognito from '@aws-cdk/aws-cognito';
import { ApiGatewayConstruct } from '../constructs/api-gateway-construct';

export interface ApiStackProps extends cdk.StackProps {
  envConfig: any;
  vpc: ec2.Vpc;
  ecsService: ecs.FargateService;
  userPool: cognito.UserPool;
}

export class ApiStack extends cdk.Stack {
  public readonly apiGateway: apigateway.RestApi;

  constructor(scope: cdk.Construct, id: string, props: ApiStackProps) {
    super(scope, id, props);

    // Get load balancer from ECS service
    const loadBalancer = elbv2.ApplicationLoadBalancer.fromApplicationLoadBalancerAttributes(
      this,
      'ImportedALB',
      {
        loadBalancerArn: cdk.Fn.importValue(`${props.envConfig.env}-opportunity-compute-lb-arn`),
        securityGroupId: cdk.Fn.importValue(`${props.envConfig.env}-opportunity-compute-lb-sg-id`),
        loadBalancerDnsName: cdk.Fn.importValue(`${props.envConfig.env}-opportunity-compute-lb-dns`),
      }
    );

    // Create API Gateway
    const apiGatewayConstruct = new ApiGatewayConstruct(this, 'ApiGatewayConstruct', {
      vpc: props.vpc,
      loadBalancer: loadBalancer,
      userPool: props.userPool,
      domainName: props.envConfig.domainName,
      // Optional: Add hosted zone ID and name if you have a Route53 hosted zone
      // hostedZoneId: props.envConfig.hostedZoneId,
      // hostedZoneName: props.envConfig.hostedZoneName,
    });

    this.apiGateway = apiGatewayConstruct.api;
  }
}
```
