# Step 5: Design Infrastructure Architecture

This document outlines the infrastructure architecture design for the Opportunity Management Service.

## Network Architecture

### VPC Design

We will create a dedicated VPC for the Opportunity Management Service with the following components:

1. **VPC CIDR**: 10.0.0.0/16
2. **Availability Zones**: Deploy across 3 AZs for high availability
3. **Subnets**:
   - **Public Subnets**: 10.0.0.0/24, 10.0.1.0/24, 10.0.2.0/24
     - For NAT Gateways and load balancers
   - **Private App Subnets**: 10.0.10.0/24, 10.0.11.0/24, 10.0.12.0/24
     - For ECS Fargate tasks
   - **Private Data Subnets**: 10.0.20.0/24, 10.0.21.0/24, 10.0.22.0/24
     - For RDS and ElastiCache

4. **NAT Gateways**:
   - One NAT Gateway per AZ for high availability
   - Placed in public subnets

5. **Internet Gateway**:
   - Single Internet Gateway for the VPC
   - Connected to public subnets

6. **Route Tables**:
   - Public route table with routes to the Internet Gateway
   - Private app route tables with routes to NAT Gateways
   - Private data route tables with no internet access

7. **Security Groups**:
   - **ALB Security Group**: Allow HTTP/HTTPS from internet
   - **ECS Security Group**: Allow traffic from ALB security group
   - **RDS Security Group**: Allow MySQL/PostgreSQL from ECS security group
   - **ElastiCache Security Group**: Allow Redis from ECS security group

8. **Network ACLs**:
   - Default NACLs with custom rules for additional security

### Network Diagram

```
                                  Internet
                                     │
                                     ▼
                              ┌──────────────┐
                              │    AWS WAF   │
                              └──────┬───────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Internet Gateway                         │
└─────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                         Public Subnets                          │
│                                                                 │
└───────┬─────────────────────┬─────────────────────┬─────────────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│ NAT Gateway 1 │     │ NAT Gateway 2 │     │ NAT Gateway 3 │
└───────┬───────┘     └───────┬───────┘     └───────┬───────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                      Private App Subnets                        │
│                                                                 │
└───────┬─────────────────────┬─────────────────────┬─────────────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│  ECS Fargate  │     │  ECS Fargate  │     │  ECS Fargate  │
│  (AZ 1)       │     │  (AZ 2)       │     │  (AZ 3)       │
└───────┬───────┘     └───────┬───────┘     └───────┬───────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                      Private Data Subnets                       │
│                                                                 │
└───────┬─────────────────────┬─────────────────────┬─────────────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│  RDS Instance │     │  RDS Standby  │     │  ElastiCache  │
│  (Primary)    │     │  (Replica)    │     │  (Redis)      │
└───────────────┘     └───────────────┘     └───────────────┘
```

## Service Deployment Architecture

### ECS Fargate Configuration

1. **ECS Cluster**:
   - Dedicated cluster for the Opportunity Management Service
   - Fargate launch type for serverless container management

2. **Task Definitions**:
   - **API Service Task**: Runs the API service container
     - CPU: 1 vCPU
     - Memory: 2 GB
     - Essential container: API service
     - Sidecar container: AWS X-Ray daemon
   
   - **Background Worker Task** (for async processing):
     - CPU: 1 vCPU
     - Memory: 2 GB
     - Essential container: Worker service

3. **ECS Services**:
   - **API Service**:
     - Desired count: 3 (minimum)
     - Auto-scaling: Based on CPU utilization and request count
     - Maximum count: 10
     - Deployment configuration: Rolling update with 100% minimum healthy percent
   
   - **Worker Service**:
     - Desired count: 2 (minimum)
     - Auto-scaling: Based on queue depth
     - Maximum count: 5

4. **Load Balancer**:
   - Application Load Balancer (ALB)
   - HTTPS listeners with ACM certificates
   - Health checks on `/health` endpoint
   - Target groups for API service

