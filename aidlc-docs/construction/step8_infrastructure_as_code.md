# Step 8: Implement Infrastructure as Code

This document outlines the implementation of Infrastructure as Code (IaC) for the Opportunity Management Service using AWS Cloud Development Kit (CDK).

## AWS CDK Overview

AWS CDK is a software development framework for defining cloud infrastructure in code and provisioning it through AWS CloudFormation. We'll use CDK with TypeScript for our infrastructure implementation.

## Project Structure

```
opportunity-management-service-infra/
├── bin/
│   └── opportunity-management-service-infra.ts
├── lib/
│   ├── constructs/
│   │   ├── vpc-construct.ts
│   │   ├── database-construct.ts
│   │   ├── cache-construct.ts
│   │   ├── ecs-construct.ts
│   │   ├── api-gateway-construct.ts
│   │   ├── s3-construct.ts
│   │   ├── cognito-construct.ts
│   │   ├── monitoring-construct.ts
│   │   └── security-construct.ts
│   ├── stacks/
│   │   ├── network-stack.ts
│   │   ├── data-stack.ts
│   │   ├── compute-stack.ts
│   │   ├── api-stack.ts
│   │   ├── storage-stack.ts
│   │   ├── auth-stack.ts
│   │   ├── monitoring-stack.ts
│   │   └── security-stack.ts
│   └── opportunity-management-service-infra-stack.ts
├── test/
│   └── opportunity-management-service-infra.test.ts
├── cdk.json
├── package.json
└── tsconfig.json
```

## CDK Setup

### Initialize CDK Project

```bash
# Install CDK globally
npm install -g aws-cdk

# Create a new CDK project
mkdir opportunity-management-service-infra
cd opportunity-management-service-infra
cdk init app --language typescript

# Install dependencies
npm install @aws-cdk/aws-ec2 @aws-cdk/aws-ecs @aws-cdk/aws-ecs-patterns \
  @aws-cdk/aws-rds @aws-cdk/aws-elasticache @aws-cdk/aws-apigateway \
  @aws-cdk/aws-s3 @aws-cdk/aws-cognito @aws-cdk/aws-cloudwatch \
  @aws-cdk/aws-wafv2 @aws-cdk/aws-iam @aws-cdk/aws-logs \
  @aws-cdk/aws-certificatemanager @aws-cdk/aws-route53
```

### CDK Configuration

Create a `cdk.json` file with the following content:

```json
{
  "app": "npx ts-node --prefer-ts-exts bin/opportunity-management-service-infra.ts",
  "context": {
    "@aws-cdk/core:enableStackNameDuplicates": "false",
    "aws-cdk:enableDiffNoFail": "true",
    "@aws-cdk/core:stackRelativeExports": "true",
    "@aws-cdk/aws-ecr-assets:dockerIgnoreSupport": true,
    "@aws-cdk/aws-secretsmanager:parseOwnedSecretName": true,
    "@aws-cdk/aws-kms:defaultKeyPolicies": true,
    "@aws-cdk/aws-s3:grantWriteWithoutAcl": true,
    "@aws-cdk/aws-ecs-patterns:removeDefaultDesiredCount": true,
    "environments": {
      "dev": {
        "account": "123456789012",
        "region": "us-east-1",
        "vpcCidr": "10.0.0.0/16",
        "availabilityZones": ["us-east-1a", "us-east-1b", "us-east-1c"],
        "databaseInstanceType": "db.r5.large",
        "cacheNodeType": "cache.m5.large",
        "ecsTaskCpu": 1024,
        "ecsTaskMemory": 2048,
        "ecsMinCapacity": 3,
        "ecsMaxCapacity": 10,
        "domainName": "dev-api.example.com"
      },
      "prod": {
        "account": "123456789012",
        "region": "us-east-1",
        "vpcCidr": "10.0.0.0/16",
        "availabilityZones": ["us-east-1a", "us-east-1b", "us-east-1c"],
        "databaseInstanceType": "db.r5.xlarge",
        "cacheNodeType": "cache.m5.xlarge",
        "ecsTaskCpu": 2048,
        "ecsTaskMemory": 4096,
        "ecsMinCapacity": 5,
        "ecsMaxCapacity": 20,
        "domainName": "api.example.com"
      }
    }
  }
}
```

### Entry Point

Create the entry point file `bin/opportunity-management-service-infra.ts`:

```typescript
#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { NetworkStack } from '../lib/stacks/network-stack';
import { DataStack } from '../lib/stacks/data-stack';
import { ComputeStack } from '../lib/stacks/compute-stack';
import { ApiStack } from '../lib/stacks/api-stack';
import { StorageStack } from '../lib/stacks/storage-stack';
import { AuthStack } from '../lib/stacks/auth-stack';
import { MonitoringStack } from '../lib/stacks/monitoring-stack';
import { SecurityStack } from '../lib/stacks/security-stack';

const app = new cdk.App();

// Get environment from context
const envName = app.node.tryGetContext('env') || 'dev';
const envConfig = app.node.tryGetContext('environments')[envName];

if (!envConfig) {
  throw new Error(`Environment ${envName} not found in cdk.json`);
}

// Create environment
const env = {
  account: envConfig.account,
  region: envConfig.region
};

// Create stacks
const networkStack = new NetworkStack(app, `${envName}-opportunity-network`, {
  env,
  envConfig
});

const dataStack = new DataStack(app, `${envName}-opportunity-data`, {
  env,
  envConfig,
  vpc: networkStack.vpc
});

const storageStack = new StorageStack(app, `${envName}-opportunity-storage`, {
  env,
  envConfig
});

const authStack = new AuthStack(app, `${envName}-opportunity-auth`, {
  env,
  envConfig
});

const computeStack = new ComputeStack(app, `${envName}-opportunity-compute`, {
  env,
  envConfig,
  vpc: networkStack.vpc,
  database: dataStack.database,
  redis: dataStack.redis,
  attachmentsBucket: storageStack.attachmentsBucket,
  userPool: authStack.userPool
});

const apiStack = new ApiStack(app, `${envName}-opportunity-api`, {
  env,
  envConfig,
  vpc: networkStack.vpc,
  ecsService: computeStack.ecsService,
  userPool: authStack.userPool
});

const monitoringStack = new MonitoringStack(app, `${envName}-opportunity-monitoring`, {
  env,
  envConfig,
  vpc: networkStack.vpc,
  database: dataStack.database,
  redis: dataStack.redis,
  ecsService: computeStack.ecsService,
  apiGateway: apiStack.apiGateway
});

const securityStack = new SecurityStack(app, `${envName}-opportunity-security`, {
  env,
  envConfig,
  apiGateway: apiStack.apiGateway
});

// Add tags to all stacks
const stacks = [
  networkStack,
  dataStack,
  computeStack,
  apiStack,
  storageStack,
  authStack,
  monitoringStack,
  securityStack
];

stacks.forEach(stack => {
  cdk.Tags.of(stack).add('Environment', envName);
  cdk.Tags.of(stack).add('Project', 'OpportunityManagementService');
  cdk.Tags.of(stack).add('Owner', 'SalesTeam');
});
```
