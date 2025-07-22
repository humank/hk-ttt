"""
Test example demonstrating skills requirements management.
"""

import logging
from decimal import Decimal

# Import domain model components
from customer import Customer
from opportunity import Opportunity
from skill_requirement import SkillRequirement
from priority import Priority
from skill_importance import SkillImportance

# Import repositories
from in_memory_customer_repository import InMemoryCustomerRepository
from in_memory_opportunity_repository import InMemoryOpportunityRepository

# Import services
from skills_validation_service import SkillsValidationService
from skills_matching_preparation_service import SkillsMatchingPreparationService
from opportunity_validation_service import OpportunityValidationService
from opportunity_modification_service import OpportunityModificationService


def setup_logging():
    """Setup logging for the test."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def create_sample_opportunity():
    """Create a sample opportunity for testing."""
    # Setup repositories
    customer_repo = InMemoryCustomerRepository()
    opportunity_repo = InMemoryOpportunityRepository()
    
    # Create customer
    customer = Customer(
        name="Innovation Labs",
        industry="Technology",
        contact_email="projects@innovationlabs.com"
    )
    customer = customer_repo.save(customer)
    
    # Create opportunity
    opportunity = Opportunity(
        title="AI-Powered Analytics Platform",
        description="Build an AI-powered analytics platform for real-time data insights",
        customer_id=customer.id,
        sales_manager_id="sm_003",
        annual_recurring_revenue=Decimal("2000000"),
        priority=Priority.CRITICAL
    )
    
    opportunity = opportunity_repo.save(opportunity)
    return opportunity_repo, customer_repo, opportunity


def test_skill_requirements_management():
    """Test skill requirements management."""
    print("=== Testing Skill Requirements Management ===\n")
    
    # Setup
    opportunity_repo, customer_repo, opportunity = create_sample_opportunity()
    skills_validator = SkillsValidationService()
    
    print(f"Opportunity: {opportunity.title}")
    print(f"Initial skills count: {len(opportunity.skill_requirements)}")
    
    try:
        # Test 1: Add valid skill requirements
        print("\n1. Adding valid skill requirements...")
        
        skills_to_add = [
            {
                "skill_name": "Python",
                "skill_category": "Technical",
                "importance": "Must Have",
                "proficiency_level": "Expert",
                "description": "Advanced Python programming for AI/ML development"
            },
            {
                "skill_name": "Machine Learning",
                "skill_category": "Technical",
                "importance": "Must Have",
                "proficiency_level": "Advanced",
                "description": "ML algorithms and model development"
            },
            {
                "skill_name": "TensorFlow",
                "skill_category": "Technical",
                "importance": "Nice to Have",
                "proficiency_level": "Intermediate",
                "description": "Deep learning framework experience"
            },
            {
                "skill_name": "Leadership",
                "skill_category": "Soft",
                "importance": "Must Have",
                "description": "Team leadership and project management"
            },
            {
                "skill_name": "Healthcare",
                "skill_category": "Industry",
                "importance": "Nice to Have",
                "description": "Healthcare domain knowledge"
            }
        ]
        
        for skill_data in skills_to_add:
            # Validate skill requirement
            validation_errors = skills_validator.validate_skill_requirement(skill_data)
            if validation_errors:
                print(f"❌ Validation failed for {skill_data['skill_name']}: {validation_errors}")
                continue
            
            # Create and add skill requirement
            skill_req = SkillRequirement.from_dict(skill_data)
            opportunity.add_skill_requirement(skill_req)
            print(f"✅ Added skill: {skill_req.skill_name} ({skill_req.skill_category}, {skill_req.importance.value})")
        
        opportunity_repo.save(opportunity)
        print(f"\nTotal skills after addition: {len(opportunity.skill_requirements)}")
        print(f"Mandatory skills: {len(opportunity.mandatory_skills)}")
        print(f"Optional skills: {len(opportunity.optional_skills)}")
        
        # Test 2: Validate skill requirements collection
        print("\n2. Validating skill requirements collection...")
        collection_errors = skills_validator.validate_skill_requirements_collection(opportunity.skill_requirements)
        if collection_errors:
            print("⚠️  Collection validation warnings:")
            for error in collection_errors:
                print(f"   - {error}")
        else:
            print("✅ Skill requirements collection is valid")
        
        # Test 3: Get skill recommendations
        print("\n3. Getting skill recommendations...")
        recommendations = skills_validator.get_skill_recommendations(opportunity.skill_requirements)
        if recommendations:
            print("💡 Recommendations:")
            for rec in recommendations:
                print(f"   - {rec}")
        else:
            print("✅ No recommendations - skill set looks good")
        
        # Test 4: Calculate complexity score
        print("\n4. Calculating skill complexity score...")
        complexity = skills_validator.calculate_skill_complexity_score(opportunity.skill_requirements)
        print(f"✅ Complexity Analysis:")
        print(f"   Score: {complexity['score']}/100")
        print(f"   Complexity: {complexity['complexity']}")
        print(f"   Matching likelihood: {complexity['matching_likelihood']}")
        if complexity['factors']:
            print(f"   Factors: {', '.join(complexity['factors'])}")
        
        # Test 5: Test skill catalog validation
        print("\n5. Testing skill catalog validation...")
        test_skills = ["Python", "JavaScript", "AWS", "UnknownSkill", "React"]
        
        for skill_name in test_skills:
            result = skills_validator.validate_skill_against_catalog(skill_name, "Technical")
            if result["is_recognized"]:
                print(f"✅ {skill_name}: Recognized")
            else:
                suggestions_str = ", ".join(result["suggestions"]) if result["suggestions"] else "None"
                print(f"⚠️  {skill_name}: Not recognized (Suggestions: {suggestions_str})")
        
        print("\n✅ Skill requirements management tests completed!")
        
    except Exception as e:
        print(f"❌ Error during skills management: {str(e)}")
        import traceback
        traceback.print_exc()


def test_skill_modification():
    """Test skill requirements modification."""
    print("\n=== Testing Skill Requirements Modification ===\n")
    
    # Setup
    opportunity_repo, customer_repo, opportunity = create_sample_opportunity()
    validation_service = OpportunityValidationService()
    modification_service = OpportunityModificationService(validation_service)
    
    # Add initial skills
    initial_skills = [
        SkillRequirement("Java", "Technical", SkillImportance.MUST_HAVE, "Advanced"),
        SkillRequirement("Spring Boot", "Technical", SkillImportance.NICE_TO_HAVE, "Intermediate"),
        SkillRequirement("Communication", "Soft", SkillImportance.MUST_HAVE)
    ]
    
    for skill in initial_skills:
        opportunity.add_skill_requirement(skill)
    
    opportunity_repo.save(opportunity)
    print(f"Initial skills: {[s.skill_name for s in opportunity.skill_requirements]}")
    
    try:
        # Test 1: Add new skills
        print("\n1. Adding new skills...")
        skill_updates = {
            "add_skills": [
                {
                    "skill_name": "Docker",
                    "skill_category": "Technical",
                    "importance": "Must Have",
                    "proficiency_level": "Intermediate",
                    "description": "Containerization technology"
                },
                {
                    "skill_name": "Kubernetes",
                    "skill_category": "Technical",
                    "importance": "Nice to Have",
                    "proficiency_level": "Beginner",
                    "description": "Container orchestration"
                }
            ]
        }
        
        result = modification_service.update_skill_requirements(
            opportunity, skill_updates, "sm_003"
        )
        
        if result["success"]:
            print(f"✅ {result['message']}")
            print(f"   Changes: {result['changes_made']}")
            print(f"   Total skills: {result['total_skills']}")
            print(f"   Mandatory skills: {result['mandatory_skills']}")
            opportunity_repo.save(opportunity)
        else:
            print(f"❌ Failed to add skills: {result['errors']}")
        
        # Test 2: Remove skills
        print("\n2. Removing skills...")
        skill_updates = {
            "remove_skills": [
                {
                    "skill_name": "Spring Boot",
                    "skill_category": "Technical"
                }
            ]
        }
        
        result = modification_service.update_skill_requirements(
            opportunity, skill_updates, "sm_003"
        )
        
        if result["success"]:
            print(f"✅ {result['message']}")
            print(f"   Changes: {result['changes_made']}")
            opportunity_repo.save(opportunity)
        else:
            print(f"❌ Failed to remove skills: {result['errors']}")
        
        # Test 3: Try to add duplicate skill
        print("\n3. Testing duplicate skill addition...")
        skill_updates = {
            "add_skills": [
                {
                    "skill_name": "Java",  # Duplicate
                    "skill_category": "Technical",
                    "importance": "Must Have",
                    "proficiency_level": "Expert"
                }
            ]
        }
        
        result = modification_service.update_skill_requirements(
            opportunity, skill_updates, "sm_003"
        )
        
        if not result["success"]:
            print(f"✅ Correctly rejected duplicate skill: {result['errors']}")
        else:
            print("❌ Should have rejected duplicate skill")
        
        # Final skills list
        print(f"\nFinal skills: {[s.skill_name for s in opportunity.skill_requirements]}")
        
        print("\n✅ Skill modification tests completed!")
        
    except Exception as e:
        print(f"❌ Error during skill modification: {str(e)}")
        import traceback
        traceback.print_exc()


def test_matching_preparation():
    """Test skills matching preparation."""
    print("\n=== Testing Skills Matching Preparation ===\n")
    
    # Setup
    opportunity_repo, customer_repo, opportunity = create_sample_opportunity()
    matching_service = SkillsMatchingPreparationService()
    
    # Add comprehensive skill set
    skills = [
        SkillRequirement("Python", "Technical", SkillImportance.MUST_HAVE, "Advanced"),
        SkillRequirement("AWS", "Technical", SkillImportance.MUST_HAVE, "Intermediate"),
        SkillRequirement("Docker", "Technical", SkillImportance.NICE_TO_HAVE, "Intermediate"),
        SkillRequirement("Communication", "Soft", SkillImportance.MUST_HAVE),
        SkillRequirement("Leadership", "Soft", SkillImportance.NICE_TO_HAVE),
        SkillRequirement("Financial Services", "Industry", SkillImportance.NICE_TO_HAVE)
    ]
    
    for skill in skills:
        opportunity.add_skill_requirement(skill)
    
    # Add problem statement and timeline to make it ready for matching
    from problem_statement import ProblemStatement
    from timeline_specification import TimelineSpecification
    from timeline_flexibility import TimelineFlexibility
    from datetime import date, timedelta
    
    problem_statement = ProblemStatement(
        title="AI Platform Development",
        description="Develop a comprehensive AI platform with advanced analytics capabilities for financial services clients."
    )
    opportunity.set_problem_statement(problem_statement)
    
    timeline = TimelineSpecification(
        expected_start_date=date.today() + timedelta(days=60),
        expected_duration_days=240,
        flexibility=TimelineFlexibility.FLEXIBLE
    )
    opportunity.set_timeline_specification(timeline)
    
    opportunity_repo.save(opportunity)
    
    try:
        # Test 1: Validate matching readiness
        print("1. Validating matching readiness...")
        readiness = matching_service.validate_matching_readiness(opportunity)
        print(f"✅ Readiness Assessment:")
        print(f"   Ready: {readiness['is_ready']}")
        print(f"   Score: {readiness['readiness_score']}/100")
        if readiness['issues']:
            print(f"   Issues: {readiness['issues']}")
        if readiness['warnings']:
            print(f"   Warnings: {readiness['warnings']}")
        
        if not readiness['is_ready']:
            print("❌ Opportunity not ready for matching")
            return
        
        # Test 2: Prepare matching criteria
        print("\n2. Preparing matching criteria...")
        criteria = matching_service.prepare_matching_criteria(opportunity)
        print(f"✅ Matching Criteria Prepared:")
        print(f"   Opportunity: {criteria['opportunity_title']}")
        print(f"   Priority: {criteria['priority']} (weight: {criteria['priority_weight']})")
        print(f"   ARR: ${criteria['annual_recurring_revenue']}")
        print(f"   Minimum match score: {criteria['minimum_match_score']}")
        
        # Skills breakdown
        skills_info = criteria['skills']
        print(f"\n   Skills Summary:")
        print(f"   - Total skills: {skills_info['total_skills']}")
        print(f"   - Mandatory: {skills_info['mandatory_count']}")
        print(f"   - Optional: {skills_info['optional_count']}")
        
        print(f"\n   Mandatory Skills:")
        for skill in skills_info['mandatory_skills']:
            synonyms_str = ", ".join(skill['synonyms']) if skill['synonyms'] else "None"
            print(f"   - {skill['name']} ({skill['category']}) - Synonyms: {synonyms_str}")
        
        print(f"\n   Optional Skills:")
        for skill in skills_info['optional_skills']:
            print(f"   - {skill['name']} ({skill['category']})")
        
        # Matching weights
        print(f"\n   Matching Weights:")
        for weight_type, weight_value in criteria['matching_weights'].items():
            print(f"   - {weight_type}: {weight_value}")
        
        # Test 3: Generate matching query
        print("\n3. Generating matching query...")
        query = matching_service.generate_matching_query(opportunity)
        print(f"✅ Matching Query Generated:")
        print(f"   Query type: {query['query_type']}")
        print(f"   Mandatory skills filter: {query['filters']['mandatory_skills']}")
        print(f"   Skill categories: {query['filters']['skill_categories']}")
        print(f"   Timeline: {query['filters']['timeline_start']} to {query['filters']['timeline_end']}")
        print(f"   Remote work: {query['filters']['remote_work']}")
        print(f"   Minimum score: {query['scoring']['minimum_score']}")
        
        # Test 4: Skill alternatives
        print("\n4. Testing skill alternatives...")
        for skill in opportunity.skill_requirements[:3]:  # Test first 3 skills
            alternatives = matching_service.suggest_skill_alternatives(skill)
            if alternatives:
                print(f"   Alternatives for {skill.skill_name}:")
                for alt in alternatives:
                    print(f"   - {alt['skill_name']}: {alt['reason']}")
            else:
                print(f"   No alternatives found for {skill.skill_name}")
        
        print("\n✅ Matching preparation tests completed!")
        
    except Exception as e:
        print(f"❌ Error during matching preparation: {str(e)}")
        import traceback
        traceback.print_exc()


def test_skill_validation_edge_cases():
    """Test edge cases in skill validation."""
    print("\n=== Testing Skill Validation Edge Cases ===\n")
    
    skills_validator = SkillsValidationService()
    
    # Test 1: Invalid skill data
    print("1. Testing invalid skill data...")
    invalid_skills = [
        {
            "skill_name": "",  # Empty name
            "skill_category": "Technical",
            "importance": "Must Have"
        },
        {
            "skill_name": "Python",
            "skill_category": "InvalidCategory",  # Invalid category
            "importance": "Must Have"
        },
        {
            "skill_name": "Java",
            "skill_category": "Technical",
            "importance": "InvalidImportance"  # Invalid importance
        },
        {
            "skill_name": "AWS",
            "skill_category": "Technical",
            "importance": "Must Have",
            "proficiency_level": "InvalidLevel"  # Invalid proficiency
        }
    ]
    
    for i, skill_data in enumerate(invalid_skills, 1):
        errors = skills_validator.validate_skill_requirement(skill_data)
        if errors:
            print(f"   ✅ Test {i}: Correctly caught errors: {errors}")
        else:
            print(f"   ❌ Test {i}: Should have caught validation errors")
    
    # Test 2: Empty skills collection
    print("\n2. Testing empty skills collection...")
    errors = skills_validator.validate_skill_requirements_collection([])
    if errors:
        print(f"   ✅ Correctly rejected empty collection: {errors}")
    else:
        print("   ❌ Should have rejected empty collection")
    
    # Test 3: All optional skills (no mandatory)
    print("\n3. Testing collection with no mandatory skills...")
    optional_only_skills = [
        SkillRequirement("Python", "Technical", SkillImportance.NICE_TO_HAVE),
        SkillRequirement("Java", "Technical", SkillImportance.NICE_TO_HAVE)
    ]
    
    errors = skills_validator.validate_skill_requirements_collection(optional_only_skills)
    if errors:
        print(f"   ✅ Correctly flagged missing mandatory skills: {errors}")
    else:
        print("   ❌ Should have flagged missing mandatory skills")
    
    # Test 4: Too many skills
    print("\n4. Testing collection with too many skills...")
    many_skills = []
    for i in range(20):  # Create 20 skills
        skill = SkillRequirement(f"Skill{i}", "Technical", SkillImportance.MUST_HAVE)
        many_skills.append(skill)
    
    errors = skills_validator.validate_skill_requirements_collection(many_skills)
    if any("too many" in error.lower() for error in errors):
        print(f"   ✅ Correctly flagged too many skills")
    else:
        print("   ⚠️  Did not flag too many skills (might be acceptable)")
    
    print("\n✅ Edge case validation tests completed!")


if __name__ == "__main__":
    setup_logging()
    test_skill_requirements_management()
    test_skill_modification()
    test_matching_preparation()
    test_skill_validation_edge_cases()
