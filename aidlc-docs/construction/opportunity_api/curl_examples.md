# API Testing with cURL Examples

This document provides comprehensive cURL examples for testing all API endpoints.

## Health Check

```bash
curl -X GET "http://localhost:8000/health"
```

## Opportunity Management

### 1. Create Opportunity

```bash
curl -X POST "http://localhost:8000/api/v1/opportunities" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "E-commerce Platform Development",
    "customer_id": "123e4567-e89b-12d3-a456-426614174000",
    "customer_name": "TechCorp Solutions",
    "sales_manager_id": "123e4567-e89b-12d3-a456-426614174001",
    "description": "Need to build a modern e-commerce platform with mobile responsiveness and payment integration",
    "priority": "HIGH",
    "annual_recurring_revenue": 250000.0,
    "geographic_requirements": {
      "region_id": "123e4567-e89b-12d3-a456-426614174002",
      "name": "North America",
      "requires_physical_presence": false,
      "allows_remote_work": true
    }
  }'
```

### 2. Search Opportunities

```bash
# Search all opportunities
curl -X GET "http://localhost:8000/api/v1/opportunities"

# Search with filters
curl -X GET "http://localhost:8000/api/v1/opportunities?status=DRAFT&priority=HIGH&page=1&page_size=10"

# Search by query
curl -X GET "http://localhost:8000/api/v1/opportunities?query=e-commerce"

# Search by sales manager
curl -X GET "http://localhost:8000/api/v1/opportunities?sales_manager_id=123e4567-e89b-12d3-a456-426614174001"
```

### 3. Get Opportunity Details

```bash
# Replace {opportunity_id} with actual ID from create response
curl -X GET "http://localhost:8000/api/v1/opportunities/{opportunity_id}"
```

### 4. Add Problem Statement

```bash
curl -X POST "http://localhost:8000/api/v1/opportunities/{opportunity_id}/problem-statement" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Our current e-commerce system is outdated and cannot handle the increasing traffic. We need a scalable solution that can support 10,000+ concurrent users, integrate with multiple payment gateways, and provide real-time inventory management. The system should also support mobile commerce and have advanced analytics capabilities for business intelligence."
  }'
```

### 5. Add Skill Requirements

```bash
# Add Python skill requirement
curl -X POST "http://localhost:8000/api/v1/opportunities/{opportunity_id}/skill-requirements" \
  -H "Content-Type: application/json" \
  -d '{
    "skill_id": "123e4567-e89b-12d3-a456-426614174010",
    "skill_type": "TECHNICAL",
    "importance_level": "MUST_HAVE",
    "minimum_proficiency_level": "ADVANCED"
  }'

# Add React skill requirement
curl -X POST "http://localhost:8000/api/v1/opportunities/{opportunity_id}/skill-requirements" \
  -H "Content-Type: application/json" \
  -d '{
    "skill_id": "123e4567-e89b-12d3-a456-426614174011",
    "skill_type": "TECHNICAL",
    "importance_level": "MUST_HAVE",
    "minimum_proficiency_level": "INTERMEDIATE"
  }'

# Add Project Management skill requirement
curl -X POST "http://localhost:8000/api/v1/opportunities/{opportunity_id}/skill-requirements" \
  -H "Content-Type: application/json" \
  -d '{
    "skill_id": "123e4567-e89b-12d3-a456-426614174012",
    "skill_type": "SOFT",
    "importance_level": "PREFERRED",
    "minimum_proficiency_level": "INTERMEDIATE"
  }'
```

### 6. Add Timeline Requirement

```bash
curl -X POST "http://localhost:8000/api/v1/opportunities/{opportunity_id}/timeline-requirement" \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2025-08-01",
    "end_date": "2025-12-31",
    "is_flexible": true,
    "specific_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
  }'
```

### 7. Submit Opportunity

```bash
curl -X POST "http://localhost:8000/api/v1/opportunities/{opportunity_id}/submit" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "123e4567-e89b-12d3-a456-426614174001"
  }'
```

### 8. Cancel Opportunity

