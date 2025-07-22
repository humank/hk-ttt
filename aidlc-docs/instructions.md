# AI-DLC Workflow

## Inception

### Intent to User Stories

Your Role: You are an expert product manager. You are tasked with creating well defined user stories that become the contract for developing the system as described in the Task section below. 

Plan for the work ahead and write your steps in the aidlc-docs/inception/user_stories_plan.md file with checkboxes for each step in the plan. If any step needs my clarification, add the questions with the [Question] tag and create an empty [Answer] tag for me to fill the answer. Do not make any assumptions or decisions on your own. Upon creating the plan, ask for my review and approval. After my approval, you can go ahead to execute the same plan one step at a time. Once you finish each step, mark the checkboxes as completed in the plan.

Your Task: Solution Architects register their skills and availability. Sales Managers registers customer opportunity with the problem statement. System matches the customer opportunity with the top matching  Solution Architects based on skills and  availability. Sales Manager chooses a Solutions Architect from the system recommended options. The objective of this system is to serve the customer opportunities faster with best matching skills.



### Stories to Units


Your Role: You are an experienced software architect. You are tasked with understanding the user stories of a full system as in the Task section. You will group the stories into multiple units of work that can be implemented in parallel. Each unit contains highly cohesive user stories that can be built by a single team. An unit is equivalent to bounded contexts in domain driven design and is aligned to a particular subdomain or specific business roles. For each unit, write their respective user stories and acceptance criteria in individual md files in the aidlc-docs/inception/units/ folder. Don't generate any additional design details. 

Plan for the work ahead and write your steps in the iaidlc-docs/nception/units/units_plan.md file with checkboxes for each step in the plan. If any step needs my clarification, add the questions with the [Question] tag and create an empty [Answer] tag for me to fill the answer. Do not make any assumptions or decisions on your own. Upon creating the plan, ask for my review and approval. After my approval, you can go ahead to execute the same plan one step at a time. Once you finish each step, mark the checkboxes as completed in the plan.

Your Task: Refer to the user stories in the aidlc-docs/inception/comprehensive_user_stories.md folder.


## Construction

### Domain Modelling

Your Role: You are an experienced software engineer. You are tasked with designing the Domain Model to implement all the user stories as referred in the Task section. This model shall contain all the components, the attributes, the behaviours and how the components interact to implement business logic in the user stories. Do not generate any architectural components. Do not generate any codes. Write the component model into a separate md file in the aidlc-docs/construction folder. We will use Amazon Bedrock API for the AI capabilities. Don't create any AI functionality from the scratch.

Plan for the work ahead and write your steps in the aidlc-docs/construction/domain_model_plan.md file with checkboxes for each step in the plan. If any step needs my clarification, add the questions with the [Question] tag and create an empty [Answer] tag for me to fill the answer. Do not make any assumptions or decisions on your own. Upon creating the plan, ask for my review and approval. After my approval, you can go ahead to execute the same plan one step at a time. Once you finish each step, mark the checkboxes as completed in the plan.

Your Task: Refer to the user stories in the /Users/yikaikao/git/hk-ttt/aidlc-docs/inception/units/opportunity_management_service.md

### Dmain Model to Code

Your Role: You are an experienced software engineer. Your task is as mentioned in the Task section below. Plan for the work ahead and write your steps in the aidlc-docs/construction/domain_model_plan.md file with checkboxes for each step in the plan. If any step needs my clarification, add the questions with the [Question] tag and create an empty [Answer] tag for me to fill the answer. Do not make any assumptions or decisions on your own. Upon creating the plan, ask for my review and approval. After my approval, you can go ahead to execute the same plan one step at a time. Once you finish each step, mark the checkboxes as completed in the plan.

Task: Refer to aidlc-docs/construction/domain_model_plan.md file. Generate a very simple and intuitive Python implementation for the components in the domain model. Keep the directory structure flat. Reuse standard python components available for loggic and other utulities. Assume the repositories are in-memory. Generate the classes in respective individual files.


### Adding Architectural Components

Your Role: You are an experienced software architect. Your task is as mentioned in the Task section below. Plan for the work ahead and write your steps in the aidlc-docs/construction/architecture_plan.md file with checkboxes for each step in the plan. If any step needs my clarification, add the questions with the [Question] tag and create an empty [Answer] tag for me to fill the answer. Do not make any assumptions or decisions on your own. Upon creating the plan, ask for my review and approval. After my approval, you can go ahead to execute the same plan one step at a time. Once you finish each step, mark the checkboxes as completed in the plan.

Task: Refer to text_enhancement/text_enhancement_service.py. I want to expose enhance_content method to be consumed by clients over the internet. This service will be hosted on AWS. Use AWS Well Architected Principles and select the packaging and deployment option.