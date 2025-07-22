# Solution Architect Profile & Skills Service

## Unit Overview
This service manages all aspects of Solution Architect profiles, including skills registration (technical, soft, industry, language, geographic) and availability management. It provides comprehensive profile data for the matching algorithm.

## Scope and Responsibilities
- Solution Architect skills registration and management
- Availability calendar management
- Profile completeness tracking
- Skills catalog integration
- Availability notifications and reminders

## User Stories

### US-SA-3: Technical Skills Registration
**As a** Solution Architect,  
**I want to** register my technical skills with proficiency levels,  
**So that** I can be matched with opportunities requiring those skills.

**Acceptance Criteria:**
- Solution Architect can select from a predefined list of technical skills (AWS services, technologies, etc.)
- Solution Architect can add custom technical skills not in the predefined list
- Solution Architect can specify proficiency level for each skill (Beginner, Intermediate, Advanced, Expert)
- Solution Architect can add years of experience for each skill
- System saves the registered skills and displays them in the profile
- Solution Architect can edit or remove skills at any time

### US-SA-4: Soft Skills Registration
**As a** Solution Architect,  
**I want to** register my soft skills,  
**So that** I can be matched with opportunities requiring specific interpersonal abilities.

**Acceptance Criteria:**
- Solution Architect can select from a predefined list of soft skills (presentation, communication, leadership, etc.)
- Solution Architect can add custom soft skills not in the predefined list
- Solution Architect can specify proficiency level for each soft skill
- System saves the registered soft skills and displays them in the profile
- Solution Architect can edit or remove soft skills at any time

### US-SA-5: Industry Knowledge Registration
**As a** Solution Architect,  
**I want to** register my industry knowledge and experience,  
**So that** I can be matched with opportunities in industries I'm familiar with.

**Acceptance Criteria:**
- Solution Architect can select from a predefined list of industries (healthcare, finance, retail, etc.)
- Solution Architect can specify years of experience in each industry
- Solution Architect can add specific domain knowledge within each industry
- System saves the registered industry knowledge and displays it in the profile
- Solution Architect can edit or remove industry knowledge at any time

### US-SA-6: Language Skills Registration
**As a** Solution Architect,  
**I want to** register the languages I speak and my proficiency levels,  
**So that** I can be matched with opportunities requiring specific language skills.

**Acceptance Criteria:**
- Solution Architect can select from a predefined list of languages
- Solution Architect can specify proficiency level for each language (Basic, Conversational, Fluent, Native)
- System saves the registered languages and displays them in the profile
- Solution Architect can edit or remove languages at any time

### US-SA-7: Geographic Location Registration
**As a** Solution Architect,  
**I want to** register my geographic locations of expertise and preference,  
**So that** I can be matched with opportunities in those regions.

**Acceptance Criteria:**
- Solution Architect can select multiple geographic regions/countries
- Solution Architect can specify if they are willing to travel to specific regions
- Solution Architect can indicate remote work capabilities
- System saves the registered geographic preferences and displays them in the profile
- Solution Architect can edit or remove geographic preferences at any time

### US-SA-8: Monthly Availability Registration
**As a** Solution Architect,  
**I want to** register my availability for specific days in a month,  
**So that** I can be matched only with opportunities during my available time.

**Acceptance Criteria:**
- Solution Architect can view a calendar interface showing the current and upcoming months
- Solution Architect can select/deselect specific days to indicate availability
- Solution Architect can set recurring availability patterns (e.g., always available on Mondays)
- System saves the availability information and displays it in a calendar view
- Solution Architect receives confirmation when availability is updated

### US-SA-9: Availability Update Notification
**As a** Solution Architect,  
**I want to** receive reminders to update my availability,  
**So that** my availability status is always current.

**Acceptance Criteria:**
- System sends monthly reminders to update availability for the upcoming month
- Reminders are sent via email with direct links to update availability
- Solution Architect can set preferences for reminder frequency
- Solution Architect can disable reminders if desired

## Key Capabilities
- **Skills Management**: Comprehensive skills registration across multiple categories
- **Availability Management**: Calendar-based availability tracking and management
- **Profile Completeness**: Track and encourage complete profile information
- **Notification Management**: Automated reminders for availability updates
- **Skills Validation**: Integration with standardized skills catalogs

## Integration Points
- **Outbound Dependencies**: 
  - User Management Service for user authentication and basic profile
  - Email service for availability reminders
  - System Administration Service for skills catalog
- **Inbound Dependencies**: 
  - Matching Engine Service queries this service for SA profiles and availability
  - Selection & Assignment Service updates availability when SAs are assigned
- **Shared Data Models**: 
  - Solution Architect profile (skills, availability, preferences)
  - Skills catalog and proficiency levels
  - Availability calendar data

## API Contracts
- Skills CRUD endpoints (technical, soft, industry, language, geographic)
- Availability management endpoints
- Profile retrieval endpoints for matching
- Availability query endpoints
- Notification preference management endpoints

## Notes
- Designed as a microservice with its own database
- Maintains comprehensive SA profile data for matching purposes
- Handles complex availability calendar logic
- Integrates with notification system for availability reminders
- Supports both predefined and custom skills across all categories
