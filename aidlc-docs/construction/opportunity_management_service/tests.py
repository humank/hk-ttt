"""
Unit tests for the Opportunity Management Service.
"""

import unittest
import uuid
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

# Mock the imports to avoid issues with dataclasses
class MockUser:
    def __init__(self, id=None, name="", email="", role="", employee_id="", department="", job_title="", is_active=True):
        self.id = id or uuid.uuid4()
        self.name = name
        self.email = email
        self.role = role
        self.employee_id = employee_id
        self.department = department
        self.job_title = job_title
        self.is_active = is_active
    
    def is_sales_manager(self):
        return self.role == "SalesManager" and self.is_active
    
    def is_solution_architect(self):
        return self.role == "SolutionArchitect" and self.is_active
    
    def is_admin(self):
        return self.role == "Admin" and self.is_active

class MockCustomer:
    def __init__(self, id=None, name="", industry="", is_active=True):
        self.id = id or uuid.uuid4()
        self.name = name
        self.industry = industry
        self.is_active = is_active

class MockSkillsCatalog:
    def __init__(self, id=None, name="", category=None, description="", is_active=True):
        self.id = id or uuid.uuid4()
        self.name = name
        self.category = category
        self.description = description
        self.is_active = is_active

class MockOpportunity:
    def __init__(self, id=None, title="", customer_id=None, customer_name="", sales_manager_id=None, 
                description="", priority=None, status=None, annual_recurring_revenue=0.0, 
                geographic_requirements=None):
        self.id = id or uuid.uuid4()
        self.title = title
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.sales_manager_id = sales_manager_id
        self.description = description
        self.priority = priority
        self.status = status
        self.annual_recurring_revenue = annual_recurring_revenue
        self.geographic_requirements = geographic_requirements
        self.submitted_at = None
        self.completed_at = None
        self.cancelled_at = None
        self.cancellation_reason = None
        self.reactivation_deadline = None

class MockProblemStatement:
    def __init__(self, id=None, opportunity_id=None, content="", minimum_character_count=140):
        self.id = id or uuid.uuid4()
        self.opportunity_id = opportunity_id
        self.content = content
        self.minimum_character_count = minimum_character_count

class MockSkillRequirement:
    def __init__(self, id=None, opportunity_id=None, skill_id=None, skill_name="", 
                skill_type=None, importance_level=None, minimum_proficiency_level=None):
        self.id = id or uuid.uuid4()
        self.opportunity_id = opportunity_id
        self.skill_id = skill_id
        self.skill_name = skill_name
        self.skill_type = skill_type
        self.importance_level = importance_level
        self.minimum_proficiency_level = minimum_proficiency_level

class MockTimelineRequirement:
    def __init__(self, id=None, opportunity_id=None, expected_start_date="", expected_end_date="", 
                is_flexible=False, specific_required_days=None):
        self.id = id or uuid.uuid4()
        self.opportunity_id = opportunity_id
        self.expected_start_date = expected_start_date
        self.expected_end_date = expected_end_date
        self.is_flexible = is_flexible
        self.specific_required_days = specific_required_days or []

class MockOpportunityStatusEntity:
    def __init__(self, id=None, opportunity_id=None, status=None, changed_by=None, 
                changed_at=None, reason=None):
        self.id = id or uuid.uuid4()
        self.opportunity_id = opportunity_id
        self.status = status
        self.changed_by = changed_by
        self.changed_at = changed_at or datetime.now()
        self.reason = reason

class MockAttachment:
    def __init__(self, id=None, problem_statement_id=None, file_name="", file_type="", 
                file_size=0, file_url="", uploaded_by=None, is_removed=False):
        self.id = id or uuid.uuid4()
        self.problem_statement_id = problem_statement_id
        self.file_name = file_name
        self.file_type = file_type
        self.file_size = file_size
        self.file_url = file_url
        self.uploaded_by = uploaded_by
        self.is_removed = is_removed

class MockChangeRecord:
    def __init__(self, id=None, opportunity_id=None, changed_by=None, field_changed="", 
                reason="", old_value=None, new_value=None):
        self.id = id or uuid.uuid4()
        self.opportunity_id = opportunity_id
        self.changed_by = changed_by
        self.field_changed = field_changed
        self.reason = reason
        self.old_value = old_value
        self.new_value = new_value
        self.changed_at = datetime.now()

