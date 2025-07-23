# Step 3: Select AWS Services

Based on the requirements analysis and API architecture decisions, this document outlines the AWS services selected for the Opportunity Management Service implementation.

## Compute Service Selection

### Options Considered

1. **AWS Lambda**
   - Serverless compute service
   - Pay-per-use pricing model
   - Auto-scaling built-in
   - Limited execution time (15 minutes max)
   - Cold start latency concerns

2. **Amazon ECS (Elastic Container Service) with Fargate**
   - Containerized deployment
   - No server management with Fargate
   - More consistent performance than Lambda
   - Better for long-running processes
   - Auto-scaling capabilities

3. **Amazon EKS (Elastic Kubernetes Service)**
   - Kubernetes-based container orchestration
   - More complex to set up and maintain
   - Better for large, complex microservices architectures
   - More control over infrastructure

4. **Amazon EC2 (Elastic Compute Cloud)**
   - Traditional virtual server approach
   - Full control over the environment
   - Requires more management overhead
   - Manual scaling or Auto Scaling Groups

### Decision: Amazon ECS with Fargate

**Rationale:**
1. **Performance Requirements**: The service needs to handle up to 500 RPS with low latency (< 200ms for reads, < 500ms for writes). Fargate provides more consistent performance compared to Lambda, avoiding cold start issues.
2. **Complexity**: The service has multiple interconnected components and repositories, which fits better with a containerized approach than with Lambda functions.
3. **Deployment Frequency**: Weekly deployments for features and daily deployments for bug fixes are well-supported by container-based deployments.
4. **Cost Efficiency**: Fargate provides a good balance between operational overhead and cost, with pay-for-what-you-use pricing.
5. **Scalability**: Fargate can easily scale to handle the peak load of 500 RPS during business hours.
6. **Integration**: Better integration with existing RDS database due to persistent connections.

## API Management Service Selection

### Options Considered

1. **Amazon API Gateway (REST API)**
   - Fully managed service for REST APIs
   - Request throttling and rate limiting
   - API keys and usage plans
   - Integration with AWS Lambda, HTTP endpoints, and other AWS services
   - Caching capabilities

2. **Amazon API Gateway (HTTP API)**
   - Simpler and more cost-effective than REST API
   - Lower latency
   - Fewer features than REST API
   - Limited integration options

3. **AWS AppSync**
   - Managed GraphQL service
   - Real-time data synchronization
   - Offline data access
   - Complex to set up for REST-style APIs

### Decision: Amazon API Gateway (REST API)

**Rationale:**
1. **API Architecture**: We've chosen a REST API architecture, which aligns perfectly with API Gateway REST API.
2. **Feature Set**: REST API provides all the features we need, including request validation, throttling, and authorization.
3. **Caching**: REST API supports response caching, which helps meet the latency requirements.
4. **Security**: Strong integration with Cognito for authentication and authorization.
5. **Monitoring**: Comprehensive logging and monitoring capabilities.
6. **Rate Limiting**: Built-in throttling and rate limiting to protect the backend services.

## Database Service Selection

### Options Considered

1. **Amazon RDS (Relational Database Service)**
   - Fully managed relational database service
   - Supports multiple database engines (MySQL, PostgreSQL, etc.)
   - Automatic backups and patching
   - Multi-AZ deployments for high availability

2. **Amazon DynamoDB**
   - Fully managed NoSQL database
   - Millisecond latency at any scale
   - Auto-scaling capabilities
   - Pay-per-request pricing option
   - Less suitable for complex relational data

3. **Amazon Aurora**
   - MySQL and PostgreSQL-compatible relational database
   - Higher performance than standard RDS
   - Automatic scaling
   - Higher cost than standard RDS

### Decision: Use Existing Amazon RDS Database

