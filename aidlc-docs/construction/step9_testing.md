# Step 9: Implement Testing

This document outlines the testing strategy and implementation for the Opportunity Management Service.

## Testing Strategy

Our testing strategy follows the testing pyramid approach:

1. **Unit Tests**: Test individual components in isolation
2. **Integration Tests**: Test interactions between components
3. **API Tests**: Test the API endpoints
4. **Load Tests**: Test performance under load
5. **Security Tests**: Test for security vulnerabilities

## Unit Tests

### Domain Model Tests

We'll use Python's unittest framework to test the domain model:

```python
import unittest
from datetime import datetime
from opportunity_management_service.domain.model import (
    Opportunity, ProblemStatement, SkillRequirement, 
    TimelineRequirement, OpportunityStatus, Attachment
)

class OpportunityTests(unittest.TestCase):
    def test_create_opportunity(self):
        # Arrange
        opportunity_id = "123"
        title = "Test Opportunity"
        description = "Test Description"
        client_name = "Test Client"
        estimated_budget = 10000.0
        estimated_start_date = datetime(2023, 1, 1)
        estimated_end_date = datetime(2023, 12, 31)
        status = OpportunityStatus.DRAFT
        created_by = "user123"
        
        # Act
        opportunity = Opportunity(
            id=opportunity_id,
            title=title,
            description=description,
            client_name=client_name,
            estimated_budget=estimated_budget,
            estimated_start_date=estimated_start_date,
            estimated_end_date=estimated_end_date,
            status=status,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            created_by=created_by,
            problem_statements=[],
            skill_requirements=[],
            timeline_requirements=[],
            attachments=[],
            change_history=[]
        )
        
        # Assert
        self.assertEqual(opportunity.id, opportunity_id)
        self.assertEqual(opportunity.title, title)
        self.assertEqual(opportunity.description, description)
        self.assertEqual(opportunity.client_name, client_name)
        self.assertEqual(opportunity.estimated_budget, estimated_budget)
        self.assertEqual(opportunity.estimated_start_date, estimated_start_date)
        self.assertEqual(opportunity.estimated_end_date, estimated_end_date)
        self.assertEqual(opportunity.status, status)
        self.assertEqual(opportunity.created_by, created_by)
        self.assertEqual(len(opportunity.problem_statements), 0)
        self.assertEqual(len(opportunity.skill_requirements), 0)
        self.assertEqual(len(opportunity.timeline_requirements), 0)
        self.assertEqual(len(opportunity.attachments), 0)
        self.assertEqual(len(opportunity.change_history), 0)
    
    def test_add_problem_statement(self):
        # Arrange
        opportunity = Opportunity(
            id="123",
            title="Test Opportunity",
            description="Test Description",
            client_name="Test Client",
            estimated_budget=10000.0,
            estimated_start_date=datetime(2023, 1, 1),
            estimated_end_date=datetime(2023, 12, 31),
            status=OpportunityStatus.DRAFT,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            created_by="user123",
            problem_statements=[],
            skill_requirements=[],
            timeline_requirements=[],
            attachments=[],
            change_history=[]
        )
        
        problem_statement = ProblemStatement(
            id="ps1",
            opportunity_id=opportunity.id,
            description="Test Problem Statement",
            priority=1,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Act
        opportunity.add_problem_statement(problem_statement)
        
        # Assert
        self.assertEqual(len(opportunity.problem_statements), 1)
        self.assertEqual(opportunity.problem_statements[0].id, "ps1")
        self.assertEqual(opportunity.problem_statements[0].description, "Test Problem Statement")
    
    def test_change_status(self):
        # Arrange
        opportunity = Opportunity(
            id="123",
            title="Test Opportunity",
            description="Test Description",
            client_name="Test Client",
            estimated_budget=10000.0,
            estimated_start_date=datetime(2023, 1, 1),
            estimated_end_date=datetime(2023, 12, 31),
            status=OpportunityStatus.DRAFT,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            created_by="user123",
            problem_statements=[],
            skill_requirements=[],
            timeline_requirements=[],
            attachments=[],
            change_history=[]
        )
        
        # Act
        opportunity.change_status(OpportunityStatus.SUBMITTED)
        
        # Assert
        self.assertEqual(opportunity.status, OpportunityStatus.SUBMITTED)
```

