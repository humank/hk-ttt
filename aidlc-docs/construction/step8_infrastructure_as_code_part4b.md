# Step 8: Implement Infrastructure as Code (Part 4b)

## Monitoring Stack Implementation

### Monitoring Construct

Create the monitoring construct in `lib/constructs/monitoring-construct.ts`:

```typescript
import * as cdk from '@aws-cdk/core';
import * as ec2 from '@aws-cdk/aws-ec2';
import * as rds from '@aws-cdk/aws-rds';
import * as elasticache from '@aws-cdk/aws-elasticache';
import * as ecs from '@aws-cdk/aws-ecs';
import * as apigateway from '@aws-cdk/aws-apigateway';
import * as cloudwatch from '@aws-cdk/aws-cloudwatch';
import * as sns from '@aws-cdk/aws-sns';
import * as subscriptions from '@aws-cdk/aws-sns-subscriptions';
import * as cw_actions from '@aws-cdk/aws-cloudwatch-actions';

export interface MonitoringConstructProps {
  vpc: ec2.Vpc;
  database: rds.DatabaseInstance;
  redis: elasticache.CfnReplicationGroup;
  ecsService: ecs.FargateService;
  apiGateway: apigateway.RestApi;
  alarmEmail?: string;
}

export class MonitoringConstruct extends cdk.Construct {
  public readonly dashboard: cloudwatch.Dashboard;
  public readonly alarmTopic: sns.Topic;

  constructor(scope: cdk.Construct, id: string, props: MonitoringConstructProps) {
    super(scope, id);

    // Create SNS topic for alarms
    this.alarmTopic = new sns.Topic(this, 'AlarmTopic', {
      displayName: 'Opportunity Management Service Alarms',
    });

    // Add email subscription if provided
    if (props.alarmEmail) {
      this.alarmTopic.addSubscription(
        new subscriptions.EmailSubscription(props.alarmEmail)
      );
    }

    // Create dashboard
    this.dashboard = new cloudwatch.Dashboard(this, 'Dashboard', {
      dashboardName: 'OpportunityManagementService',
    });

    // Add ECS service metrics
    this.addEcsMetrics(props.ecsService);

    // Add database metrics
    this.addDatabaseMetrics(props.database);

    // Add Redis metrics
    this.addRedisMetrics(props.redis);

    // Add API Gateway metrics
    this.addApiGatewayMetrics(props.apiGateway);

    // Add VPC metrics
    this.addVpcMetrics(props.vpc);

    // Create alarms
    this.createAlarms(props);
  }

  private addEcsMetrics(ecsService: ecs.FargateService) {
    // CPU utilization
    const cpuUtilization = new cloudwatch.Metric({
      namespace: 'AWS/ECS',
      metricName: 'CPUUtilization',
      dimensionsMap: {
        ClusterName: ecsService.cluster.clusterName,
        ServiceName: ecsService.serviceName,
      },
      statistic: 'Average',
      period: cdk.Duration.minutes(1),
    });

    // Memory utilization
    const memoryUtilization = new cloudwatch.Metric({
      namespace: 'AWS/ECS',
      metricName: 'MemoryUtilization',
      dimensionsMap: {
        ClusterName: ecsService.cluster.clusterName,
        ServiceName: ecsService.serviceName,
      },
      statistic: 'Average',
      period: cdk.Duration.minutes(1),
    });

    // Running tasks
    const runningTasks = new cloudwatch.Metric({
      namespace: 'AWS/ECS',
      metricName: 'RunningTaskCount',
      dimensionsMap: {
        ClusterName: ecsService.cluster.clusterName,
        ServiceName: ecsService.serviceName,
      },
      statistic: 'Average',
      period: cdk.Duration.minutes(1),
    });

    // Add to dashboard
    this.dashboard.addWidgets(
      new cloudwatch.GraphWidget({
        title: 'ECS CPU Utilization',
        left: [cpuUtilization],
      }),
      new cloudwatch.GraphWidget({
        title: 'ECS Memory Utilization',
        left: [memoryUtilization],
      }),
      new cloudwatch.GraphWidget({
        title: 'ECS Running Tasks',
        left: [runningTasks],
      })
    );
  }

  private addDatabaseMetrics(database: rds.DatabaseInstance) {
    // CPU utilization
    const dbCpuUtilization = new cloudwatch.Metric({
      namespace: 'AWS/RDS',
      metricName: 'CPUUtilization',
      dimensionsMap: {
        DBInstanceIdentifier: database.instanceIdentifier,
      },
      statistic: 'Average',
      period: cdk.Duration.minutes(1),
    });

    // Database connections
    const dbConnections = new cloudwatch.Metric({
      namespace: 'AWS/RDS',
      metricName: 'DatabaseConnections',
      dimensionsMap: {
        DBInstanceIdentifier: database.instanceIdentifier,
      },
      statistic: 'Average',
      period: cdk.Duration.minutes(1),
    });

    // Free storage space
    const freeStorageSpace = new cloudwatch.Metric({
      namespace: 'AWS/RDS',
      metricName: 'FreeStorageSpace',
      dimensionsMap: {
        DBInstanceIdentifier: database.instanceIdentifier,
      },
      statistic: 'Average',
      period: cdk.Duration.minutes(1),
    });

    // Read IOPS
    const readIOPS = new cloudwatch.Metric({
      namespace: 'AWS/RDS',
      metricName: 'ReadIOPS',
      dimensionsMap: {
        DBInstanceIdentifier: database.instanceIdentifier,
      },
      statistic: 'Average',
      period: cdk.Duration.minutes(1),
    });

    // Write IOPS
    const writeIOPS = new cloudwatch.Metric({
      namespace: 'AWS/RDS',
      metricName: 'WriteIOPS',
      dimensionsMap: {
        DBInstanceIdentifier: database.instanceIdentifier,
      },
      statistic: 'Average',
      period: cdk.Duration.minutes(1),
    });

    // Add to dashboard
    this.dashboard.addWidgets(
      new cloudwatch.GraphWidget({
        title: 'RDS CPU Utilization',
        left: [dbCpuUtilization],
      }),
      new cloudwatch.GraphWidget({
        title: 'RDS Connections',
        left: [dbConnections],
      }),
      new cloudwatch.GraphWidget({
        title: 'RDS Free Storage Space',
        left: [freeStorageSpace],
      }),
      new cloudwatch.GraphWidget({
        title: 'RDS IOPS',
        left: [readIOPS, writeIOPS],
      })
    );
  }

  private addRedisMetrics(redis: elasticache.CfnReplicationGroup) {
    // CPU utilization
    const redisCpuUtilization = new cloudwatch.Metric({
      namespace: 'AWS/ElastiCache',
      metricName: 'CPUUtilization',
      dimensionsMap: {
        ReplicationGroupId: redis.ref,
      },
      statistic: 'Average',
      period: cdk.Duration.minutes(1),
    });

    // Memory usage
    const redisMemoryUsage = new cloudwatch.Metric({
      namespace: 'AWS/ElastiCache',
      metricName: 'DatabaseMemoryUsagePercentage',
      dimensionsMap: {
        ReplicationGroupId: redis.ref,
      },
      statistic: 'Average',
      period: cdk.Duration.minutes(1),
    });

    // Cache hits
    const cacheHits = new cloudwatch.Metric({
      namespace: 'AWS/ElastiCache',
      metricName: 'CacheHits',
      dimensionsMap: {
        ReplicationGroupId: redis.ref,
      },
      statistic: 'Sum',
      period: cdk.Duration.minutes(1),
    });

    // Cache misses
    const cacheMisses = new cloudwatch.Metric({
      namespace: 'AWS/ElastiCache',
      metricName: 'CacheMisses',
      dimensionsMap: {
        ReplicationGroupId: redis.ref,
      },
      statistic: 'Sum',
      period: cdk.Duration.minutes(1),
    });

    // Add to dashboard
    this.dashboard.addWidgets(
      new cloudwatch.GraphWidget({
        title: 'Redis CPU Utilization',
        left: [redisCpuUtilization],
      }),
      new cloudwatch.GraphWidget({
        title: 'Redis Memory Usage',
        left: [redisMemoryUsage],
      }),
      new cloudwatch.GraphWidget({
        title: 'Redis Cache Hits/Misses',
        left: [cacheHits, cacheMisses],
      })
    );
  }

  private addApiGatewayMetrics(apiGateway: apigateway.RestApi) {
    // Count
    const count = new cloudwatch.Metric({
      namespace: 'AWS/ApiGateway',
      metricName: 'Count',
      dimensionsMap: {
        ApiName: apiGateway.restApiName,
        Stage: 'v1',
      },
      statistic: 'Sum',
      period: cdk.Duration.minutes(1),
    });

    // Latency
    const latency = new cloudwatch.Metric({
      namespace: 'AWS/ApiGateway',
      metricName: 'Latency',
      dimensionsMap: {
        ApiName: apiGateway.restApiName,
        Stage: 'v1',
      },
      statistic: 'Average',
      period: cdk.Duration.minutes(1),
    });

    // 4XX errors
    const errors4xx = new cloudwatch.Metric({
      namespace: 'AWS/ApiGateway',
      metricName: '4XXError',
      dimensionsMap: {
        ApiName: apiGateway.restApiName,
        Stage: 'v1',
      },
      statistic: 'Sum',
      period: cdk.Duration.minutes(1),
    });

    // 5XX errors
    const errors5xx = new cloudwatch.Metric({
      namespace: 'AWS/ApiGateway',
      metricName: '5XXError',
      dimensionsMap: {
        ApiName: apiGateway.restApiName,
        Stage: 'v1',
      },
      statistic: 'Sum',
      period: cdk.Duration.minutes(1),
    });

    // Add to dashboard
    this.dashboard.addWidgets(
      new cloudwatch.GraphWidget({
        title: 'API Gateway Requests',
        left: [count],
      }),
      new cloudwatch.GraphWidget({
        title: 'API Gateway Latency',
        left: [latency],
      }),
      new cloudwatch.GraphWidget({
        title: 'API Gateway Errors',
        left: [errors4xx, errors5xx],
      })
    );
  }

  private addVpcMetrics(vpc: ec2.Vpc) {
    // NAT gateway bytes out
    const natGatewayBytesOut = new cloudwatch.Metric({
      namespace: 'AWS/NATGateway',
      metricName: 'BytesOutToDestination',
      statistic: 'Sum',
      period: cdk.Duration.minutes(5),
    });

    // NAT gateway bytes in
    const natGatewayBytesIn = new cloudwatch.Metric({
      namespace: 'AWS/NATGateway',
      metricName: 'BytesInFromSource',
      statistic: 'Sum',
      period: cdk.Duration.minutes(5),
    });

    // Add to dashboard
    this.dashboard.addWidgets(
      new cloudwatch.GraphWidget({
        title: 'NAT Gateway Traffic',
        left: [natGatewayBytesOut, natGatewayBytesIn],
      })
    );
  }

  private createAlarms(props: MonitoringConstructProps) {
    // ECS CPU utilization alarm
    const ecsCpuAlarm = new cloudwatch.Alarm(this, 'EcsCpuAlarm', {
      metric: new cloudwatch.Metric({
        namespace: 'AWS/ECS',
        metricName: 'CPUUtilization',
        dimensionsMap: {
          ClusterName: props.ecsService.cluster.clusterName,
          ServiceName: props.ecsService.serviceName,
        },
        statistic: 'Average',
        period: cdk.Duration.minutes(5),
      }),
      threshold: 80,
      evaluationPeriods: 3,
      datapointsToAlarm: 3,
      comparisonOperator: cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
      alarmDescription: 'ECS CPU utilization is high',
    });

    ecsCpuAlarm.addAlarmAction(new cw_actions.SnsAction(this.alarmTopic));

    // ECS memory utilization alarm
    const ecsMemoryAlarm = new cloudwatch.Alarm(this, 'EcsMemoryAlarm', {
      metric: new cloudwatch.Metric({
        namespace: 'AWS/ECS',
        metricName: 'MemoryUtilization',
        dimensionsMap: {
          ClusterName: props.ecsService.cluster.clusterName,
          ServiceName: props.ecsService.serviceName,
        },
        statistic: 'Average',
        period: cdk.Duration.minutes(5),
      }),
      threshold: 80,
      evaluationPeriods: 3,
      datapointsToAlarm: 3,
      comparisonOperator: cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
      alarmDescription: 'ECS memory utilization is high',
    });

    ecsMemoryAlarm.addAlarmAction(new cw_actions.SnsAction(this.alarmTopic));

    // Database CPU utilization alarm
    const dbCpuAlarm = new cloudwatch.Alarm(this, 'DbCpuAlarm', {
      metric: new cloudwatch.Metric({
        namespace: 'AWS/RDS',
        metricName: 'CPUUtilization',
        dimensionsMap: {
          DBInstanceIdentifier: props.database.instanceIdentifier,
        },
        statistic: 'Average',
        period: cdk.Duration.minutes(5),
      }),
      threshold: 80,
      evaluationPeriods: 3,
      datapointsToAlarm: 3,
      comparisonOperator: cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
      alarmDescription: 'Database CPU utilization is high',
    });

    dbCpuAlarm.addAlarmAction(new cw_actions.SnsAction(this.alarmTopic));

    // Database free storage space alarm
    const dbStorageAlarm = new cloudwatch.Alarm(this, 'DbStorageAlarm', {
      metric: new cloudwatch.Metric({
        namespace: 'AWS/RDS',
        metricName: 'FreeStorageSpace',
        dimensionsMap: {
          DBInstanceIdentifier: props.database.instanceIdentifier,
        },
        statistic: 'Average',
        period: cdk.Duration.minutes(5),
      }),
      threshold: 10 * 1024 * 1024 * 1024, // 10 GB
      evaluationPeriods: 3,
      datapointsToAlarm: 3,
      comparisonOperator: cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD,
      alarmDescription: 'Database free storage space is low',
    });

    dbStorageAlarm.addAlarmAction(new cw_actions.SnsAction(this.alarmTopic));

    // API Gateway 5XX errors alarm
    const api5xxAlarm = new cloudwatch.Alarm(this, 'Api5xxAlarm', {
      metric: new cloudwatch.Metric({
        namespace: 'AWS/ApiGateway',
        metricName: '5XXError',
        dimensionsMap: {
          ApiName: props.apiGateway.restApiName,
          Stage: 'v1',
        },
        statistic: 'Sum',
        period: cdk.Duration.minutes(5),
      }),
      threshold: 10,
      evaluationPeriods: 3,
      datapointsToAlarm: 3,
      comparisonOperator: cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
      alarmDescription: 'API Gateway 5XX errors are high',
    });

    api5xxAlarm.addAlarmAction(new cw_actions.SnsAction(this.alarmTopic));

    // API Gateway latency alarm
    const apiLatencyAlarm = new cloudwatch.Alarm(this, 'ApiLatencyAlarm', {
      metric: new cloudwatch.Metric({
        namespace: 'AWS/ApiGateway',
        metricName: 'Latency',
        dimensionsMap: {
          ApiName: props.apiGateway.restApiName,
          Stage: 'v1',
        },
        statistic: 'p95',
        period: cdk.Duration.minutes(5),
      }),
      threshold: 500, // 500 ms
      evaluationPeriods: 3,
      datapointsToAlarm: 3,
      comparisonOperator: cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
      alarmDescription: 'API Gateway latency is high',
    });

    apiLatencyAlarm.addAlarmAction(new cw_actions.SnsAction(this.alarmTopic));
  }
}
```