```bash
curl -X POST "http://localhost:8000/api/v1/opportunities/{opportunity_id}/cancel" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "123e4567-e89b-12d3-a456-426614174001",
    "reason": "Client decided to postpone the project due to budget constraints"
  }'
```

### 9. Reactivate Opportunity

```bash
curl -X POST "http://localhost:8000/api/v1/opportunities/{opportunity_id}/reactivate" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "123e4567-e89b-12d3-a456-426614174001"
  }'
```

## Attachment Management

### 1. Upload Attachment

```bash
# Create a test file first
echo "This is a test document for the e-commerce project requirements." > test_document.txt

# Upload the file
curl -X POST "http://localhost:8000/api/v1/problem-statements/{problem_statement_id}/attachments" \
  -F "file=@test_document.txt" \
  -F "uploaded_by=123e4567-e89b-12d3-a456-426614174001"

# Upload a larger file (create a sample PDF-like file)
echo "Sample PDF content for project specifications and wireframes" > project_specs.pdf
curl -X POST "http://localhost:8000/api/v1/problem-statements/{problem_statement_id}/attachments" \
  -F "file=@project_specs.pdf" \
  -F "uploaded_by=123e4567-e89b-12d3-a456-426614174001"
```

### 2. Get Attachments for Problem Statement

```bash
curl -X GET "http://localhost:8000/api/v1/problem-statements/{problem_statement_id}/attachments"
```

### 3. Download Attachment

```bash
# Download and save to file
curl -X GET "http://localhost:8000/api/v1/attachments/{attachment_id}/download" \
  -o downloaded_file.txt

# Download and display content
curl -X GET "http://localhost:8000/api/v1/attachments/{attachment_id}/download"
```

### 4. Remove Attachment

```bash
curl -X DELETE "http://localhost:8000/api/v1/attachments/{attachment_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "123e4567-e89b-12d3-a456-426614174001"
  }'
```

## Complete Workflow Example

Here's a complete workflow that creates an opportunity and takes it through the full lifecycle:

```bash
#!/bin/bash

# Set base URL
BASE_URL="http://localhost:8000/api/v1"

echo "=== Creating Opportunity ==="
OPPORTUNITY_RESPONSE=$(curl -s -X POST "$BASE_URL/opportunities" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mobile Banking App Development",
    "customer_id": "123e4567-e89b-12d3-a456-426614174000",
    "customer_name": "SecureBank Inc",
    "sales_manager_id": "123e4567-e89b-12d3-a456-426614174001",
    "description": "Develop a secure mobile banking application with biometric authentication",
    "priority": "CRITICAL",
    "annual_recurring_revenue": 500000.0,
    "geographic_requirements": {
      "region_id": "123e4567-e89b-12d3-a456-426614174002",
      "name": "Global",
      "requires_physical_presence": false,
      "allows_remote_work": true
    }
  }')

# Extract opportunity ID (you might need jq for this)
OPPORTUNITY_ID=$(echo $OPPORTUNITY_RESPONSE | grep -o '"id":"[^"]*' | cut -d'"' -f4)
echo "Created opportunity: $OPPORTUNITY_ID"

echo "=== Adding Problem Statement ==="
PROBLEM_RESPONSE=$(curl -s -X POST "$BASE_URL/opportunities/$OPPORTUNITY_ID/problem-statement" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "We need to develop a cutting-edge mobile banking application that provides secure, user-friendly access to banking services. The app must support biometric authentication, real-time transaction processing, account management, bill payments, and fund transfers. Security is paramount as we handle sensitive financial data. The application should work seamlessly on both iOS and Android platforms and integrate with our existing core banking system."
  }')

PROBLEM_ID=$(echo $PROBLEM_RESPONSE | grep -o '"id":"[^"]*' | cut -d'"' -f4)
echo "Created problem statement: $PROBLEM_ID"

echo "=== Adding Skill Requirements ==="
# iOS Development
curl -s -X POST "$BASE_URL/opportunities/$OPPORTUNITY_ID/skill-requirements" \
  -H "Content-Type: application/json" \
  -d '{
    "skill_id": "123e4567-e89b-12d3-a456-426614174020",
    "skill_type": "TECHNICAL",
    "importance_level": "MUST_HAVE",
    "minimum_proficiency_level": "EXPERT"
  }'

# Android Development
curl -s -X POST "$BASE_URL/opportunities/$OPPORTUNITY_ID/skill-requirements" \
  -H "Content-Type: application/json" \
  -d '{
    "skill_id": "123e4567-e89b-12d3-a456-426614174021",
    "skill_type": "TECHNICAL",
    "importance_level": "MUST_HAVE",
    "minimum_proficiency_level": "EXPERT"
  }'

# Security
curl -s -X POST "$BASE_URL/opportunities/$OPPORTUNITY_ID/skill-requirements" \
  -H "Content-Type: application/json" \
  -d '{
    "skill_id": "123e4567-e89b-12d3-a456-426614174022",
    "skill_type": "TECHNICAL",
    "importance_level": "MUST_HAVE",
    "minimum_proficiency_level": "ADVANCED"
  }'

echo "Added skill requirements"

echo "=== Adding Timeline Requirement ==="
curl -s -X POST "$BASE_URL/opportunities/$OPPORTUNITY_ID/timeline-requirement" \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2025-09-01",
    "end_date": "2026-03-31",
    "is_flexible": false,
    "specific_days": null
  }'

echo "Added timeline requirement"

echo "=== Adding Attachment ==="
echo "Mobile Banking App Requirements and Specifications" > banking_requirements.txt
curl -s -X POST "$BASE_URL/problem-statements/$PROBLEM_ID/attachments" \
  -F "file=@banking_requirements.txt" \
  -F "uploaded_by=123e4567-e89b-12d3-a456-426614174001"

echo "Added attachment"

echo "=== Getting Opportunity Details ==="
curl -s -X GET "$BASE_URL/opportunities/$OPPORTUNITY_ID" | python -m json.tool

echo "=== Submitting Opportunity ==="
curl -s -X POST "$BASE_URL/opportunities/$OPPORTUNITY_ID/submit" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "123e4567-e89b-12d3-a456-426614174001"
  }'

echo "Opportunity submitted successfully!"

# Clean up
rm -f banking_requirements.txt
```