### Repository Tests

We'll use mocks to test the repositories:

```python
import unittest
from unittest.mock import MagicMock
from datetime import datetime
from opportunity_management_service.domain.model import Opportunity, OpportunityStatus
from opportunity_management_service.adapters.repositories import OpportunityRepository

class OpportunityRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.db_session = MagicMock()
        self.repository = OpportunityRepository(self.db_session)
    
    def test_create(self):
        # Arrange
        opportunity = Opportunity(
            id="123",
            title="Test Opportunity",
            description="Test Description",
            client_name="Test Client",
            estimated_budget=10000.0,
            estimated_start_date=datetime(2023, 1, 1),
            estimated_end_date=datetime(2023, 12, 31),
            status=OpportunityStatus.DRAFT,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            created_by="user123",
            problem_statements=[],
            skill_requirements=[],
            timeline_requirements=[],
            attachments=[],
            change_history=[]
        )
        
        # Act
        self.repository.create(opportunity)
        
        # Assert
        self.db_session.add.assert_called_once()
        self.db_session.commit.assert_called_once()
    
    def test_get_by_id(self):
        # Arrange
        opportunity_id = "123"
        opportunity = Opportunity(
            id=opportunity_id,
            title="Test Opportunity",
            description="Test Description",
            client_name="Test Client",
            estimated_budget=10000.0,
            estimated_start_date=datetime(2023, 1, 1),
            estimated_end_date=datetime(2023, 12, 31),
            status=OpportunityStatus.DRAFT,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            created_by="user123",
            problem_statements=[],
            skill_requirements=[],
            timeline_requirements=[],
            attachments=[],
            change_history=[]
        )
        
        self.db_session.query().filter_by().first.return_value = opportunity
        
        # Act
        result = self.repository.get_by_id(opportunity_id)
        
        # Assert
        self.assertEqual(result, opportunity)
        self.db_session.query.assert_called_once()
```

### Service Tests

We'll use mocks to test the service layer:

```python
import unittest
from unittest.mock import MagicMock
from datetime import datetime
from opportunity_management_service.domain.model import (
    Opportunity, OpportunityStatus, User, Role
)
from opportunity_management_service.service.opportunity_service import OpportunityService
from opportunity_management_service.service.exceptions import ValidationError, AuthorizationError

class OpportunityServiceTests(unittest.TestCase):
    def setUp(self):
        self.opportunity_repo = MagicMock()
        self.problem_statement_repo = MagicMock()
        self.skill_requirement_repo = MagicMock()
        self.timeline_requirement_repo = MagicMock()
        self.attachment_repo = MagicMock()
        self.change_record_repo = MagicMock()
        
        self.service = OpportunityService(
            self.opportunity_repo,
            self.problem_statement_repo,
            self.skill_requirement_repo,
            self.timeline_requirement_repo,
            self.attachment_repo,
            self.change_record_repo
        )
    
    def test_create_opportunity_success(self):
        # Arrange
        opportunity = Opportunity(
            id="123",
            title="Test Opportunity",
            description="Test Description",
            client_name="Test Client",
            estimated_budget=10000.0,
            estimated_start_date=datetime(2023, 1, 1),
            estimated_end_date=datetime(2023, 12, 31),
            status=OpportunityStatus.DRAFT,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            created_by=None,
            problem_statements=[],
            skill_requirements=[],
            timeline_requirements=[],
            attachments=[],
            change_history=[]
        )
        
        user = User(
            id="user123",
            username="testuser",
            email="test@example.com",
            role=Role.SALES_MANAGER
        )
        
        self.opportunity_repo.create.return_value = opportunity
        
        # Act
        result = self.service.create_opportunity(opportunity, user)
        
        # Assert
        self.assertEqual(result, opportunity)
        self.assertEqual(opportunity.created_by, user.id)
        self.opportunity_repo.create.assert_called_once_with(opportunity)
        self.change_record_repo.create.assert_called_once()
    
    def test_create_opportunity_validation_error(self):
        # Arrange
        opportunity = Opportunity(
            id="123",
            title="",  # Empty title should fail validation
            description="Test Description",
            client_name="Test Client",
            estimated_budget=10000.0,
            estimated_start_date=datetime(2023, 1, 1),
            estimated_end_date=datetime(2023, 12, 31),
            status=OpportunityStatus.DRAFT,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            created_by=None,
            problem_statements=[],
            skill_requirements=[],
            timeline_requirements=[],
            attachments=[],
            change_history=[]
        )
        
        user = User(
            id="user123",
            username="testuser",
            email="test@example.com",
            role=Role.SALES_MANAGER
        )
        
        # Act & Assert
        with self.assertRaises(ValidationError):
            self.service.create_opportunity(opportunity, user)
    
    def test_create_opportunity_authorization_error(self):
        # Arrange
        opportunity = Opportunity(
            id="123",
            title="Test Opportunity",
            description="Test Description",
            client_name="Test Client",
            estimated_budget=10000.0,
            estimated_start_date=datetime(2023, 1, 1),
            estimated_end_date=datetime(2023, 12, 31),
            status=OpportunityStatus.DRAFT,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            created_by=None,
            problem_statements=[],
            skill_requirements=[],
            timeline_requirements=[],
            attachments=[],
            change_history=[]
        )
        
        user = User(
            id="user123",
            username="testuser",
            email="test@example.com",
            role=Role.SALES_REPRESENTATIVE  # Sales reps can't create opportunities
        )
        
        # Act & Assert
        with self.assertRaises(AuthorizationError):
            self.service.create_opportunity(opportunity, user)
```

## Integration Tests

### Database Integration Tests

We'll use a test database to test the repositories:

```python
import unittest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from opportunity_management_service.domain.model import (
    Opportunity, OpportunityStatus, Base
)
from opportunity_management_service.adapters.repositories import OpportunityRepository

class OpportunityRepositoryIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create test database
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
    
    def setUp(self):
        # Create a new session for each test
        self.session = self.Session()
        self.repository = OpportunityRepository(self.session)
    
    def tearDown(self):
        # Close session after each test
        self.session.close()
    
    def test_create_and_get(self):
        # Arrange
        opportunity = Opportunity(
            id="123",
            title="Test Opportunity",
            description="Test Description",
            client_name="Test Client",
            estimated_budget=10000.0,
            estimated_start_date=datetime(2023, 1, 1),
            estimated_end_date=datetime(2023, 12, 31),
            status=OpportunityStatus.DRAFT,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            created_by="user123",
            problem_statements=[],
            skill_requirements=[],
            timeline_requirements=[],
            attachments=[],
            change_history=[]
        )
        
        # Act
        self.repository.create(opportunity)
        result = self.repository.get_by_id("123")
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.id, "123")
        self.assertEqual(result.title, "Test Opportunity")
        self.assertEqual(result.description, "Test Description")
        self.assertEqual(result.client_name, "Test Client")
        self.assertEqual(result.estimated_budget, 10000.0)
        self.assertEqual(result.status, OpportunityStatus.DRAFT)
        self.assertEqual(result.created_by, "user123")
```

### Service Integration Tests

We'll test the service layer with real repositories:

```python
import unittest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from opportunity_management_service.domain.model import (
    Opportunity, OpportunityStatus, User, Role, Base
)
from opportunity_management_service.adapters.repositories import (
    OpportunityRepository, ProblemStatementRepository,
    SkillRequirementRepository, TimelineRequirementRepository,
    AttachmentRepository, ChangeRecordRepository
)
from opportunity_management_service.service.opportunity_service import OpportunityService

class OpportunityServiceIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create test database
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
    
    def setUp(self):
        # Create a new session for each test
        self.session = self.Session()
        
        # Create repositories
        self.opportunity_repo = OpportunityRepository(self.session)
        self.problem_statement_repo = ProblemStatementRepository(self.session)
        self.skill_requirement_repo = SkillRequirementRepository(self.session)
        self.timeline_requirement_repo = TimelineRequirementRepository(self.session)
        self.attachment_repo = AttachmentRepository(self.session)
        self.change_record_repo = ChangeRecordRepository(self.session)
        
        # Create service
        self.service = OpportunityService(
            self.opportunity_repo,
            self.problem_statement_repo,
            self.skill_requirement_repo,
            self.timeline_requirement_repo,
            self.attachment_repo,
            self.change_record_repo
        )
        
        # Create test user
        self.user = User(
            id="user123",
            username="testuser",
            email="test@example.com",
            role=Role.SALES_MANAGER
        )
    
    def tearDown(self):
        # Close session after each test
        self.session.close()
    
    def test_create_opportunity(self):
        # Arrange
        opportunity = Opportunity(
            id="123",
            title="Test Opportunity",
            description="Test Description",
            client_name="Test Client",
            estimated_budget=10000.0,
            estimated_start_date=datetime(2023, 1, 1),
            estimated_end_date=datetime(2023, 12, 31),
            status=OpportunityStatus.DRAFT,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            created_by=None,
            problem_statements=[],
            skill_requirements=[],
            timeline_requirements=[],
            attachments=[],
            change_history=[]
        )
        
        # Act
        created_opportunity = self.service.create_opportunity(opportunity, self.user)
        
        # Assert
        self.assertEqual(created_opportunity.id, "123")
        self.assertEqual(created_opportunity.created_by, "user123")
        
        # Verify it's in the database
        db_opportunity = self.opportunity_repo.get_by_id("123")
        self.assertIsNotNone(db_opportunity)
        self.assertEqual(db_opportunity.title, "Test Opportunity")
        
        # Verify change record was created
        change_records = self.change_record_repo.get_by_entity_id("123")
        self.assertEqual(len(change_records), 1)
        self.assertEqual(change_records[0].entity_type, "Opportunity")
        self.assertEqual(change_records[0].field_name, "status")
        self.assertEqual(change_records[0].new_value, "DRAFT")
```

## API Tests

We'll use FastAPI's TestClient to test the API endpoints:

```python
import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json
from opportunity_management_service.api.app import app
from opportunity_management_service.domain.model import Base
from opportunity_management_service.adapters.repositories import get_session

class APITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create test database
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
        
        # Override the get_session dependency
        def override_get_session():
            session = cls.Session()
            try:
                yield session
            finally:
                session.close()
        
        app.dependency_overrides[get_session] = override_get_session
        
        # Create test client
        cls.client = TestClient(app)
        
        # Create test token
        cls.token = "test_token"  # In a real test, we would create a valid JWT token
    
    def test_create_opportunity(self):
        # Arrange
        opportunity_data = {
            "title": "Test Opportunity",
            "description": "Test Description",
            "client_name": "Test Client",
            "estimated_budget": 10000.0,
            "estimated_start_date": "2023-01-01T00:00:00Z",
            "estimated_end_date": "2023-12-31T00:00:00Z",
            "status": "DRAFT"
        }
        
        # Act
        response = self.client.post(
            "/api/v1/opportunities",
            json=opportunity_data,
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        # Assert
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIsNotNone(data["id"])
        self.assertEqual(data["title"], "Test Opportunity")
        self.assertEqual(data["description"], "Test Description")
        self.assertEqual(data["client_name"], "Test Client")
        self.assertEqual(data["estimated_budget"], 10000.0)
        self.assertEqual(data["status"], "DRAFT")
    
    def test_get_opportunity(self):
        # Arrange - Create an opportunity first
        opportunity_data = {
            "title": "Test Opportunity",
            "description": "Test Description",
            "client_name": "Test Client",
            "estimated_budget": 10000.0,
            "estimated_start_date": "2023-01-01T00:00:00Z",
            "estimated_end_date": "2023-12-31T00:00:00Z",
            "status": "DRAFT"
        }
        
        create_response = self.client.post(
            "/api/v1/opportunities",
            json=opportunity_data,
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        opportunity_id = create_response.json()["id"]
        
        # Act
        response = self.client.get(
            f"/api/v1/opportunities/{opportunity_id}",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        # Assert
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], opportunity_id)
        self.assertEqual(data["title"], "Test Opportunity")
```

