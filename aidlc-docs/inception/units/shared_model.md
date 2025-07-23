# Shared Data Models

This document defines the component models for the core entities in the Solution Architect Matching System. Each component model includes attributes with data types and sample data.

## 1. User Component Model

The User component represents basic user information across the system.

### Attributes

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| id | UUID | Unique identifier for the user | Yes |
| name | String | Full name of the user | Yes |
| email | String | Email address (used for login) | Yes |
| role | Enum | User role in the system (SA, SalesManager, Admin) | Yes |
| employeeId | String | Company employee ID | Yes |
| department | String | Department or business unit | Yes |
| jobTitle | String | Official job title | Yes |
| isActive | Boolean | Whether the user account is active | Yes |
| createdAt | DateTime | When the user account was created | Yes |
| lastLoginAt | DateTime | When the user last logged in | No |
| profilePictureUrl | String | URL to profile picture | No |
| phoneNumber | String | Contact phone number | No |

### Sample Data

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Jane Smith",
  "email": "jane.smith@company.com",
  "role": "SolutionArchitect",
  "employeeId": "EMP12345",
  "department": "Cloud Solutions",
  "jobTitle": "Senior Solution Architect",
  "isActive": true,
  "createdAt": "2025-01-15T08:30:00Z",
  "lastLoginAt": "2025-07-21T14:22:10Z",
  "profilePictureUrl": "https://company.com/profiles/jsmith.jpg",
  "phoneNumber": "+1-555-123-4567"
}
```

## 2. Solution Architect Profile Component Model

The Solution Architect Profile component extends the User model with detailed information about a Solution Architect's skills, availability, and preferences.

### Attributes

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| id | UUID | Unique identifier for the profile | Yes |
| userId | UUID | Reference to the User entity | Yes |
| yearsOfExperience | Integer | Total years of professional experience | Yes |
| biography | String | Professional summary/bio | No |
| technicalSkills | Array of Skill | Technical skills with proficiency levels | Yes |
| softSkills | Array of Skill | Soft skills with proficiency levels | No |
| industryKnowledge | Array of Industry | Industries with years of experience | No |
| languages | Array of Language | Languages with proficiency levels | No |
| geographicExpertise | Array of Region | Regions of expertise | No |
| travelPreferences | Object | Travel willingness and restrictions | No |
| remoteWorkCapability | Boolean | Whether SA can work remotely | Yes |
| availability | Array of DateRange | Calendar of available dates | Yes |
| certifications | Array of Certification | Professional certifications | No |
| previousAssignments | Array of UUID | References to previous assignments | No |
| averageRating | Decimal | Average rating from previous assignments | No |
| lastUpdated | DateTime | When the profile was last updated | Yes |

### Skill Object

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| skillId | UUID | Reference to Skills Catalog | Yes |
| name | String | Name of the skill | Yes |
| proficiencyLevel | Enum | Beginner, Intermediate, Advanced, Expert | Yes |
| yearsOfExperience | Integer | Years of experience with this skill | Yes |
| isCustom | Boolean | Whether this is a custom skill not in catalog | No |

### Industry Object

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| industryId | UUID | Reference to industry catalog | Yes |
| name | String | Name of the industry | Yes |
| yearsOfExperience | Integer | Years of experience in this industry | Yes |
| specificDomains | Array of String | Specific domains within industry | No |

### Language Object

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| languageId | UUID | Reference to language catalog | Yes |
| name | String | Name of the language | Yes |
| proficiencyLevel | Enum | Basic, Conversational, Fluent, Native | Yes |

### Region Object

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| regionId | UUID | Reference to region catalog | Yes |
| name | String | Name of the region/country | Yes |
| isWillingToTravel | Boolean | Whether SA is willing to travel here | Yes |

### DateRange Object

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| startDate | Date | Start date of availability | Yes |
| endDate | Date | End date of availability | Yes |
| isRecurring | Boolean | Whether this is a recurring pattern | No |
| recurringPattern | String | Description of recurring pattern | No |

### Certification Object

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| name | String | Name of certification | Yes |
| issuingOrganization | String | Organization that issued certification | Yes |
| issueDate | Date | When certification was issued | Yes |
| expirationDate | Date | When certification expires | No |
| verificationUrl | String | URL to verify certification | No |

### Sample Data

```json
{
  "id": "7a1b9c36-e29b-41d4-a716-446655440123",
  "userId": "550e8400-e29b-41d4-a716-446655440000",
  "yearsOfExperience": 8,
  "biography": "Experienced Solution Architect with focus on cloud migration and serverless architectures.",
  "technicalSkills": [
    {
      "skillId": "a1b2c3d4-e5f6-4a5b-8c7d-9e0f1a2b3c4d",
      "name": "AWS Lambda",
      "proficiencyLevel": "Expert",
      "yearsOfExperience": 5,
      "isCustom": false
    },
    {
      "skillId": "b2c3d4e5-f6a7-5b6c-9d0e-1f2a3b4c5d6e",
      "name": "Terraform",
      "proficiencyLevel": "Advanced",
      "yearsOfExperience": 3,
      "isCustom": false
    }
  ],
  "softSkills": [
    {
      "skillId": "c3d4e5f6-a7b8-6c7d-0e1f-2a3b4c5d6e7f",
      "name": "Public Speaking",
      "proficiencyLevel": "Advanced",
      "yearsOfExperience": 6,
      "isCustom": false
    }
  ],
  "industryKnowledge": [
    {
      "industryId": "d4e5f6a7-b8c9-7d0e-1f2a-3b4c5d6e7f8a",
      "name": "Financial Services",
      "yearsOfExperience": 4,
      "specificDomains": ["Retail Banking", "Payment Processing"]
    }
  ],
  "languages": [
    {
      "languageId": "e5f6a7b8-c9d0-8e1f-2a3b-4c5d6e7f8a9b",
      "name": "English",
      "proficiencyLevel": "Native"
    },
    {
      "languageId": "f6a7b8c9-d0e1-9f2a-3b4c-5d6e7f8a9b0c",
      "name": "Spanish",
      "proficiencyLevel": "Conversational"
    }
  ],
  "geographicExpertise": [
    {
      "regionId": "a7b8c9d0-e1f2-0a3b-4c5d-6e7f8a9b0c1d",
      "name": "North America",
      "isWillingToTravel": true
    }
  ],
  "travelPreferences": {
    "maxTravelDays": 5,
    "preferredTransportation": "Air",
    "travelRestrictions": "No international travel"
  },
  "remoteWorkCapability": true,
  "availability": [
    {
      "startDate": "2025-08-01",
      "endDate": "2025-08-15",
      "isRecurring": false
    },
    {
      "startDate": "2025-09-01",
      "endDate": "2025-12-31",
      "isRecurring": true,
      "recurringPattern": "Every Monday and Wednesday"
    }
  ],
  "certifications": [
    {
      "name": "AWS Certified Solutions Architect - Professional",
      "issuingOrganization": "Amazon Web Services",
      "issueDate": "2023-05-15",
      "expirationDate": "2026-05-15",
      "verificationUrl": "https://aws.amazon.com/verification/12345"
    }
  ],
  "previousAssignments": [
    "b8c9d0e1-f2a3-1b4c-5d6e-7f8a9b0c1d2e",
    "c9d0e1f2-a3b4-2c5d-6e7f-8a9b0c1d2e3f"
  ],
  "averageRating": 4.8,
  "lastUpdated": "2025-07-10T09:15:30Z"
}
```

## 3. Opportunity Component Model

The Opportunity component represents a customer opportunity that requires a Solution Architect.

### Attributes

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| id | UUID | Unique identifier for the opportunity | Yes |
| title | String | Title of the opportunity | Yes |
| customerId | UUID | Reference to the customer | Yes |
| customerName | String | Name of the customer | Yes |
| salesManagerId | UUID | Reference to the Sales Manager who created it | Yes |
| description | String | General description of the opportunity | Yes |
| problemStatement | String | Detailed problem statement | Yes |
| priority | Enum | Priority level (Low, Medium, High, Critical) | Yes |
| status | Enum | Current status (Draft, Submitted, Matching, MatchesFound, ArchitectSelected, Completed, Cancelled) | Yes |
| annualRecurringRevenue | Decimal | Expected ARR from the opportunity | No |
| requiredTechnicalSkills | Array of RequiredSkill | Technical skills needed | Yes |
| requiredSoftSkills | Array of RequiredSkill | Soft skills needed | No |
| requiredIndustryKnowledge | Array of RequiredIndustry | Industry knowledge needed | No |
| requiredLanguages | Array of RequiredLanguage | Languages needed | No |
| geographicRequirements | Object | Geographic location requirements | Yes |
| timeline | Object | Timeline requirements | Yes |
| attachments | Array of Attachment | Related documents | No |
| createdAt | DateTime | When the opportunity was created | Yes |
| updatedAt | DateTime | When the opportunity was last updated | Yes |
| submittedAt | DateTime | When the opportunity was submitted for matching | No |
| completedAt | DateTime | When the opportunity was completed | No |
| changeHistory | Array of ChangeRecord | History of changes | Yes |

### RequiredSkill Object

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| skillId | UUID | Reference to Skills Catalog | Yes |
| name | String | Name of the skill | Yes |
| importanceLevel | Enum | Must Have, Nice to Have | Yes |
| minimumProficiencyLevel | Enum | Beginner, Intermediate, Advanced, Expert | Yes |
| isCustom | Boolean | Whether this is a custom skill not in catalog | No |

### RequiredIndustry Object

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| industryId | UUID | Reference to industry catalog | Yes |
| name | String | Name of the industry | Yes |
| importanceLevel | Enum | Must Have, Nice to Have | Yes |
| specificDomains | Array of String | Specific domains within industry | No |

### RequiredLanguage Object

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| languageId | UUID | Reference to language catalog | Yes |
| name | String | Name of the language | Yes |
| importanceLevel | Enum | Must Have, Nice to Have | Yes |
| minimumProficiencyLevel | Enum | Basic, Conversational, Fluent, Native | Yes |

### GeographicRequirements Object

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| regionId | UUID | Reference to region catalog | Yes |
| name | String | Name of the region/country | Yes |
| requiresPhysicalPresence | Boolean | Whether physical presence is required | Yes |
| allowsRemoteWork | Boolean | Whether remote work is allowed | Yes |

### Timeline Object

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| expectedStartDate | Date | Expected start date | Yes |
| expectedEndDate | Date | Expected end date | No |
| expectedDurationDays | Integer | Expected duration in days | Yes |
| specificRequiredDays | Array of Date | Specific days when SA is needed | No |
| isFlexible | Boolean | Whether the timeline is flexible | Yes |

### Attachment Object

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| id | UUID | Unique identifier for the attachment | Yes |
| fileName | String | Name of the file | Yes |
| fileType | String | MIME type of the file | Yes |
| fileSize | Integer | Size of the file in bytes | Yes |
| uploadedAt | DateTime | When the file was uploaded | Yes |
| uploadedBy | UUID | Reference to the user who uploaded it | Yes |
| fileUrl | String | URL to access the file | Yes |

### ChangeRecord Object

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| changedAt | DateTime | When the change was made | Yes |
| changedBy | UUID | Reference to the user who made the change | Yes |
| fieldChanged | String | Name of the field that was changed | Yes |
| oldValue | String | Previous value | No |
| newValue | String | New value | No |
| reason | String | Reason for the change | No |

### Sample Data

```json
{
  "id": "d1e2f3a4-b5c6-7d8e-9f0a-1b2c3d4e5f6a",
  "title": "Cloud Migration Strategy for FinTech Platform",
  "customerId": "e2f3a4b5-c6d7-8e9f-0a1b-2c3d4e5f6a7b",
  "customerName": "Global Finance Tech Inc.",
  "salesManagerId": "f3a4b5c6-d7e8-9f0a-1b2c-3d4e5f6a7b8c",
  "description": "Customer needs a comprehensive cloud migration strategy for their financial platform.",
  "problemStatement": "Global Finance Tech Inc. is looking to migrate their legacy financial platform to the cloud. The platform processes over 1 million transactions daily and requires high availability and security. They need a comprehensive migration strategy that minimizes downtime and ensures compliance with financial regulations.",
  "priority": "High",
  "status": "Submitted",
  "annualRecurringRevenue": 750000.00,
  "requiredTechnicalSkills": [
    {
      "skillId": "a1b2c3d4-e5f6-4a5b-8c7d-9e0f1a2b3c4d",
      "name": "AWS Migration",
      "importanceLevel": "Must Have",
      "minimumProficiencyLevel": "Advanced",
      "isCustom": false
    },
    {
      "skillId": "b2c3d4e5-f6a7-5b6c-9d0e-1f2a3b4c5d6e",
      "name": "Financial Services Cloud Architecture",
      "importanceLevel": "Must Have",
      "minimumProficiencyLevel": "Expert",
      "isCustom": false
    },
    {
      "skillId": "c3d4e5f6-a7b8-6c7d-0e1f-2a3b4c5d6e7f",
      "name": "Database Migration",
      "importanceLevel": "Nice to Have",
      "minimumProficiencyLevel": "Intermediate",
      "isCustom": false
    }
  ],
  "requiredSoftSkills": [
    {
      "skillId": "d4e5f6a7-b8c9-7d0e-1f2a-3b4c5d6e7f8a",
      "name": "Executive Presentation",
      "importanceLevel": "Must Have",
      "minimumProficiencyLevel": "Advanced",
      "isCustom": false
    }
  ],
  "requiredIndustryKnowledge": [
    {
      "industryId": "e5f6a7b8-c9d0-8e1f-2a3b-4c5d6e7f8a9b",
      "name": "Financial Services",
      "importanceLevel": "Must Have",
      "specificDomains": ["Banking", "Payment Processing"]
    }
  ],
  "requiredLanguages": [
    {
      "languageId": "f6a7b8c9-d0e1-9f2a-3b4c-5d6e7f8a9b0c",
      "name": "English",
      "importanceLevel": "Must Have",
      "minimumProficiencyLevel": "Fluent"
    }
  ],
  "geographicRequirements": {
    "regionId": "a7b8c9d0-e1f2-0a3b-4c5d-6e7f8a9b0c1d",
    "name": "North America - East Coast",
    "requiresPhysicalPresence": true,
    "allowsRemoteWork": true
  },
  "timeline": {
    "expectedStartDate": "2025-09-01",
    "expectedEndDate": "2025-12-15",
    "expectedDurationDays": 75,
    "specificRequiredDays": [
      "2025-09-01",
      "2025-09-15",
      "2025-10-01",
      "2025-11-01",
      "2025-12-15"
    ],
    "isFlexible": false
  },
  "attachments": [
    {
      "id": "b8c9d0e1-f2a3-1b4c-5d6e-7f8a9b0c1d2e",
      "fileName": "Current Architecture Diagram.pdf",
      "fileType": "application/pdf",
      "fileSize": 2458621,
      "uploadedAt": "2025-07-15T10:30:00Z",
      "uploadedBy": "f3a4b5c6-d7e8-9f0a-1b2c-3d4e5f6a7b8c",
      "fileUrl": "https://company.com/files/architecture-diagram.pdf"
    }
  ],
  "createdAt": "2025-07-15T09:45:00Z",
  "updatedAt": "2025-07-15T14:20:00Z",
  "submittedAt": "2025-07-15T14:20:00Z",
  "completedAt": null,
  "changeHistory": [
    {
      "changedAt": "2025-07-15T10:30:00Z",
      "changedBy": "f3a4b5c6-d7e8-9f0a-1b2c-3d4e5f6a7b8c",
      "fieldChanged": "attachments",
      "oldValue": "[]",
      "newValue": "[{\"id\":\"b8c9d0e1-f2a3-1b4c-5d6e-7f8a9b0c1d2e\",\"fileName\":\"Current Architecture Diagram.pdf\"}]",
      "reason": "Added architecture diagram from customer"
    },
    {
      "changedAt": "2025-07-15T14:20:00Z",
      "changedBy": "f3a4b5c6-d7e8-9f0a-1b2c-3d4e5f6a7b8c",
      "fieldChanged": "status",
      "oldValue": "Draft",
      "newValue": "Submitted",
      "reason": "Opportunity details complete and ready for matching"
    }
  ]
}
```
## 4. Skills Catalog Component Model

The Skills Catalog component represents the standardized taxonomy of skills used throughout the system.

### Attributes

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| id | UUID | Unique identifier for the skill | Yes |
| name | String | Name of the skill | Yes |
| category | Enum | Category (Technical, Soft, Industry, Language) | Yes |
| subcategory | String | Subcategory for organization | No |
| description | String | Description of the skill | Yes |
| isActive | Boolean | Whether the skill is active in the catalog | Yes |
| createdAt | DateTime | When the skill was added to the catalog | Yes |
| updatedAt | DateTime | When the skill was last updated | Yes |
| relatedSkills | Array of UUID | References to related skills | No |
| synonyms | Array of String | Alternative names for the skill | No |

### Sample Data

```json
{
  "id": "a1b2c3d4-e5f6-4a5b-8c7d-9e0f1a2b3c4d",
  "name": "AWS Lambda",
  "category": "Technical",
  "subcategory": "AWS Services",
  "description": "AWS Lambda is a serverless compute service that runs your code in response to events and automatically manages the underlying compute resources.",
  "isActive": true,
  "createdAt": "2024-01-10T08:00:00Z",
  "updatedAt": "2024-06-15T11:30:00Z",
  "relatedSkills": [
    "b2c3d4e5-f6a7-5b6c-9d0e-1f2a3b4c5d6e",
    "c3d4e5f6-a7b8-6c7d-0e1f-2a3b4c5d6e7f"
  ],
  "synonyms": [
    "Serverless Functions",
    "AWS Serverless"
  ]
}
```
## 5. Match Results Component Model

The Match Results component represents the output of the matching algorithm, providing recommendations of Solution Architects for opportunities.

### Attributes

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| id | UUID | Unique identifier for the match result | Yes |
| opportunityId | UUID | Reference to the opportunity | Yes |
| generatedAt | DateTime | When the match results were generated | Yes |
| algorithmVersion | String | Version of the matching algorithm used | Yes |
| configurationParameters | Object | Algorithm configuration parameters used | Yes |
| recommendations | Array of Recommendation | Recommended Solution Architects | Yes |
| status | Enum | Status of the match (Pending, Completed, Failed) | Yes |
| errorMessage | String | Error message if matching failed | No |
| processingTimeMs | Integer | Time taken to generate matches in milliseconds | Yes |

### Recommendation Object

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| solutionArchitectId | UUID | Reference to the Solution Architect | Yes |
| overallMatchScore | Decimal | Overall match score (0-100) | Yes |
| skillsMatchScore | Decimal | Skills match score (0-100) | Yes |
| availabilityMatchScore | Decimal | Availability match score (0-100) | Yes |
| languageMatchScore | Decimal | Language match score (0-100) | Yes |
| geographicMatchScore | Decimal | Geographic match score (0-100) | Yes |
| matchedSkills | Array of MatchedSkill | Skills that matched | Yes |
| unmatchedSkills | Array of UnmatchedSkill | Required skills that didn't match | Yes |
| availabilityConfirmation | Object | Confirmation of availability | Yes |
| rank | Integer | Rank among recommendations (1 = best match) | Yes |

### MatchedSkill Object

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| skillId | UUID | Reference to the skill | Yes |
| name | String | Name of the skill | Yes |
| requiredProficiencyLevel | Enum | Required proficiency level | Yes |
| actualProficiencyLevel | Enum | SA's actual proficiency level | Yes |
| importanceLevel | Enum | Must Have, Nice to Have | Yes |
| matchScore | Decimal | Match score for this skill (0-100) | Yes |

### UnmatchedSkill Object

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| skillId | UUID | Reference to the skill | Yes |
| name | String | Name of the skill | Yes |
| requiredProficiencyLevel | Enum | Required proficiency level | Yes |
| importanceLevel | Enum | Must Have, Nice to Have | Yes |
| reason | String | Reason for not matching | Yes |

### AvailabilityConfirmation Object

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| isFullyAvailable | Boolean | Whether SA is fully available for the opportunity | Yes |
| availableDays | Integer | Number of days SA is available | Yes |
| totalRequiredDays | Integer | Total number of days required | Yes |
| conflictingDates | Array of Date | Dates where SA is not available | No |

### Sample Data

```json
{
  "id": "g4h5i6j7-k8l9-0m1n-2o3p-4q5r6s7t8u9v",
  "opportunityId": "d1e2f3a4-b5c6-7d8e-9f0a-1b2c3d4e5f6a",
  "generatedAt": "2025-07-15T14:25:30Z",
  "algorithmVersion": "1.2.0",
  "configurationParameters": {
    "skillsWeight": 0.5,
    "availabilityWeight": 0.3,
    "languageWeight": 0.1,
    "geographicWeight": 0.1,
    "mustHaveMultiplier": 2.0,
    "niceToHaveMultiplier": 1.0
  },
  "recommendations": [
    {
      "solutionArchitectId": "550e8400-e29b-41d4-a716-446655440000",
      "overallMatchScore": 92.5,
      "skillsMatchScore": 95.0,
      "availabilityMatchScore": 100.0,
      "languageMatchScore": 100.0,
      "geographicMatchScore": 60.0,
      "matchedSkills": [
        {
          "skillId": "a1b2c3d4-e5f6-4a5b-8c7d-9e0f1a2b3c4d",
          "name": "AWS Migration",
          "requiredProficiencyLevel": "Advanced",
          "actualProficiencyLevel": "Expert",
          "importanceLevel": "Must Have",
          "matchScore": 100.0
        },
        {
          "skillId": "b2c3d4e5-f6a7-5b6c-9d0e-1f2a3b4c5d6e",
          "name": "Financial Services Cloud Architecture",
          "requiredProficiencyLevel": "Expert",
          "actualProficiencyLevel": "Expert",
          "importanceLevel": "Must Have",
          "matchScore": 100.0
        }
      ],
      "unmatchedSkills": [
        {
          "skillId": "c3d4e5f6-a7b8-6c7d-0e1f-2a3b4c5d6e7f",
          "name": "Database Migration",
          "requiredProficiencyLevel": "Intermediate",
          "importanceLevel": "Nice to Have",
          "reason": "Skill not found in SA profile"
        }
      ],
      "availabilityConfirmation": {
        "isFullyAvailable": true,
        "availableDays": 75,
        "totalRequiredDays": 75,
        "conflictingDates": []
      },
      "rank": 1
    },
    {
      "solutionArchitectId": "660f9511-f30c-52e5-b827-557766551111",
      "overallMatchScore": 85.2,
      "skillsMatchScore": 90.0,
      "availabilityMatchScore": 80.0,
      "languageMatchScore": 100.0,
      "geographicMatchScore": 70.0,
      "matchedSkills": [
        {
          "skillId": "a1b2c3d4-e5f6-4a5b-8c7d-9e0f1a2b3c4d",
          "name": "AWS Migration",
          "requiredProficiencyLevel": "Advanced",
          "actualProficiencyLevel": "Advanced",
          "importanceLevel": "Must Have",
          "matchScore": 100.0
        },
        {
          "skillId": "b2c3d4e5-f6a7-5b6c-9d0e-1f2a3b4c5d6e",
          "name": "Financial Services Cloud Architecture",
          "requiredProficiencyLevel": "Expert",
          "actualProficiencyLevel": "Advanced",
          "importanceLevel": "Must Have",
          "matchScore": 80.0
        }
      ],
      "unmatchedSkills": [
        {
          "skillId": "c3d4e5f6-a7b8-6c7d-0e1f-2a3b4c5d6e7f",
          "name": "Database Migration",
          "requiredProficiencyLevel": "Intermediate",
          "importanceLevel": "Nice to Have",
          "reason": "Skill not found in SA profile"
        }
      ],
      "availabilityConfirmation": {
        "isFullyAvailable": false,
        "availableDays": 60,
        "totalRequiredDays": 75,
        "conflictingDates": [
          "2025-11-01",
          "2025-12-15"
        ]
      },
      "rank": 2
    }
  ],
  "status": "Completed",
  "errorMessage": null,
  "processingTimeMs": 1250
}
```
## 6. Assignments Component Model

The Assignments component represents the assignment of a Solution Architect to an opportunity.

### Attributes

| Attribute | Data Type | Description | Required |
|-----------|-----------|-------------|----------|
| id | UUID | Unique identifier for the assignment | Yes |
| opportunityId | UUID | Reference to the opportunity | Yes |
| solutionArchitectId | UUID | Reference to the assigned Solution Architect | Yes |
| salesManagerId | UUID | Reference to the Sales Manager who made the selection | Yes |
| matchResultId | UUID | Reference to the match result that led to this assignment | Yes |
| status | Enum | Status of the assignment (Assigned, Accepted, Rejected, Completed, Cancelled) | Yes |
| assignedAt | DateTime | When the assignment was made | Yes |
| acceptedAt | DateTime | When the SA accepted the assignment | No |
| rejectedAt | DateTime | When the SA rejected the assignment | No |
| rejectionReason | String | Reason for rejection if rejected | No |
| completedAt | DateTime | When the assignment was completed | No |
| cancelledAt | DateTime | When the assignment was cancelled | No |
| cancellationReason | String | Reason for cancellation if cancelled | No |
| notes | String | Additional notes about the assignment | No |
| rating | Decimal | Rating given to the SA after completion (0-5) | No |
| feedback | String | Feedback given to the SA after completion | No |

### Sample Data

```json
{
  "id": "h5i6j7k8-l9m0-1n2o-3p4q-5r6s7t8u9v0w",
  "opportunityId": "d1e2f3a4-b5c6-7d8e-9f0a-1b2c3d4e5f6a",
  "solutionArchitectId": "550e8400-e29b-41d4-a716-446655440000",
  "salesManagerId": "f3a4b5c6-d7e8-9f0a-1b2c-3d4e5f6a7b8c",
  "matchResultId": "g4h5i6j7-k8l9-0m1n-2o3p-4q5r6s7t8u9v",
  "status": "Accepted",
  "assignedAt": "2025-07-16T09:30:00Z",
  "acceptedAt": "2025-07-16T10:15:45Z",
  "rejectedAt": null,
  "rejectionReason": null,
  "completedAt": null,
  "cancelledAt": null,
  "cancellationReason": null,
  "notes": "Selected based on excellent match score and previous experience with similar financial services migrations.",
  "rating": null,
  "feedback": null
}
```

## Component Relationships

The following diagram describes the relationships between the core components:

1. **User** is the base entity for all users in the system
   - A User can have one **Solution Architect Profile** (if role is SolutionArchitect)
   - A User (with SalesManager role) can create multiple **Opportunities**
   - A User (with Admin role) can manage the **Skills Catalog**

2. **Solution Architect Profile** extends User
   - A Solution Architect Profile references multiple skills from the **Skills Catalog**
   - A Solution Architect Profile can be included in multiple **Match Results**
   - A Solution Architect Profile can have multiple **Assignments**

3. **Opportunity** is created by a Sales Manager (User)
   - An Opportunity references multiple skills from the **Skills Catalog**
   - An Opportunity can have one or more **Match Results**
   - An Opportunity can have one **Assignment**

4. **Skills Catalog** is a central repository of standardized skills
   - Skills from the catalog are referenced by **Solution Architect Profiles**
   - Skills from the catalog are referenced by **Opportunities**
   - Skills from the catalog are referenced in **Match Results**

5. **Match Results** are generated for an Opportunity
   - Match Results reference an **Opportunity**
   - Match Results include recommendations of **Solution Architect Profiles**
   - Match Results can lead to an **Assignment**

6. **Assignments** connect Solution Architects to Opportunities
   - An Assignment references one **Opportunity**
   - An Assignment references one **Solution Architect Profile**
   - An Assignment references the **Match Results** that led to it
   - An Assignment references the Sales Manager (User) who made the selection