### Monitoring Stack

Create the monitoring stack in `lib/stacks/monitoring-stack.ts`:

```typescript
import * as cdk from '@aws-cdk/core';
import * as ec2 from '@aws-cdk/aws-ec2';
import * as rds from '@aws-cdk/aws-rds';
import * as elasticache from '@aws-cdk/aws-elasticache';
import * as ecs from '@aws-cdk/aws-ecs';
import * as apigateway from '@aws-cdk/aws-apigateway';
import * as cloudwatch from '@aws-cdk/aws-cloudwatch';
import * as sns from '@aws-cdk/aws-sns';
import { MonitoringConstruct } from '../constructs/monitoring-construct';

export interface MonitoringStackProps extends cdk.StackProps {
  envConfig: any;
  vpc: ec2.Vpc;
  database: rds.DatabaseInstance;
  redis: elasticache.CfnReplicationGroup;
  ecsService: ecs.FargateService;
  apiGateway: apigateway.RestApi;
}

export class MonitoringStack extends cdk.Stack {
  public readonly dashboard: cloudwatch.Dashboard;
  public readonly alarmTopic: sns.Topic;

  constructor(scope: cdk.Construct, id: string, props: MonitoringStackProps) {
    super(scope, id, props);

    // Create monitoring construct
    const monitoringConstruct = new MonitoringConstruct(this, 'MonitoringConstruct', {
      vpc: props.vpc,
      database: props.database,
      redis: props.redis,
      ecsService: props.ecsService,
      apiGateway: props.apiGateway,
      alarmEmail: props.envConfig.alarmEmail,
    });

    this.dashboard = monitoringConstruct.dashboard;
    this.alarmTopic = monitoringConstruct.alarmTopic;

    // Output dashboard URL
    new cdk.CfnOutput(this, 'DashboardUrl', {
      value: `https://${this.region}.console.aws.amazon.com/cloudwatch/home?region=${this.region}#dashboards:name=${this.dashboard.dashboardName}`,
      description: 'CloudWatch Dashboard URL',
      exportName: `${id}-dashboard-url`,
    });

    // Output alarm topic ARN
    new cdk.CfnOutput(this, 'AlarmTopicArn', {
      value: this.alarmTopic.topicArn,
      description: 'Alarm SNS topic ARN',
      exportName: `${id}-alarm-topic-arn`,
    });
  }
}
```

## Security Stack Implementation

### Security Construct

Create the security construct in `lib/constructs/security-construct.ts`:

```typescript
import * as cdk from '@aws-cdk/core';
import * as wafv2 from '@aws-cdk/aws-wafv2';
import * as apigateway from '@aws-cdk/aws-apigateway';
import * as iam from '@aws-cdk/aws-iam';