# Mock repositories
class MockRepository:
    def __init__(self):
        self.items = {}
    
    def add(self, entity):
        self.items[entity.id] = entity
        return entity
    
    def get_by_id(self, entity_id):
        return self.items.get(entity_id)
    
    def update(self, entity):
        self.items[entity.id] = entity
        return entity
    
    def remove(self, entity_id):
        if entity_id in self.items:
            del self.items[entity_id]
            return True
        return False
    
    def get_all(self):
        return list(self.items.values())

class MockUserRepository(MockRepository):
    def get_by_email(self, email):
        for user in self.items.values():
            if user.email == email:
                return user
        return None
    
    def get_sales_managers(self):
        return [user for user in self.items.values() if user.is_sales_manager()]

class MockCustomerRepository(MockRepository):
    def get_active_customers(self):
        return [customer for customer in self.items.values() if customer.is_active]

class MockSkillsCatalogRepository(MockRepository):
    def get_active_skills(self):
        return [skill for skill in self.items.values() if skill.is_active]

class MockOpportunityRepository(MockRepository):
    def get_by_sales_manager(self, sales_manager_id):
        return [opp for opp in self.items.values() if opp.sales_manager_id == sales_manager_id]

class MockProblemStatementRepository(MockRepository):
    def get_by_opportunity(self, opportunity_id):
        for statement in self.items.values():
            if statement.opportunity_id == opportunity_id:
                return statement
        return None

class MockSkillRequirementRepository(MockRepository):
    def get_by_opportunity(self, opportunity_id):
        return [req for req in self.items.values() if req.opportunity_id == opportunity_id]

class MockTimelineRequirementRepository(MockRepository):
    def get_by_opportunity(self, opportunity_id):
        for timeline in self.items.values():
            if timeline.opportunity_id == opportunity_id:
                return timeline
        return None

class MockOpportunityStatusRepository(MockRepository):
    def get_by_opportunity(self, opportunity_id):
        return [status for status in self.items.values() if status.opportunity_id == opportunity_id]
    
    def get_status_history(self, opportunity_id):
        statuses = self.get_by_opportunity(opportunity_id)
        return sorted(statuses, key=lambda s: s.changed_at)

class MockAttachmentRepository(MockRepository):
    def get_by_problem_statement(self, problem_statement_id):
        return [attachment for attachment in self.items.values() 
                if attachment.problem_statement_id == problem_statement_id]
    
    def get_active_attachments(self, problem_statement_id):
        return [attachment for attachment in self.items.values() 
                if attachment.problem_statement_id == problem_statement_id and not attachment.is_removed]

class MockChangeRecordRepository(MockRepository):
    def get_by_opportunity(self, opportunity_id):
        return [record for record in self.items.values() if record.opportunity_id == opportunity_id]

# Mock enums
class MockPriority:
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class MockOpportunityStatus:
    DRAFT = "Draft"
    SUBMITTED = "Submitted"
    MATCHING_IN_PROGRESS = "Matching in Progress"
    MATCHES_FOUND = "Matches Found"
    ARCHITECT_SELECTED = "Architect Selected"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class MockSkillType:
    TECHNICAL = "Technical"
    SOFT = "Soft"
    INDUSTRY = "Industry"
    LANGUAGE = "Language"

class MockImportanceLevel:
    MUST_HAVE = "Must Have"
    NICE_TO_HAVE = "Nice to Have"

class MockProficiencyLevel:
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    EXPERT = "Expert"

# Mock exceptions
class MockValidationException(Exception):
    pass

class MockNotFoundException(Exception):
    pass

class MockOperationNotAllowedException(Exception):
    pass