5. **Auto-scaling Policies**:
   - **API Service**:
     - Scale out: CPU utilization > 70% for 3 minutes
     - Scale out: Request count > 1000 per target for 3 minutes
     - Scale in: CPU utilization < 30% for 10 minutes
   
   - **Worker Service**:
     - Scale out: Queue depth > 100 messages for 3 minutes
     - Scale in: Queue depth < 10 messages for 10 minutes

### Container Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      ECS Task Definition                    │
│                                                             │
│  ┌─────────────────────────┐    ┌─────────────────────────┐ │
│  │                         │    │                         │ │
│  │    API Service          │    │    X-Ray Daemon         │ │
│  │    Container            │    │    Container            │ │
│  │                         │    │                         │ │
│  └─────────────────────────┘    └─────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Database Architecture

### RDS Configuration

We will use the existing RDS database with the following configuration:

1. **Database Engine**: PostgreSQL (assuming based on the domain model)
2. **Deployment**: Multi-AZ for high availability
3. **Instance Type**: db.r5.large (assuming based on data size and traffic)
4. **Storage**: 100 GB with auto-scaling enabled
5. **Backup**: Daily automated backups with 7-day retention
6. **Maintenance Window**: Weekly during off-peak hours
7. **Parameter Group**: Custom parameters for performance optimization
8. **Security**:
   - Encryption at rest using AWS KMS
   - SSL/TLS for data in transit
   - IAM database authentication

### Connection Pooling

1. **PgBouncer**:
   - Deployed as a sidecar container
   - Connection pooling for efficient database connections
   - Default pool size: 20 connections per container
   - Maximum pool size: 50 connections per container

### Database Scaling Strategy

1. **Vertical Scaling**:
   - Monitor CPU and memory utilization
   - Upgrade instance type when utilization consistently exceeds 70%

2. **Read Scaling**:
   - Deploy read replicas for read-heavy operations
   - Use connection string with read/write splitting

3. **Storage Scaling**:
   - Enable storage auto-scaling
   - Initial size: 100 GB
   - Maximum size: 500 GB
   - Scaling increment: 50 GB

## Caching Strategy

### ElastiCache Configuration

1. **Redis Cluster**:
   - Engine: Redis 6.x
   - Node Type: cache.m5.large
   - Number of Shards: 2
   - Replicas per Shard: 1
   - Multi-AZ: Enabled
   - Auto-failover: Enabled

2. **Cache Settings**:
   - TTL for opportunity data: 5 minutes
   - TTL for reference data: 1 hour
   - Maximum memory policy: volatile-lru

### Caching Patterns

1. **Cache-Aside Pattern**:
   - Check cache first
   - If miss, read from database and update cache
   - Used for opportunity details, problem statements, and skill requirements

2. **Write-Through Pattern**:
   - Update cache when database is updated
   - Used for frequently accessed data that changes often

3. **Cache Invalidation**:
   - Invalidate cache entries when data is modified
   - Use event-based invalidation for consistency

### Cached Data

1. **Opportunity Details**:
   - Cache key: `opportunity:{id}`
   - TTL: 5 minutes

2. **Problem Statements**:
   - Cache key: `problem_statement:{id}`
   - TTL: 5 minutes

3. **Skill Requirements**:
   - Cache key: `skill_requirements:{opportunity_id}`
   - TTL: 5 minutes

4. **Skills Catalog**:
   - Cache key: `skills_catalog`
   - TTL: 1 hour

5. **User Profiles**:
   - Cache key: `user:{id}`
   - TTL: 15 minutes

## File Storage Architecture

### S3 Configuration

1. **Buckets**:
   - `opportunity-attachments-{environment}`: For storing attachments
   - `opportunity-exports-{environment}`: For storing exported data

2. **Lifecycle Policies**:
   - Transition to Infrequent Access after 30 days
   - Transition to Glacier after 90 days
   - Expire objects after 7 years (GDPR compliance)