export interface SecurityConstructProps {
  apiGateway: apigateway.RestApi;
  rateLimit: number;
}

export class SecurityConstruct extends cdk.Construct {
  public readonly webAcl: wafv2.CfnWebACL;

  constructor(scope: cdk.Construct, id: string, props: SecurityConstructProps) {
    super(scope, id);

    // Create WAF Web ACL
    this.webAcl = new wafv2.CfnWebACL(this, 'WebAcl', {
      name: 'OpportunityManagementServiceWebAcl',
      description: 'Web ACL for Opportunity Management Service',
      scope: 'REGIONAL',
      defaultAction: {
        allow: {},
      },
      visibilityConfig: {
        cloudWatchMetricsEnabled: true,
        metricName: 'OpportunityManagementServiceWebAcl',
        sampledRequestsEnabled: true,
      },
      rules: [
        // AWS Managed Rules - Common Rule Set
        {
          name: 'AWSManagedRulesCommonRuleSet',
          priority: 10,
          overrideAction: { none: {} },
          statement: {
            managedRuleGroupStatement: {
              name: 'AWSManagedRulesCommonRuleSet',
              vendorName: 'AWS',
            },
          },
          visibilityConfig: {
            cloudWatchMetricsEnabled: true,
            metricName: 'AWSManagedRulesCommonRuleSet',
            sampledRequestsEnabled: true,
          },
        },
        // AWS Managed Rules - SQL Injection Rule Set
        {
          name: 'AWSManagedRulesSQLiRuleSet',
          priority: 20,
          overrideAction: { none: {} },
          statement: {
            managedRuleGroupStatement: {
              name: 'AWSManagedRulesSQLiRuleSet',
              vendorName: 'AWS',
            },
          },
          visibilityConfig: {
            cloudWatchMetricsEnabled: true,
            metricName: 'AWSManagedRulesSQLiRuleSet',
            sampledRequestsEnabled: true,
          },
        },
        // AWS Managed Rules - Known Bad Inputs Rule Set
        {
          name: 'AWSManagedRulesKnownBadInputsRuleSet',
          priority: 30,
          overrideAction: { none: {} },
          statement: {
            managedRuleGroupStatement: {
              name: 'AWSManagedRulesKnownBadInputsRuleSet',
              vendorName: 'AWS',
            },
          },
          visibilityConfig: {
            cloudWatchMetricsEnabled: true,
            metricName: 'AWSManagedRulesKnownBadInputsRuleSet',
            sampledRequestsEnabled: true,
          },
        },
        // Rate-based rule
        {
          name: 'RateLimitRule',
          priority: 40,
          action: { block: {} },
          statement: {
            rateBasedStatement: {
              limit: props.rateLimit,
              aggregateKeyType: 'IP',
            },
          },
          visibilityConfig: {
            cloudWatchMetricsEnabled: true,
            metricName: 'RateLimitRule',
            sampledRequestsEnabled: true,
          },
        },
      ],
    });

    // Associate Web ACL with API Gateway
    new wafv2.CfnWebACLAssociation(this, 'WebAclAssociation', {
      resourceArn: `arn:aws:apigateway:${cdk.Aws.REGION}::/restapis/${props.apiGateway.restApiId}/stages/v1`,
      webAclArn: this.webAcl.attrArn,
    });

    // Output Web ACL ARN
    new cdk.CfnOutput(this, 'WebAclArn', {
      value: this.webAcl.attrArn,
      description: 'Web ACL ARN',
      exportName: `${id}-web-acl-arn`,
    });
  }
}
```

### Security Stack

Create the security stack in `lib/stacks/security-stack.ts`:

```typescript
import * as cdk from '@aws-cdk/core';
import * as wafv2 from '@aws-cdk/aws-wafv2';
import * as apigateway from '@aws-cdk/aws-apigateway';
import { SecurityConstruct } from '../constructs/security-construct';