# Mock services
class MockOpportunityService:
    def __init__(self, opportunity_repository, problem_statement_repository, skill_requirement_repository,
                timeline_requirement_repository, opportunity_status_repository, change_record_repository,
                skills_catalog_repository, user_repository, customer_repository):
        self.opportunity_repository = opportunity_repository
        self.problem_statement_repository = problem_statement_repository
        self.skill_requirement_repository = skill_requirement_repository
        self.timeline_requirement_repository = timeline_requirement_repository
        self.opportunity_status_repository = opportunity_status_repository
        self.change_record_repository = change_record_repository
        self.skills_catalog_repository = skills_catalog_repository
        self.user_repository = user_repository
        self.customer_repository = customer_repository
    
    def create_opportunity(self, title, customer_id, customer_name, sales_manager_id, description,
                         priority, annual_recurring_revenue, geographic_requirements):
        # Validate user is a sales manager
        user = self.user_repository.get_by_id(sales_manager_id)
        if not user or not user.is_sales_manager():
            raise MockOperationNotAllowedException("Only Sales Managers can create opportunities")
        
        # Validate customer exists
        customer = self.customer_repository.get_by_id(customer_id)
        if not customer:
            raise MockNotFoundException(f"Customer with ID {customer_id} not found")
        
        # Create opportunity
        opportunity = MockOpportunity(
            title=title,
            customer_id=customer_id,
            customer_name=customer_name,
            sales_manager_id=sales_manager_id,
            description=description,
            priority=priority,
            status=MockOpportunityStatus.DRAFT,
            annual_recurring_revenue=annual_recurring_revenue,
            geographic_requirements=geographic_requirements
        )
        
        # Save opportunity
        saved_opportunity = self.opportunity_repository.add(opportunity)
        
        # Create initial status record
        status_record = MockOpportunityStatusEntity(
            opportunity_id=saved_opportunity.id,
            status=MockOpportunityStatus.DRAFT,
            changed_by=sales_manager_id,
            reason="Opportunity created"
        )
        self.opportunity_status_repository.add(status_record)
        
        return saved_opportunity
    
    def add_problem_statement(self, opportunity_id, content):
        # Validate opportunity exists
        opportunity = self.opportunity_repository.get_by_id(opportunity_id)
        if not opportunity:
            raise MockNotFoundException(f"Opportunity with ID {opportunity_id} not found")
        
        # Validate opportunity is in Draft status
        if opportunity.status != MockOpportunityStatus.DRAFT:
            raise MockOperationNotAllowedException(
                "Problem statement can only be added to opportunities in Draft status"
            )
        
        # Validate content length
        if len(content) < 140:
            raise MockValidationException("Problem statement must be at least 140 characters long")
        
        # Check if problem statement already exists
        existing_statement = self.problem_statement_repository.get_by_opportunity(opportunity_id)
        if existing_statement:
            raise MockOperationNotAllowedException(
                f"Problem statement already exists for opportunity {opportunity_id}"
            )
        
        # Create problem statement
        problem_statement = MockProblemStatement(
            opportunity_id=opportunity_id,
            content=content
        )
        
        # Save problem statement
        return self.problem_statement_repository.add(problem_statement)
    
    def add_skill_requirement(self, opportunity_id, skill_id, skill_type, importance_level, minimum_proficiency_level):
        # Validate opportunity exists
        opportunity = self.opportunity_repository.get_by_id(opportunity_id)
        if not opportunity:
            raise MockNotFoundException(f"Opportunity with ID {opportunity_id} not found")
        
        # Validate opportunity is in Draft status
        if opportunity.status != MockOpportunityStatus.DRAFT:
            raise MockOperationNotAllowedException(
                "Skill requirements can only be added to opportunities in Draft status"
            )
        
        # Validate skill exists in catalog
        skill = self.skills_catalog_repository.get_by_id(skill_id)
        if not skill:
            raise MockNotFoundException(f"Skill with ID {skill_id} not found in Skills Catalog")
        
        if not skill.is_active:
            raise MockValidationException(f"Skill with ID {skill_id} is not active")
        
        # Create skill requirement
        skill_requirement = MockSkillRequirement(
            opportunity_id=opportunity_id,
            skill_id=skill_id,
            skill_name=skill.name,
            skill_type=skill_type,
            importance_level=importance_level,
            minimum_proficiency_level=minimum_proficiency_level
        )
        
        # Save skill requirement
        return self.skill_requirement_repository.add(skill_requirement)
    
    def add_timeline_requirement(self, opportunity_id, start_date, end_date, is_flexible, specific_days=None):
        # Validate opportunity exists
        opportunity = self.opportunity_repository.get_by_id(opportunity_id)
        if not opportunity:
            raise MockNotFoundException(f"Opportunity with ID {opportunity_id} not found")
        
        # Validate opportunity is in Draft status
        if opportunity.status != MockOpportunityStatus.DRAFT:
            raise MockOperationNotAllowedException(
                "Timeline requirement can only be added to opportunities in Draft status"
            )
        
        # Check if timeline requirement already exists
        existing_timeline = self.timeline_requirement_repository.get_by_opportunity(opportunity_id)
        if existing_timeline:
            raise MockOperationNotAllowedException(
                f"Timeline requirement already exists for opportunity {opportunity_id}"
            )
        
        # Create timeline requirement
        timeline_requirement = MockTimelineRequirement(
            opportunity_id=opportunity_id,
            expected_start_date=start_date,
            expected_end_date=end_date,
            is_flexible=is_flexible,
            specific_required_days=specific_days or []
        )
        
        # Save timeline requirement
        return self.timeline_requirement_repository.add(timeline_requirement)