**Rationale:**
1. **Integration Requirement**: The service needs to integrate with an existing RDS database.
2. **Data Model**: The domain model is highly relational with many interconnected entities, which fits well with a relational database.
3. **Data Volume**: The expected data volume (10GB initially, growing by 1GB per month) is well within RDS capabilities.
4. **Consistency**: The service requires strong consistency for operations like opportunity submission and cancellation.
5. **GDPR Compliance**: RDS provides features that help with GDPR compliance, such as encryption at rest and in transit.

## Additional Supporting Services

### 1. Amazon Cognito (Authentication and Authorization)

- Use the existing Cognito user pool for authentication
- Implement JWT token validation
- Configure role-based access control

### 2. Amazon ElastiCache (Caching)

- Redis-based caching for frequently accessed data
- Helps meet the latency requirements for read operations
- Cache opportunity details, skill requirements, and other relatively static data

### 3. Amazon S3 (File Storage)

- Store attachments securely
- Integrate with CloudFront for faster content delivery
- Implement lifecycle policies for cost optimization

### 4. AWS CloudFront (Content Delivery)

- Deliver attachments and static content with low latency
- Global distribution for faster access
- Reduce load on the main application

### 5. Amazon CloudWatch (Monitoring and Logging)

- Collect and track metrics
- Set up alarms for performance issues
- Centralized logging
- Create dashboards for visibility

### 6. AWS X-Ray (Distributed Tracing)

- Trace requests through the application
- Identify performance bottlenecks
- Troubleshoot issues in production

### 7. AWS WAF (Web Application Firewall)

- Protect the API from common web exploits
- Implement rate-based rules to prevent DDoS attacks
- Configure security rules for GDPR compliance

### 8. AWS Secrets Manager

- Store database credentials and other secrets
- Rotate secrets automatically
- Integrate with ECS for secure access to secrets

### 9. Amazon ECR (Elastic Container Registry)

- Store and manage Docker container images
- Integrate with ECS for deployment
- Implement vulnerability scanning

### 10. AWS CodePipeline and CodeBuild (CI/CD)

- Automate the build and deployment process
- Support frequent deployments (daily/weekly)
- Implement testing stages

## Service Architecture Diagram

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  AWS CloudFront │     │   AWS WAF       │     │  Amazon Cognito │
│                 │     │                 │     │                 │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                     Amazon API Gateway                          │
│                                                                 │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                 Amazon ECS with Fargate                         │
│                                                                 │
└───────┬─────────────────────────┬─────────────────────┬─────────┘
        │                         │                     │
        ▼                         ▼                     ▼
┌───────────────┐       ┌─────────────────┐     ┌───────────────┐
│               │       │                 │     │               │
│  Amazon RDS   │       │ Amazon          │     │   Amazon S3   │
│               │       │ ElastiCache     │     │               │
└───────────────┘       └─────────────────┘     └───────────────┘
```

## Summary of Selected Services

| Requirement | Selected Service | Justification |
|-------------|-----------------|---------------|
| Compute | Amazon ECS with Fargate | Better performance consistency, suitable for complex services, auto-scaling capabilities |
| API Management | Amazon API Gateway (REST API) | Full feature set for REST APIs, caching, security, and monitoring |
| Database | Existing Amazon RDS | Integration requirement, relational data model, GDPR compliance features |
| Authentication | Amazon Cognito | Integration requirement, OAuth 2.0 with JWT support, role-based access control |
| File Storage | Amazon S3 | Secure, scalable storage for attachments |
| Caching | Amazon ElastiCache | Meet latency requirements for read operations |
| Content Delivery | AWS CloudFront | Fast delivery of attachments and static content |
| Monitoring | Amazon CloudWatch | Comprehensive monitoring and logging |
| Tracing | AWS X-Ray | Distributed tracing for performance optimization |
| Security | AWS WAF | Protection against web exploits and DDoS attacks |
| Secret Management | AWS Secrets Manager | Secure storage and rotation of credentials |
| Container Registry | Amazon ECR | Storage and management of container images |
| CI/CD | AWS CodePipeline and CodeBuild | Automated build and deployment process |
