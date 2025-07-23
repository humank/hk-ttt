# Step 10: Deploy and Validate

This document outlines the deployment and validation process for the Opportunity Management Service.

## Deployment Strategy

We'll follow a staged deployment approach:

1. **Development Environment**: Initial deployment for development and testing
2. **Staging Environment**: Pre-production environment for final validation
3. **Production Environment**: Live environment for end users

## Deployment Process

### Development Environment Deployment

1. **Prepare Infrastructure**:
   ```bash
   # Navigate to infrastructure directory
   cd opportunity-management-service-infra

   # Deploy infrastructure with CDK
   cdk deploy --all --context env=dev
   ```

2. **Build and Push Docker Image**:
   ```bash
   # Build Docker image
   docker build -t opportunity-management-service:dev .

   # Tag image for ECR
   docker tag opportunity-management-service:dev ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/opportunity-management-service:dev

   # Login to ECR
   aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

   # Push image to ECR
   docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/opportunity-management-service:dev
   ```

3. **Deploy Application**:
   ```bash
   # Update ECS service to use the new image
   aws ecs update-service \
     --cluster opportunity-management-service-dev \
     --service opportunity-management-service \
     --force-new-deployment
   ```

4. **Run Database Migrations**:
   ```bash
   # Run database migrations
   python -m opportunity_management_service.adapters.db_migrations
   ```

5. **Verify Deployment**:
   ```bash
   # Check ECS service status
   aws ecs describe-services \
     --cluster opportunity-management-service-dev \
     --services opportunity-management-service

   # Check API health
   curl https://dev-api.example.com/health
   ```

### Staging Environment Deployment

1. **Prepare Infrastructure**:
   ```bash
   # Navigate to infrastructure directory
   cd opportunity-management-service-infra

   # Deploy infrastructure with CDK
   cdk deploy --all --context env=staging
   ```

2. **Build and Push Docker Image**:
   ```bash
   # Build Docker image
   docker build -t opportunity-management-service:staging .

   # Tag image for ECR
   docker tag opportunity-management-service:staging ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/opportunity-management-service:staging

   # Login to ECR
   aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

   # Push image to ECR
   docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/opportunity-management-service:staging
   ```

3. **Deploy Application**:
   ```bash
   # Update ECS service to use the new image
   aws ecs update-service \
     --cluster opportunity-management-service-staging \
     --service opportunity-management-service \
     --force-new-deployment
   ```

4. **Run Database Migrations**:
   ```bash
   # Run database migrations
   python -m opportunity_management_service.adapters.db_migrations
   ```

5. **Verify Deployment**:
   ```bash
   # Check ECS service status
   aws ecs describe-services \
     --cluster opportunity-management-service-staging \
     --services opportunity-management-service

   # Check API health
   curl https://staging-api.example.com/health
   ```

### Production Environment Deployment

1. **Prepare Infrastructure**:
   ```bash
   # Navigate to infrastructure directory
   cd opportunity-management-service-infra

   # Deploy infrastructure with CDK
   cdk deploy --all --context env=prod
   ```

2. **Build and Push Docker Image**:
   ```bash
   # Build Docker image
   docker build -t opportunity-management-service:prod .

   # Tag image for ECR
   docker tag opportunity-management-service:prod ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/opportunity-management-service:prod

   # Login to ECR
   aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

   # Push image to ECR
   docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/opportunity-management-service:prod
   ```

3. **Deploy Application**:
   ```bash
   # Update ECS service to use the new image
   aws ecs update-service \
     --cluster opportunity-management-service-prod \
     --service opportunity-management-service \
     --force-new-deployment
   ```

4. **Run Database Migrations**:
   ```bash
   # Run database migrations
   python -m opportunity_management_service.adapters.db_migrations
   ```

5. **Verify Deployment**:
   ```bash
   # Check ECS service status
   aws ecs describe-services \
     --cluster opportunity-management-service-prod \
     --services opportunity-management-service

   # Check API health
   curl https://api.example.com/health
   ```

## Validation Procedures

### Functional Validation

1. **API Health Check**:
   ```bash
   # Check API health
   curl https://api.example.com/health

   # Check detailed health
   curl https://api.example.com/health/detailed
   ```

2. **Authentication Validation**:
   ```bash
   # Get authentication token
   TOKEN=$(curl -X POST https://auth.example.com/oauth2/token \
     -d "grant_type=client_credentials&client_id=${CLIENT_ID}&client_secret=${CLIENT_SECRET}" \
     | jq -r '.access_token')

   # Verify token works
   curl -H "Authorization: Bearer ${TOKEN}" https://api.example.com/api/v1/opportunities
   ```

3. **CRUD Operations Validation**:
   ```bash
   # Create opportunity
   OPPORTUNITY_ID=$(curl -X POST https://api.example.com/api/v1/opportunities \
     -H "Authorization: Bearer ${TOKEN}" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Test Opportunity",
       "description": "Test Description",
       "client_name": "Test Client",
       "estimated_budget": 10000.0,
       "estimated_start_date": "2023-01-01T00:00:00Z",
       "estimated_end_date": "2023-12-31T00:00:00Z",
       "status": "DRAFT"
     }' | jq -r '.id')

   # Get opportunity
   curl -H "Authorization: Bearer ${TOKEN}" https://api.example.com/api/v1/opportunities/${OPPORTUNITY_ID}

   # Update opportunity
   curl -X PUT https://api.example.com/api/v1/opportunities/${OPPORTUNITY_ID} \
     -H "Authorization: Bearer ${TOKEN}" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Updated Opportunity"
     }'

   # Change status
   curl -X POST https://api.example.com/api/v1/opportunities/${OPPORTUNITY_ID}/status \
     -H "Authorization: Bearer ${TOKEN}" \
     -H "Content-Type: application/json" \
     -d '{
       "new_status": "SUBMITTED",
       "reason": "Ready for review"
     }'

   # Delete opportunity
   curl -X DELETE https://api.example.com/api/v1/opportunities/${OPPORTUNITY_ID} \
     -H "Authorization: Bearer ${TOKEN}"
   ```

