# Step 8: Implement Infrastructure as Code (Part 4a)

## Storage Stack Implementation

### S3 Construct

Create the S3 construct in `lib/constructs/s3-construct.ts`:

```typescript
import * as cdk from '@aws-cdk/core';
import * as s3 from '@aws-cdk/aws-s3';
import * as cloudfront from '@aws-cdk/aws-cloudfront';
import * as origins from '@aws-cdk/aws-cloudfront-origins';
import * as iam from '@aws-cdk/aws-iam';

export interface S3ConstructProps {
  bucketName: string;
  enableCloudFront: boolean;
  corsAllowedOrigins?: string[];
}

export class S3Construct extends cdk.Construct {
  public readonly bucket: s3.Bucket;
  public readonly cloudFrontDistribution?: cloudfront.Distribution;

  constructor(scope: cdk.Construct, id: string, props: S3ConstructProps) {
    super(scope, id);

    // Create S3 bucket
    this.bucket = new s3.Bucket(this, 'Bucket', {
      bucketName: props.bucketName,
      encryption: s3.BucketEncryption.S3_MANAGED,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      versioned: true,
      removalPolicy: cdk.RemovalPolicy.RETAIN,
      lifecycleRules: [
        {
          id: 'TransitionToIA',
          transitions: [
            {
              storageClass: s3.StorageClass.INFREQUENT_ACCESS,
              transitionAfter: cdk.Duration.days(30),
            },
          ],
        },
        {
          id: 'TransitionToGlacier',
          transitions: [
            {
              storageClass: s3.StorageClass.GLACIER,
              transitionAfter: cdk.Duration.days(90),
            },
          ],
        },
        {
          id: 'ExpireObjects',
          expiration: cdk.Duration.days(2555), // ~7 years for GDPR compliance
        },
      ],
      cors: props.corsAllowedOrigins
        ? [
            {
              allowedMethods: [
                s3.HttpMethods.GET,
                s3.HttpMethods.PUT,
                s3.HttpMethods.POST,
                s3.HttpMethods.DELETE,
                s3.HttpMethods.HEAD,
              ],
              allowedOrigins: props.corsAllowedOrigins,
              allowedHeaders: ['*'],
              maxAge: 3600,
            },
          ]
        : undefined,
    });

    // Create CloudFront distribution if enabled
    if (props.enableCloudFront) {
      // Create Origin Access Identity
      const originAccessIdentity = new cloudfront.OriginAccessIdentity(this, 'OAI', {
        comment: `OAI for ${props.bucketName}`,
      });

      // Grant read access to CloudFront
      this.bucket.grantRead(originAccessIdentity);

      // Create CloudFront distribution
      this.cloudFrontDistribution = new cloudfront.Distribution(this, 'Distribution', {
        defaultBehavior: {
          origin: new origins.S3Origin(this.bucket, {
            originAccessIdentity,
          }),
          viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
          allowedMethods: cloudfront.AllowedMethods.ALLOW_GET_HEAD,
          cachedMethods: cloudfront.CachedMethods.CACHE_GET_HEAD,
          cachePolicy: cloudfront.CachePolicy.CACHING_OPTIMIZED,
          originRequestPolicy: cloudfront.OriginRequestPolicy.CORS_S3_ORIGIN,
          responseHeadersPolicy: cloudfront.ResponseHeadersPolicy.CORS_ALLOW_ALL_ORIGINS,
        },
        priceClass: cloudfront.PriceClass.PRICE_CLASS_100,
        enableLogging: true,
        logBucket: new s3.Bucket(this, 'LogBucket', {
          encryption: s3.BucketEncryption.S3_MANAGED,
          blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
          lifecycleRules: [
            {
              expiration: cdk.Duration.days(365),
            },
          ],
          removalPolicy: cdk.RemovalPolicy.DESTROY,
        }),
        logFilePrefix: 'cloudfront-logs/',
      });

      // Output CloudFront domain name
      new cdk.CfnOutput(this, 'CloudFrontDomainName', {
        value: this.cloudFrontDistribution.distributionDomainName,
        description: 'CloudFront distribution domain name',
        exportName: `${id}-cloudfront-domain`,
      });
    }

    // Output bucket name
    new cdk.CfnOutput(this, 'BucketName', {
      value: this.bucket.bucketName,
      description: 'S3 bucket name',
      exportName: `${id}-bucket-name`,
    });

    // Output bucket ARN
    new cdk.CfnOutput(this, 'BucketArn', {
      value: this.bucket.bucketArn,
      description: 'S3 bucket ARN',
      exportName: `${id}-bucket-arn`,
    });
  }
}
```

### Storage Stack

Create the storage stack in `lib/stacks/storage-stack.ts`:

```typescript
import * as cdk from '@aws-cdk/core';
import * as s3 from '@aws-cdk/aws-s3';
import { S3Construct } from '../constructs/s3-construct';

export interface StorageStackProps extends cdk.StackProps {
  envConfig: any;
}

export class StorageStack extends cdk.Stack {
  public readonly attachmentsBucket: s3.Bucket;
  public readonly exportsBucket: s3.Bucket;

  constructor(scope: cdk.Construct, id: string, props: StorageStackProps) {
    super(scope, id, props);

    // Create attachments bucket
    const attachmentsConstruct = new S3Construct(this, 'AttachmentsConstruct', {
      bucketName: `opportunity-attachments-${props.envConfig.env}-${this.account}`,
      enableCloudFront: true,
      corsAllowedOrigins: ['*'], // In production, restrict to specific origins
    });

    this.attachmentsBucket = attachmentsConstruct.bucket;

    // Create exports bucket
    const exportsConstruct = new S3Construct(this, 'ExportsConstruct', {
      bucketName: `opportunity-exports-${props.envConfig.env}-${this.account}`,
      enableCloudFront: false,
    });

    this.exportsBucket = exportsConstruct.bucket;
  }
}
```

## Auth Stack Implementation

### Cognito Construct

Create the Cognito construct in `lib/constructs/cognito-construct.ts`:

```typescript
import * as cdk from '@aws-cdk/core';
import * as cognito from '@aws-cdk/aws-cognito';
import * as iam from '@aws-cdk/aws-iam';
import * as lambda from '@aws-cdk/aws-lambda';

export interface CognitoConstructProps {
  userPoolName: string;
  clientName: string;
  customDomain?: string;
  emailSendingAccount?: cognito.EmailSendingAccount;
  emailSourceArn?: string;
  smsRole?: iam.Role;
  preTokenGenerationFunction?: lambda.Function;
}

export class CognitoConstruct extends cdk.Construct {
  public readonly userPool: cognito.UserPool;
  public readonly userPoolClient: cognito.UserPoolClient;
  public readonly userPoolDomain: cognito.UserPoolDomain;

  constructor(scope: cdk.Construct, id: string, props: CognitoConstructProps) {
    super(scope, id);

    // Create user pool
    this.userPool = new cognito.UserPool(this, 'UserPool', {
      userPoolName: props.userPoolName,
      selfSignUpEnabled: false, // Users are created by admins
      signInAliases: {
        email: true,
        username: true,
      },
      autoVerify: {
        email: true,
      },
      standardAttributes: {
        givenName: {
          required: true,
          mutable: true,
        },
        familyName: {
          required: true,
          mutable: true,
        },
        email: {
          required: true,
          mutable: true,
        },
      },
      customAttributes: {
        role: new cognito.StringAttribute({ mutable: true }),
        department: new cognito.StringAttribute({ mutable: true }),
      },
      passwordPolicy: {
        minLength: 12,
        requireLowercase: true,
        requireUppercase: true,
        requireDigits: true,
        requireSymbols: true,
        tempPasswordValidity: cdk.Duration.days(7),
      },
      accountRecovery: cognito.AccountRecovery.EMAIL_ONLY,
      removalPolicy: cdk.RemovalPolicy.RETAIN,
    });

    // Configure email sending if provided
    if (props.emailSendingAccount && props.emailSourceArn) {
      const cfnUserPool = this.userPool.node.defaultChild as cognito.CfnUserPool;
      cfnUserPool.emailConfiguration = {
        emailSendingAccount: props.emailSendingAccount,
        sourceArn: props.emailSourceArn,
      };
    }

    // Configure SMS role if provided
    if (props.smsRole) {
      const cfnUserPool = this.userPool.node.defaultChild as cognito.CfnUserPool;
      cfnUserPool.smsConfiguration = {
        externalId: `${id}-external`,
        snsCallerArn: props.smsRole.roleArn,
      };
    }

    // Configure pre token generation Lambda trigger if provided
    if (props.preTokenGenerationFunction) {
      this.userPool.addTrigger(
        cognito.UserPoolOperation.PRE_TOKEN_GENERATION,
        props.preTokenGenerationFunction
      );
    }

    // Create user pool client
    this.userPoolClient = this.userPool.addClient('UserPoolClient', {
      userPoolClientName: props.clientName,
      authFlows: {
        userPassword: true,
        userSrp: true,
        adminUserPassword: true,
      },
      oAuth: {
        flows: {
          authorizationCodeGrant: true,
          implicitCodeGrant: true,
        },
        scopes: [
          cognito.OAuthScope.EMAIL,
          cognito.OAuthScope.OPENID,
          cognito.OAuthScope.PROFILE,
          cognito.OAuthScope.COGNITO_ADMIN,
        ],
        callbackUrls: [
          'http://localhost:3000/callback',
          'https://app.example.com/callback',
        ],
        logoutUrls: [
          'http://localhost:3000/logout',
          'https://app.example.com/logout',
        ],
      },
      preventUserExistenceErrors: true,
      refreshTokenValidity: cdk.Duration.days(30),
      accessTokenValidity: cdk.Duration.hours(1),
      idTokenValidity: cdk.Duration.hours(1),
      enableTokenRevocation: true,
    });

    // Create user pool domain
    if (props.customDomain) {
      this.userPoolDomain = this.userPool.addDomain('CustomDomain', {
        customDomain: {
          domainName: props.customDomain,
          certificate: acm.Certificate.fromCertificateArn(
            this,
            'Certificate',
            // Replace with your ACM certificate ARN
            'arn:aws:acm:us-east-1:123456789012:certificate/abcdef12-3456-7890-abcd-ef1234567890'
          ),
        },
      });
    } else {
      this.userPoolDomain = this.userPool.addDomain('CognitoDomain', {
        cognitoDomain: {
          domainPrefix: `${props.userPoolName.toLowerCase()}-${this.node.addr.substring(0, 8)}`,
        },
      });
    }

    // Create resource server for custom scopes
    const resourceServer = this.userPool.addResourceServer('ResourceServer', {
      identifier: 'opportunities',
      scopes: [
        {
          scopeName: 'read',
          scopeDescription: 'Read opportunities',
        },
        {
          scopeName: 'write',
          scopeDescription: 'Create and update opportunities',
        },
        {
          scopeName: 'delete',
          scopeDescription: 'Delete opportunities',
        },
        {
          scopeName: 'admin',
          scopeDescription: 'Administrative access',
        },
      ],
    });

    // Output user pool ID
    new cdk.CfnOutput(this, 'UserPoolId', {
      value: this.userPool.userPoolId,
      description: 'User pool ID',
      exportName: `${id}-user-pool-id`,
    });

    // Output user pool client ID
    new cdk.CfnOutput(this, 'UserPoolClientId', {
      value: this.userPoolClient.userPoolClientId,
      description: 'User pool client ID',
      exportName: `${id}-user-pool-client-id`,
    });

    // Output user pool domain
    new cdk.CfnOutput(this, 'UserPoolDomain', {
      value: this.userPoolDomain.domainName,
      description: 'User pool domain',
      exportName: `${id}-user-pool-domain`,
    });
  }
}
```