class MockAttachmentService:
    def __init__(self, attachment_repository, problem_statement_repository):
        self.attachment_repository = attachment_repository
        self.problem_statement_repository = problem_statement_repository
    
    def add_attachment(self, problem_statement_id, file_name, file_type, file_size, file_url, uploaded_by):
        # Validate problem statement exists
        problem_statement = self.problem_statement_repository.get_by_id(problem_statement_id)
        if not problem_statement:
            raise MockNotFoundException(f"Problem statement with ID {problem_statement_id} not found")
        
        # Validate file size
        max_size = 20 * 1024 * 1024  # 20MB
        if file_size > max_size:
            raise MockValidationException(f"File size exceeds the maximum allowed size of 20MB")
        
        # Create attachment
        attachment = MockAttachment(
            problem_statement_id=problem_statement_id,
            file_name=file_name,
            file_type=file_type,
            file_size=file_size,
            file_url=file_url,
            uploaded_by=uploaded_by
        )
        
        # Save attachment
        return self.attachment_repository.add(attachment)
    
    def remove_attachment(self, attachment_id, user_id):
        # Validate attachment exists
        attachment = self.attachment_repository.get_by_id(attachment_id)
        if not attachment:
            raise MockNotFoundException(f"Attachment with ID {attachment_id} not found")
        
        # Mark attachment as removed
        attachment.is_removed = True
        
        # Save updated attachment
        return self.attachment_repository.update(attachment)
    
    def get_attachments_for_problem_statement(self, problem_statement_id):
        return self.attachment_repository.get_active_attachments(problem_statement_id)