### Performance Validation

1. **Latency Testing**:
   ```bash
   # Install hey load testing tool
   go get -u github.com/rakyll/hey

   # Run load test
   hey -n 1000 -c 50 -H "Authorization: Bearer ${TOKEN}" https://api.example.com/api/v1/opportunities
   ```

2. **Throughput Testing**:
   ```bash
   # Run throughput test
   hey -n 10000 -c 100 -H "Authorization: Bearer ${TOKEN}" https://api.example.com/api/v1/opportunities
   ```

3. **Scalability Testing**:
   ```bash
   # Run scalability test with increasing load
   for i in {1..5}; do
     hey -n $((1000 * $i)) -c $((50 * $i)) -H "Authorization: Bearer ${TOKEN}" https://api.example.com/api/v1/opportunities
     sleep 60
   done
   ```

### Security Validation

1. **SSL/TLS Configuration**:
   ```bash
   # Check SSL/TLS configuration
   nmap --script ssl-enum-ciphers -p 443 api.example.com
   ```

2. **Authentication and Authorization**:
   ```bash
   # Try accessing without token
   curl https://api.example.com/api/v1/opportunities

   # Try accessing with invalid token
   curl -H "Authorization: Bearer invalid_token" https://api.example.com/api/v1/opportunities

   # Try accessing with insufficient permissions
   # (Using a token for a user without proper role)
   curl -H "Authorization: Bearer ${LIMITED_TOKEN}" https://api.example.com/api/v1/opportunities
   ```

3. **API Security Scanning**:
   ```bash
   # Run OWASP ZAP scan
   docker run --rm -v $(pwd)/zap-report:/zap/wrk/ owasp/zap2docker-stable zap-baseline.py \
     -t https://api.example.com/ \
     -r zap-report.html
   ```

### Monitoring Validation

1. **CloudWatch Alarms**:
   ```bash
   # List CloudWatch alarms
   aws cloudwatch describe-alarms \
     --alarm-name-prefix opportunity-management-service
   ```

2. **CloudWatch Logs**:
   ```bash
   # Check CloudWatch logs
   aws logs get-log-events \
     --log-group-name /aws/ecs/opportunity-management-service \
     --log-stream-name $(aws logs describe-log-streams \
       --log-group-name /aws/ecs/opportunity-management-service \
       --order-by LastEventTime \
       --descending \
       --limit 1 \
       --query 'logStreams[0].logStreamName' \
       --output text)
   ```

3. **CloudWatch Dashboard**:
   ```bash
   # Get CloudWatch dashboard URL
   aws cloudwatch get-dashboard \
     --dashboard-name OpportunityManagementService
   ```

## Rollback Procedures

In case of deployment issues, follow these rollback procedures:

### Application Rollback

1. **Rollback ECS Service**:
   ```bash
   # Get previous task definition
   PREVIOUS_TASK_DEF=$(aws ecs describe-task-definition \
     --task-definition opportunity-management-service \
     --query 'taskDefinition.taskDefinitionArn' \
     --output text)

   # Rollback to previous task definition
   aws ecs update-service \
     --cluster opportunity-management-service-prod \
     --service opportunity-management-service \
     --task-definition ${PREVIOUS_TASK_DEF} \
     --force-new-deployment
   ```

2. **Verify Rollback**:
   ```bash
   # Check ECS service status
   aws ecs describe-services \
     --cluster opportunity-management-service-prod \
     --services opportunity-management-service

   # Check API health
   curl https://api.example.com/health
   ```

### Database Rollback

1. **Restore Database**:
   ```bash
   # Get latest snapshot
   SNAPSHOT_ID=$(aws rds describe-db-snapshots \
     --db-instance-identifier opportunity-management-service \
     --query 'sort_by(DBSnapshots, &SnapshotCreateTime)[-1].DBSnapshotIdentifier' \
     --output text)

   # Restore database from snapshot
   aws rds restore-db-instance-from-db-snapshot \
     --db-instance-identifier opportunity-management-service-restored \
     --db-snapshot-identifier ${SNAPSHOT_ID}
   ```

2. **Update Connection String**:
   ```bash
   # Update ECS task definition with new connection string
   aws ecs update-service \
     --cluster opportunity-management-service-prod \
     --service opportunity-management-service \
     --force-new-deployment
   ```

### Infrastructure Rollback

1. **Rollback CDK Deployment**:
   ```bash
   # Rollback to previous CloudFormation stack version
   aws cloudformation rollback-stack \
     --stack-name opportunity-management-service-prod
   ```

2. **Verify Infrastructure**:
   ```bash
   # Check CloudFormation stack status
   aws cloudformation describe-stacks \
     --stack-name opportunity-management-service-prod
   ```

## Post-Deployment Tasks

1. **Update Documentation**:
   - Update API documentation
   - Update deployment documentation
   - Update runbooks

2. **Notify Stakeholders**:
   - Send deployment notification to stakeholders
   - Provide release notes

3. **Monitor System**:
   - Monitor CloudWatch metrics
   - Monitor CloudWatch logs
   - Monitor CloudWatch alarms

4. **Conduct Post-Deployment Review**:
   - Review deployment process
   - Identify areas for improvement
   - Update deployment procedures

## Conclusion

The deployment and validation process ensures that the Opportunity Management Service is deployed reliably and functions correctly in production. By following these procedures, we can minimize deployment risks and ensure a smooth transition to production.
