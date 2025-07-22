# User Stories: Sales Manager Selection Process

## Viewing Recommendations

### US-SS-1: View Recommended Solution Architects
**As a** Sales Manager,  
**I want to** view a list of recommended Solution Architects for my opportunity,  
**So that** I can select the most appropriate one for the customer.

**Acceptance Criteria:**
- Sales Manager receives notification when matches are found
- Sales Manager can access a dedicated page showing all recommended Solution Architects
- Recommendations are displayed in order of match score (highest to lowest)
- Each recommendation shows the Solution Architect's name, photo, match score, key skills, and availability
- System indicates when recommendations are ready within 1 hour of opportunity submission
- Sales Manager can refresh recommendations if needed

### US-SS-2: View Solution Architect Profiles
**As a** Sales Manager,  
**I want to** view detailed profiles of recommended Solution Architects,  
**So that** I can evaluate their qualifications beyond the match score.

**Acceptance Criteria:**
- Sales Manager can click on a recommendation to view the full profile
- Profile includes professional background, skills, experience, languages, and geographic expertise
- Profile highlights the specific skills that match the opportunity requirements
- Profile shows the Solution Architect's availability calendar for the opportunity timeline
- Sales Manager can navigate between profiles easily
- Profile includes any previous collaboration history with the Sales Manager or customer

### US-SS-3: Compare Multiple Solution Architects
**As a** Sales Manager,  
**I want to** compare multiple recommended Solution Architects side by side,  
**So that** I can evaluate their relative strengths for the opportunity.

**Acceptance Criteria:**
- Sales Manager can select up to 3 Solution Architects for comparison
- Comparison view displays key attributes in a side-by-side format
- Comparison highlights differences in skills, experience, and availability
- Sales Manager can customize which attributes to compare
- Comparison view includes match scores and score breakdowns
- Sales Manager can make a selection directly from the comparison view

## Making a Selection

### US-SS-4: Select a Solution Architect
**As a** Sales Manager,  
**I want to** select a Solution Architect for my opportunity,  
**So that** the customer can be served by the most appropriate professional.

**Acceptance Criteria:**
- Sales Manager can select any Solution Architect from the recommendations
- System prompts for confirmation before finalizing the selection
- Sales Manager can add notes explaining the selection decision
- System records the selection with timestamp and Sales Manager information
- Sales Manager receives confirmation when selection is complete
- Selected Solution Architect is clearly marked in the opportunity details

### US-SS-5: Request Additional Information
**As a** Sales Manager,  
**I want to** request additional information from a potential Solution Architect before making a selection,  
**So that** I can make a more informed decision.

**Acceptance Criteria:**
- Sales Manager can send an information request to a specific Solution Architect
- Sales Manager can specify what additional information is needed
- Solution Architect receives notification of the information request
- Solution Architect can respond with the requested information
- Sales Manager receives notification when the response is available
- All communication is tracked within the system for reference

### US-SS-6: Override Match Recommendations
**As a** Sales Manager,  
**I want to** select a Solution Architect who wasn't in the top recommendations,  
**So that** I can use my judgment when the algorithm doesn't account for specific factors.

**Acceptance Criteria:**
- Sales Manager can search for and select any available Solution Architect in the system
- System requires justification when selecting outside the recommendations
- System warns about potential skill gaps or availability conflicts
- Selection is flagged for review by administrators
- System records the override decision with justification
- Reports include data on recommendation overrides for system improvement

## Post-Selection Process

### US-SS-7: Notify Selected Solution Architect
**As the** system,  
**I want to** notify the selected Solution Architect via email with the Sales Manager in cc,  
**So that** they are aware of their assignment to the opportunity.

**Acceptance Criteria:**
- System automatically sends email notification to the selected Solution Architect
- Email includes the Sales Manager in cc
- Notification contains opportunity details, customer information, and next steps
- Notification includes a link to view the full opportunity in the system
- Solution Architect can acknowledge receipt of the notification
- System records when the notification was sent and acknowledged

### US-SS-8: Manage Selection Changes
**As a** Sales Manager,  
**I want to** change my Solution Architect selection if necessary,  
**So that** I can respond to changing circumstances or availability issues.

**Acceptance Criteria:**
- Sales Manager can change the selection before the opportunity start date
- System requires justification for the change
- Previously selected Solution Architect receives notification of the change
- Newly selected Solution Architect receives assignment notification
- System maintains history of all selection changes
- Selection changes are flagged for reporting and analysis

### US-SS-9: Provide Post-Selection Feedback
**As a** Sales Manager,  
**I want to** provide feedback on the selected Solution Architect after the opportunity is completed,  
**So that** the matching system can improve and Solution Architects can receive performance feedback.

**Acceptance Criteria:**
- Sales Manager receives a prompt for feedback when an opportunity is marked complete
- Feedback form includes rating scales and open-ended questions
- Sales Manager can evaluate how well the Solution Architect met the opportunity requirements
- Feedback is shared with the Solution Architect in an anonymized format
- Feedback data is used to improve the matching algorithm
- System aggregates feedback for reporting and analysis