export interface SecurityStackProps extends cdk.StackProps {
  envConfig: any;
  apiGateway: apigateway.RestApi;
}

export class SecurityStack extends cdk.Stack {
  public readonly webAcl: wafv2.CfnWebACL;

  constructor(scope: cdk.Construct, id: string, props: SecurityStackProps) {
    super(scope, id, props);

    // Create security construct
    const securityConstruct = new SecurityConstruct(this, 'SecurityConstruct', {
      apiGateway: props.apiGateway,
      rateLimit: props.envConfig.env === 'prod' ? 1000 : 500, // Requests per 5 minutes
    });

    this.webAcl = securityConstruct.webAcl;
  }
}
```

## CI/CD Pipeline Implementation

To complete the infrastructure as code implementation, we should also create a CI/CD pipeline for automated deployment. This would be implemented in a separate stack, but for brevity, we'll outline the key components:

1. **Source Stage**: Pull code from a Git repository (e.g., CodeCommit, GitHub)
2. **Build Stage**: Build and test the application
3. **Deploy Dev Stage**: Deploy to the development environment
4. **Test Stage**: Run integration tests
5. **Approval Stage**: Manual approval for production deployment
6. **Deploy Prod Stage**: Deploy to the production environment

The pipeline would use AWS CodePipeline, CodeBuild, and CodeDeploy services to automate the deployment process.

## Deployment Instructions

To deploy the infrastructure:

1. Configure AWS credentials:
   ```bash
   aws configure
   ```

2. Bootstrap the CDK environment:
   ```bash
   cdk bootstrap aws://ACCOUNT-NUMBER/REGION
   ```

3. Deploy to development environment:
   ```bash
   cdk deploy --all --context env=dev
   ```

4. Deploy to production environment:
   ```bash
   cdk deploy --all --context env=prod
   ```

## Next Steps

1. Implement the CI/CD pipeline
2. Create automated tests for infrastructure
3. Set up cost monitoring and optimization
4. Implement disaster recovery procedures
5. Create documentation for operations team