## Error Testing Examples

### Test Validation Errors

```bash
# Missing required fields
curl -X POST "http://localhost:8000/api/v1/opportunities" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "",
    "description": "Test"
  }'

# Invalid UUID format
curl -X GET "http://localhost:8000/api/v1/opportunities/invalid-uuid"

# Problem statement too short
curl -X POST "http://localhost:8000/api/v1/opportunities/{opportunity_id}/problem-statement" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Too short"
  }'
```

### Test Business Logic Errors

```bash
# Try to submit opportunity without requirements
curl -X POST "http://localhost:8000/api/v1/opportunities/{opportunity_id}/submit" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "123e4567-e89b-12d3-a456-426614174001"
  }'

# Try to add problem statement to submitted opportunity
curl -X POST "http://localhost:8000/api/v1/opportunities/{submitted_opportunity_id}/problem-statement" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "This should fail because opportunity is already submitted"
  }'
```

## Rate Limiting Test

```bash
# Test rate limiting (run this multiple times quickly)
for i in {1..10}; do
  curl -X GET "http://localhost:8000/health"
  echo "Request $i completed"
done
```

## File Upload Size Test

```bash
# Create a large file (adjust size as needed)
dd if=/dev/zero of=large_file.bin bs=1M count=25

# Try to upload (should fail if over 20MB limit)
curl -X POST "http://localhost:8000/api/v1/problem-statements/{problem_statement_id}/attachments" \
  -F "file=@large_file.bin" \
  -F "uploaded_by=123e4567-e89b-12d3-a456-426614174001"

# Clean up
rm -f large_file.bin
```

## Notes

1. Replace `{opportunity_id}`, `{problem_statement_id}`, and `{attachment_id}` with actual IDs from API responses
2. For JSON parsing, you can pipe responses to `python -m json.tool` or use `jq` if available
3. All examples use localhost:8000 - adjust the URL for your deployment
4. The API returns detailed error messages for debugging
5. Check response headers for rate limiting information and request IDs