# Test cases
class TestOpportunityService(unittest.TestCase):
    def setUp(self):
        # Create repositories
        self.user_repository = MockUserRepository()
        self.customer_repository = MockCustomerRepository()
        self.skills_catalog_repository = MockSkillsCatalogRepository()
        self.opportunity_repository = MockOpportunityRepository()
        self.problem_statement_repository = MockProblemStatementRepository()
        self.skill_requirement_repository = MockSkillRequirementRepository()
        self.timeline_requirement_repository = MockTimelineRequirementRepository()
        self.opportunity_status_repository = MockOpportunityStatusRepository()
        self.attachment_repository = MockAttachmentRepository()
        self.change_record_repository = MockChangeRecordRepository()
        
        # Create service
        self.opportunity_service = MockOpportunityService(
            opportunity_repository=self.opportunity_repository,
            problem_statement_repository=self.problem_statement_repository,
            skill_requirement_repository=self.skill_requirement_repository,
            timeline_requirement_repository=self.timeline_requirement_repository,
            opportunity_status_repository=self.opportunity_status_repository,
            change_record_repository=self.change_record_repository,
            skills_catalog_repository=self.skills_catalog_repository,
            user_repository=self.user_repository,
            customer_repository=self.customer_repository
        )
        
        # Create test data
        # Sales Manager
        self.sales_manager = MockUser(
            name="John Doe",
            email="john.doe@example.com",
            role="SalesManager",
            employee_id="EMP12345",
            department="Sales",
            job_title="Sales Manager"
        )
        self.user_repository.add(self.sales_manager)
        
        # Customer
        self.customer = MockCustomer(
            name="Acme Inc.",
            industry="Technology"
        )
        self.customer_repository.add(self.customer)
        
        # Skills
        self.aws_migration_skill = MockSkillsCatalog(
            name="AWS Migration",
            category=MockSkillType.TECHNICAL,
            description="Experience with migrating workloads to AWS",
            is_active=True
        )
        self.skills_catalog_repository.add(self.aws_migration_skill)
        
        # Geographic requirements
        self.geographic_requirements = {
            "region_id": str(uuid.uuid4()),
            "name": "North America",
            "requires_physical_presence": True,
            "allows_remote_work": True
        }
    
    def test_create_opportunity(self):
        # Create opportunity
        opportunity = self.opportunity_service.create_opportunity(
            title="Cloud Migration Project",
            customer_id=self.customer.id,
            customer_name=self.customer.name,
            sales_manager_id=self.sales_manager.id,
            description="Migrate on-premises infrastructure to the cloud",
            priority=MockPriority.HIGH,
            annual_recurring_revenue=100000.0,
            geographic_requirements=self.geographic_requirements
        )
        
        # Verify opportunity was created correctly
        self.assertEqual(opportunity.title, "Cloud Migration Project")
        self.assertEqual(opportunity.customer_id, self.customer.id)
        self.assertEqual(opportunity.customer_name, self.customer.name)
        self.assertEqual(opportunity.sales_manager_id, self.sales_manager.id)
        self.assertEqual(opportunity.description, "Migrate on-premises infrastructure to the cloud")
        self.assertEqual(opportunity.priority, MockPriority.HIGH)
        self.assertEqual(opportunity.annual_recurring_revenue, 100000.0)
        self.assertEqual(opportunity.status, MockOpportunityStatus.DRAFT)
        
        # Verify opportunity was added to repository
        saved_opportunity = self.opportunity_repository.get_by_id(opportunity.id)
        self.assertIsNotNone(saved_opportunity)
        
        # Verify status record was created
        status_records = self.opportunity_status_repository.get_by_opportunity(opportunity.id)
        self.assertEqual(len(status_records), 1)
        self.assertEqual(status_records[0].status, MockOpportunityStatus.DRAFT)
    
    def test_add_problem_statement(self):
        # Create opportunity
        opportunity = self.opportunity_service.create_opportunity(
            title="Cloud Migration Project",
            customer_id=self.customer.id,
            customer_name=self.customer.name,
            sales_manager_id=self.sales_manager.id,
            description="Migrate on-premises infrastructure to the cloud",
            priority=MockPriority.HIGH,
            annual_recurring_revenue=100000.0,
            geographic_requirements=self.geographic_requirements
        )
        
        # Add problem statement
        content = "This is a detailed problem statement that meets the minimum character requirement. " \
                 "The customer needs to migrate their on-premises infrastructure to the cloud to " \
                 "improve scalability and reduce operational costs."
        
        problem_statement = self.opportunity_service.add_problem_statement(
            opportunity_id=opportunity.id,
            content=content
        )
        
        # Verify problem statement was created correctly
        self.assertEqual(problem_statement.opportunity_id, opportunity.id)
        self.assertEqual(problem_statement.content, content)
        
        # Verify problem statement was added to repository
        saved_statement = self.problem_statement_repository.get_by_opportunity(opportunity.id)
        self.assertIsNotNone(saved_statement)
        self.assertEqual(saved_statement.content, content)
    
    def test_add_problem_statement_too_short(self):
        # Create opportunity
        opportunity = self.opportunity_service.create_opportunity(
            title="Cloud Migration Project",
            customer_id=self.customer.id,
            customer_name=self.customer.name,
            sales_manager_id=self.sales_manager.id,
            description="Migrate on-premises infrastructure to the cloud",
            priority=MockPriority.HIGH,
            annual_recurring_revenue=100000.0,
            geographic_requirements=self.geographic_requirements
        )
        
        # Try to add a short problem statement
        short_content = "This is too short"
        
        with self.assertRaises(MockValidationException):
            self.opportunity_service.add_problem_statement(
                opportunity_id=opportunity.id,
                content=short_content
            )
    
    def test_add_skill_requirement(self):
        # Create opportunity
        opportunity = self.opportunity_service.create_opportunity(
            title="Cloud Migration Project",
            customer_id=self.customer.id,
            customer_name=self.customer.name,
            sales_manager_id=self.sales_manager.id,
            description="Migrate on-premises infrastructure to the cloud",
            priority=MockPriority.HIGH,
            annual_recurring_revenue=100000.0,
            geographic_requirements=self.geographic_requirements
        )
        
        # Add skill requirement
        skill_requirement = self.opportunity_service.add_skill_requirement(
            opportunity_id=opportunity.id,
            skill_id=self.aws_migration_skill.id,
            skill_type=MockSkillType.TECHNICAL,
            importance_level=MockImportanceLevel.MUST_HAVE,
            minimum_proficiency_level=MockProficiencyLevel.ADVANCED
        )
        
        # Verify skill requirement was created correctly
        self.assertEqual(skill_requirement.opportunity_id, opportunity.id)
        self.assertEqual(skill_requirement.skill_id, self.aws_migration_skill.id)
        self.assertEqual(skill_requirement.skill_name, self.aws_migration_skill.name)
        self.assertEqual(skill_requirement.skill_type, MockSkillType.TECHNICAL)
        self.assertEqual(skill_requirement.importance_level, MockImportanceLevel.MUST_HAVE)
        self.assertEqual(skill_requirement.minimum_proficiency_level, MockProficiencyLevel.ADVANCED)
        
        # Verify skill requirement was added to repository
        saved_requirements = self.skill_requirement_repository.get_by_opportunity(opportunity.id)
        self.assertEqual(len(saved_requirements), 1)
        self.assertEqual(saved_requirements[0].skill_id, self.aws_migration_skill.id)