3. **Security**:
   - Server-side encryption with AWS KMS
   - Bucket policies to restrict access
   - Versioning enabled for audit purposes

4. **Access Pattern**:
   - Pre-signed URLs for secure, time-limited access
   - CloudFront distribution for fast content delivery

### File Upload Process

1. Client requests a pre-signed URL from the API
2. API generates a pre-signed URL with 15-minute expiration
3. Client uploads the file directly to S3 using the pre-signed URL
4. Client notifies the API that the upload is complete
5. API creates an Attachment record with the file metadata

## High Availability and Disaster Recovery

### High Availability Design

1. **Multi-AZ Deployment**:
   - ECS Fargate tasks across 3 AZs
   - RDS in Multi-AZ configuration
   - ElastiCache with replicas across AZs

2. **Load Balancing**:
   - Application Load Balancer across all AZs
   - Health checks to detect and replace unhealthy instances

3. **Auto-scaling**:
   - Automatic scaling based on demand
   - Minimum capacity to handle base load

### Disaster Recovery Strategy

1. **Backup Strategy**:
   - RDS automated backups (daily)
   - Database snapshots before major changes
   - S3 cross-region replication for attachments

2. **Recovery Time Objective (RTO)**:
   - 1 hour for critical components
   - 4 hours for full system

3. **Recovery Point Objective (RPO)**:
   - 15 minutes for database (using Point-in-Time Recovery)
   - 1 hour for attachments

4. **Disaster Recovery Plan**:
   - Regular testing of recovery procedures
   - Automated recovery scripts
   - Documentation of recovery processes

## Monitoring and Logging

### CloudWatch Configuration

1. **Metrics**:
   - ECS service metrics (CPU, memory, task count)
   - ALB metrics (request count, latency, error rates)
   - RDS metrics (CPU, memory, connections, IOPS)
   - ElastiCache metrics (CPU, memory, cache hits/misses)
   - Custom application metrics (business KPIs)

2. **Alarms**:
   - High CPU utilization (> 80% for 5 minutes)
   - High memory utilization (> 80% for 5 minutes)
   - High error rates (> 1% for 5 minutes)
   - High latency (> 500ms for 5 minutes)
   - Low free storage space (< 20% for 15 minutes)

3. **Dashboards**:
   - Service health dashboard
   - Performance dashboard
   - Business metrics dashboard

### Logging Strategy

1. **Log Types**:
   - Application logs
   - Access logs
   - Error logs
   - Audit logs

2. **Log Destinations**:
   - CloudWatch Logs
   - S3 for long-term storage

3. **Log Retention**:
   - 30 days in CloudWatch Logs
   - 7 years in S3 (for compliance)

4. **Log Analysis**:
   - CloudWatch Logs Insights for ad-hoc analysis
   - Scheduled queries for regular reporting

## Security Architecture

### Data Protection

1. **Encryption**:
   - Data at rest: AWS KMS encryption for RDS, S3, and ElastiCache
   - Data in transit: HTTPS/TLS 1.2+ for all communications

2. **Secrets Management**:
   - AWS Secrets Manager for database credentials
   - IAM roles for service-to-service authentication

3. **Data Classification**:
   - PII data identified and tagged
   - Access controls based on data classification

### Network Security

1. **Security Groups**:
   - Principle of least privilege
   - Allow only necessary traffic between components

2. **WAF Rules**:
   - OWASP Top 10 protection
   - Rate limiting rules
   - Geo-blocking for restricted regions

3. **DDoS Protection**:
   - AWS Shield Standard
   - CloudFront for edge protection

### Compliance Controls

1. **GDPR Compliance**:
   - Data encryption
   - Access controls
   - Audit logging
   - Data retention policies
   - Data subject request handling

2. **Security Scanning**:
   - Container vulnerability scanning
   - Dependency scanning
   - Static code analysis
   - Dynamic application security testing