## Load Tests

We'll use Locust to test the API performance under load:

```python
from locust import HttpUser, task, between

class OpportunityUser(HttpUser):
    wait_time = between(1, 3)
    token = "test_token"  # In a real test, we would create a valid JWT token
    
    def on_start(self):
        # Create an opportunity to use in the tests
        self.opportunity_id = self.create_opportunity()
    
    def create_opportunity(self):
        opportunity_data = {
            "title": "Test Opportunity",
            "description": "Test Description",
            "client_name": "Test Client",
            "estimated_budget": 10000.0,
            "estimated_start_date": "2023-01-01T00:00:00Z",
            "estimated_end_date": "2023-12-31T00:00:00Z",
            "status": "DRAFT"
        }
        
        response = self.client.post(
            "/api/v1/opportunities",
            json=opportunity_data,
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        return response.json()["id"]
    
    @task(3)
    def get_opportunity(self):
        self.client.get(
            f"/api/v1/opportunities/{self.opportunity_id}",
            headers={"Authorization": f"Bearer {self.token}"}
        )
    
    @task(1)
    def list_opportunities(self):
        self.client.get(
            "/api/v1/opportunities",
            headers={"Authorization": f"Bearer {self.token}"}
        )
    
    @task(1)
    def update_opportunity(self):
        opportunity_data = {
            "title": f"Updated Opportunity {self.environment.runner.user_count}"
        }
        
        self.client.put(
            f"/api/v1/opportunities/{self.opportunity_id}",
            json=opportunity_data,
            headers={"Authorization": f"Bearer {self.token}"}
        )
```

## Security Tests

We'll use OWASP ZAP to test for security vulnerabilities:

```bash
#!/bin/bash

# Start the API
python -m opportunity_management_service.api.app &
API_PID=$!

# Wait for the API to start
sleep 5

# Run ZAP scan
docker run --rm -v $(pwd)/zap-report:/zap/wrk/ owasp/zap2docker-stable zap-baseline.py \
    -t http://host.docker.internal:8000/api/v1/ \
    -r zap-report.html

# Stop the API
kill $API_PID
```

## Test Automation

We'll set up a test automation pipeline using GitHub Actions:

```yaml
name: Test

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run unit tests
      run: |
        python -m unittest discover -s tests/unit
    
    - name: Run integration tests
      run: |
        python -m unittest discover -s tests/integration
    
    - name: Run API tests
      run: |
        python -m unittest discover -s tests/api
    
    - name: Run security tests
      run: |
        bash tests/security/run_zap_scan.sh
```

## Test Coverage

We'll use coverage.py to measure test coverage:

```bash
#!/bin/bash

# Run tests with coverage
coverage run --source=opportunity_management_service -m unittest discover

# Generate coverage report
coverage report -m

# Generate HTML report
coverage html
```

## Next Steps

1. Implement all unit tests for domain model, repositories, and services
2. Implement integration tests for database interactions
3. Implement API tests for all endpoints
4. Set up load testing environment
5. Set up security testing environment
6. Configure test automation pipeline
7. Set up test coverage reporting