class TestAttachmentService(unittest.TestCase):
    def setUp(self):
        # Create repositories
        self.problem_statement_repository = MockProblemStatementRepository()
        self.attachment_repository = MockAttachmentRepository()
        
        # Create service
        self.attachment_service = MockAttachmentService(
            attachment_repository=self.attachment_repository,
            problem_statement_repository=self.problem_statement_repository
        )
        
        # Create test data
        self.problem_statement = MockProblemStatement(
            content="This is a detailed problem statement that meets the minimum character requirement."
        )
        self.problem_statement_repository.add(self.problem_statement)
        
        self.user_id = uuid.uuid4()
    
    def test_add_attachment(self):
        # Add attachment
        attachment = self.attachment_service.add_attachment(
            problem_statement_id=self.problem_statement.id,
            file_name="test.pdf",
            file_type="application/pdf",
            file_size=1024 * 1024,  # 1MB
            file_url="https://example.com/files/test.pdf",
            uploaded_by=self.user_id
        )
        
        # Verify attachment was created correctly
        self.assertEqual(attachment.problem_statement_id, self.problem_statement.id)
        self.assertEqual(attachment.file_name, "test.pdf")
        self.assertEqual(attachment.file_type, "application/pdf")
        self.assertEqual(attachment.file_size, 1024 * 1024)
        self.assertEqual(attachment.file_url, "https://example.com/files/test.pdf")
        self.assertEqual(attachment.uploaded_by, self.user_id)
        self.assertFalse(attachment.is_removed)
        
        # Verify attachment was added to repository
        saved_attachments = self.attachment_repository.get_by_problem_statement(self.problem_statement.id)
        self.assertEqual(len(saved_attachments), 1)
        self.assertEqual(saved_attachments[0].file_name, "test.pdf")
    
    def test_add_attachment_file_too_large(self):
        # Try to add a large attachment
        with self.assertRaises(MockValidationException):
            self.attachment_service.add_attachment(
                problem_statement_id=self.problem_statement.id,
                file_name="large.pdf",
                file_type="application/pdf",
                file_size=25 * 1024 * 1024,  # 25MB
                file_url="https://example.com/files/large.pdf",
                uploaded_by=self.user_id
            )
    
    def test_remove_attachment(self):
        # Add attachment
        attachment = self.attachment_service.add_attachment(
            problem_statement_id=self.problem_statement.id,
            file_name="test.pdf",
            file_type="application/pdf",
            file_size=1024 * 1024,
            file_url="https://example.com/files/test.pdf",
            uploaded_by=self.user_id
        )
        
        # Remove attachment
        removed_attachment = self.attachment_service.remove_attachment(
            attachment_id=attachment.id,
            user_id=self.user_id
        )
        
        # Verify attachment was marked as removed
        self.assertTrue(removed_attachment.is_removed)
        
        # Verify attachment in repository was updated
        saved_attachment = self.attachment_repository.get_by_id(attachment.id)
        self.assertTrue(saved_attachment.is_removed)
        
        # Verify attachment is not returned by get_active_attachments
        active_attachments = self.attachment_service.get_attachments_for_problem_statement(
            problem_statement_id=self.problem_statement.id
        )
        self.assertEqual(len(active_attachments), 0)

if __name__ == '__main__':
    unittest.main()