### Auth Stack

Create the auth stack in `lib/stacks/auth-stack.ts`:

```typescript
import * as cdk from '@aws-cdk/core';
import * as cognito from '@aws-cdk/aws-cognito';
import * as iam from '@aws-cdk/aws-iam';
import * as lambda from '@aws-cdk/aws-lambda';
import { CognitoConstruct } from '../constructs/cognito-construct';

export interface AuthStackProps extends cdk.StackProps {
  envConfig: any;
}

export class AuthStack extends cdk.Stack {
  public readonly userPool: cognito.UserPool;
  public readonly userPoolClient: cognito.UserPoolClient;

  constructor(scope: cdk.Construct, id: string, props: AuthStackProps) {
    super(scope, id, props);

    // Create SMS role for Cognito
    const smsRole = new iam.Role(this, 'CognitoSMSRole', {
      assumedBy: new iam.ServicePrincipal('cognito-idp.amazonaws.com'),
    });

    smsRole.addToPolicy(
      new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: ['sns:Publish'],
        resources: ['*'],
      })
    );

    // Create pre token generation Lambda function
    const preTokenGenerationFunction = new lambda.Function(this, 'PreTokenGenerationFunction', {
      runtime: lambda.Runtime.NODEJS_14_X,
      handler: 'index.handler',
      code: lambda.Code.fromInline(`
        exports.handler = (event, context, callback) => {
          // Add custom claims to the token
          event.response = {
            claimsOverrideDetails: {
              claimsToAddOrOverride: {
                'custom:role': event.request.userAttributes['custom:role'],
                'custom:department': event.request.userAttributes['custom:department'],
              },
            },
          };
          
          // Return to Amazon Cognito
          callback(null, event);
        };
      `),
      description: 'Pre token generation Lambda trigger for Cognito',
    });

    // Create Cognito user pool
    const cognitoConstruct = new CognitoConstruct(this, 'CognitoConstruct', {
      userPoolName: `OpportunityManagementService-${props.envConfig.env}`,
      clientName: `opportunity-management-service-${props.envConfig.env}`,
      smsRole: smsRole,
      preTokenGenerationFunction: preTokenGenerationFunction,
      // Optional: Add custom domain if available
      // customDomain: `auth.${props.envConfig.domainName}`,
    });

    this.userPool = cognitoConstruct.userPool;
    this.userPoolClient = cognitoConstruct.userPoolClient;
  }
}
```
