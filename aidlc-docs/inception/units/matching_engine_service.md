# Matching Engine Service

## Unit Overview
This service contains the core matching algorithm that matches customer opportunities with the most suitable Solution Architects based on skills, availability, and other criteria. It also handles match-related notifications and recommendations presentation.

## Scope and Responsibilities
- Skills-based matching algorithm
- Availability filtering and validation
- Language and geographic matching
- Match score calculation and ranking
- Top matches recommendation generation
- Match details visualization
- Match-related notifications

## User Stories

### US-MA-1: Skills-Based Matching
**As the** system,  
**I want to** match Solution Architects with opportunities based on required skills,  
**So that** customers receive assistance from appropriately skilled professionals.

**Acceptance Criteria:**
- System compares required skills from opportunity with registered skills of Solution Architects
- System considers proficiency levels for each skill
- System distinguishes between "Must Have" and "Nice to Have" skills
- System assigns higher weight to exact skill matches
- System considers related skills when exact matches aren't available
- System generates a skills match score for each potential Solution Architect
- Match results include the percentage of matched skills

### US-MA-2: Availability-Based Filtering
**As the** system,  
**I want to** filter Solution Architects based on their availability during the opportunity timeline,  
**So that** only available Solution Architects are recommended.

**Acceptance Criteria:**
- System checks Solution Architect availability for the specific days required by the opportunity
- System excludes Solution Architects who are not available during the required period
- System considers partial availability if the opportunity timeline is flexible
- System accounts for existing commitments of Solution Architects
- System updates availability in real-time when new opportunities are assigned
- Match results include availability confirmation for each recommended Solution Architect

### US-MA-3: Language and Geographic Matching
**As the** system,  
**I want to** match Solution Architects based on language skills and geographic expertise,  
**So that** customers receive culturally and linguistically appropriate assistance.

**Acceptance Criteria:**
- System matches required languages with Solution Architects' language proficiencies
- System considers geographic location requirements specified in the opportunity
- System prioritizes Solution Architects with expertise in the required regions
- System considers remote work capabilities when geographic presence isn't possible
- System generates a language and geographic match score
- Match results include language and geographic match details

### US-MA-4: Match Score Calculation
**As the** system,  
**I want to** calculate an overall match score for each potential Solution Architect,  
**So that** Sales Managers can easily identify the best candidates.

**Acceptance Criteria:**
- System combines individual scores for skills, availability, language, and geographic matches
- System applies appropriate weighting to each factor based on opportunity requirements
- System normalizes scores on a 0-100 scale for easy comparison
- System ranks Solution Architects based on their overall match score
- System provides a breakdown of how each score was calculated
- Match results display both the overall score and component scores

### US-MA-5: Top Matches Recommendation
**As a** Sales Manager,  
**I want to** see a ranked list of the top matching Solution Architects for an opportunity,  
**So that** I can select the most appropriate candidate.

**Acceptance Criteria:**
- System displays a list of recommended Solution Architects sorted by match score
- System shows at least 3 and up to 10 top matches (if available)
- Each recommendation includes the Solution Architect's name, overall match score, and key matching attributes
- Sales Manager can view detailed profile information for each recommended Solution Architect
- Sales Manager can compare multiple recommendations side by side
- System provides visual indicators for exceptionally good matches (e.g., >90% match)

### US-MA-6: Match Details Visualization
**As a** Sales Manager,  
**I want to** view detailed information about why a Solution Architect was matched with an opportunity,  
**So that** I can make an informed selection decision.

**Acceptance Criteria:**
- Sales Manager can view a detailed breakdown of the match score
- System displays which required skills were matched and at what proficiency level
- System highlights any required skills that weren't matched
- System shows availability confirmation for the required timeline
- System provides language and geographic match details
- Sales Manager can access the Solution Architect's full profile from the match details

## Key Capabilities
- **Advanced Matching Algorithm**: Multi-factor matching with configurable weights
- **Real-time Processing**: Process matching requests within defined SLA
- **Score Calculation**: Comprehensive scoring with detailed breakdowns
- **Recommendation Engine**: Generate ranked recommendations with explanations
- **Availability Integration**: Real-time availability checking and filtering
- **Match Notifications**: Notify Sales Managers when matches are found
- **Performance Optimization**: Efficient matching for large datasets

## Integration Points
- **Outbound Dependencies**: 
  - Solution Architect Profile & Skills Service for SA profiles and availability
  - Opportunity Management Service for opportunity details and requirements
  - Email service for match notifications
- **Inbound Dependencies**: 
  - Opportunity Management Service triggers matching when opportunities are submitted
  - Selection & Assignment Service queries match results
  - System Administration Service for algorithm configuration
- **Shared Data Models**: 
  - Match results and scores
  - Recommendation rankings
  - Match explanations and breakdowns
  - Notification templates and preferences

## API Contracts
- Matching trigger endpoints
- Match results retrieval endpoints
- Recommendation ranking endpoints
- Match details and explanation endpoints
- Algorithm configuration endpoints
- Match status and notification endpoints

## Notes
- Designed as a microservice with its own database for match results
- Core business logic service that orchestrates matching across multiple criteria
- Includes notification capabilities for match-related communications
- Supports configurable matching weights and thresholds
- Optimized for performance with large numbers of Solution Architects
- Maintains match history for analytics and improvement
- Integrates with multiple services to gather matching data
