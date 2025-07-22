#!/usr/bin/env python3
"""
Comprehensive script to fix all import statements in the project.
"""

import os
import re
from pathlib import Path

def fix_imports_comprehensive(file_path: Path):
    """Fix imports comprehensively based on file location."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Infrastructure repositories
        if 'infrastructure/repositories' in str(file_path):
            content = re.sub(r'^from opportunity_repository import', 'from .opportunity_repository import', content, flags=re.MULTILINE)
            content = re.sub(r'^from customer_repository import', 'from .customer_repository import', content, flags=re.MULTILINE)
            content = re.sub(r'^from opportunity import', 'from ...domain.entities.opportunity import', content, flags=re.MULTILINE)
            content = re.sub(r'^from customer import', 'from ...domain.entities.customer import', content, flags=re.MULTILINE)
            content = re.sub(r'^from status import', 'from ...domain.enums.status import', content, flags=re.MULTILINE)
            content = re.sub(r'^from priority import', 'from ...domain.enums.priority import', content, flags=re.MULTILINE)
        
        # Application services
        elif 'application/services' in str(file_path):
            content = re.sub(r'^from opportunity import', 'from ...domain.entities.opportunity import', content, flags=re.MULTILINE)
            content = re.sub(r'^from customer import', 'from ...domain.entities.customer import', content, flags=re.MULTILINE)
            content = re.sub(r'^from problem_statement import', 'from ...domain.entities.problem_statement import', content, flags=re.MULTILINE)
            content = re.sub(r'^from skill_requirement import', 'from ...domain.value_objects.skill_requirement import', content, flags=re.MULTILINE)
            content = re.sub(r'^from timeline_specification import', 'from ...domain.value_objects.timeline_specification import', content, flags=re.MULTILINE)
            content = re.sub(r'^from geographic_requirement import', 'from ...domain.value_objects.geographic_requirement import', content, flags=re.MULTILINE)
            content = re.sub(r'^from language_requirement import', 'from ...domain.value_objects.language_requirement import', content, flags=re.MULTILINE)
            content = re.sub(r'^from priority import', 'from ...domain.enums.priority import', content, flags=re.MULTILINE)
            content = re.sub(r'^from status import', 'from ...domain.enums.status import', content, flags=re.MULTILINE)
            content = re.sub(r'^from opportunity_repository import', 'from ...infrastructure.repositories.opportunity_repository import', content, flags=re.MULTILINE)
            content = re.sub(r'^from customer_repository import', 'from ...infrastructure.repositories.customer_repository import', content, flags=re.MULTILINE)
            content = re.sub(r'^from opportunity_validation_service import', 'from ...domain.services.opportunity_validation_service import', content, flags=re.MULTILINE)
            content = re.sub(r'^from status_transition_service import', 'from ...domain.services.status_transition_service import', content, flags=re.MULTILINE)
            content = re.sub(r'^from opportunity_modification_service import', 'from ...domain.services.opportunity_modification_service import', content, flags=re.MULTILINE)
            content = re.sub(r'^from skills_matching_preparation_service import', 'from ...domain.services.skills_matching_preparation_service import', content, flags=re.MULTILINE)
            content = re.sub(r'^from event_dispatcher import', 'from ...infrastructure.event_handling.event_dispatcher import', content, flags=re.MULTILINE)
        
        # Application queries
        elif 'application/queries' in str(file_path):
            content = re.sub(r'^from opportunity import', 'from ...domain.entities.opportunity import', content, flags=re.MULTILINE)
            content = re.sub(r'^from customer import', 'from ...domain.entities.customer import', content, flags=re.MULTILINE)
            content = re.sub(r'^from status import', 'from ...domain.enums.status import', content, flags=re.MULTILINE)
            content = re.sub(r'^from priority import', 'from ...domain.enums.priority import', content, flags=re.MULTILINE)
            content = re.sub(r'^from opportunity_repository import', 'from ...infrastructure.repositories.opportunity_repository import', content, flags=re.MULTILINE)
            content = re.sub(r'^from customer_repository import', 'from ...infrastructure.repositories.customer_repository import', content, flags=re.MULTILINE)
        
        # Infrastructure event handling
        elif 'infrastructure/event_handling' in str(file_path):
            content = re.sub(r'^from domain_event import', 'from ...domain.events.domain_event import', content, flags=re.MULTILINE)
        
        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed imports in: {file_path}")
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def main():
    """Main function to fix all imports."""
    project_root = Path(__file__).parent.parent
    src_dir = project_root / "src" / "opportunity_management"
    
    # Process all Python files
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                file_path = Path(root) / file
                fix_imports_comprehensive(file_path)
    
    print("Comprehensive import fixing completed!")

if __name__ == "__main__":
    main()
