#!/usr/bin/env python3
"""
Script to fix import statements for the reorganized project structure.
"""

import os
import re
from pathlib import Path

def fix_imports_in_file(file_path: Path):
    """Fix imports in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Define import replacements based on file location
        if 'domain/enums' in str(file_path):
            # No changes needed for enum files
            pass
        elif 'domain/value_objects' in str(file_path):
            content = re.sub(r'^from skill_importance import', 'from ..enums.skill_importance import', content, flags=re.MULTILINE)
            content = re.sub(r'^from timeline_flexibility import', 'from ..enums.timeline_flexibility import', content, flags=re.MULTILINE)
        elif 'domain/entities' in str(file_path):
            content = re.sub(r'^from base_entity import', 'from .base_entity import', content, flags=re.MULTILINE)
            content = re.sub(r'^from aggregate_root import', 'from .aggregate_root import', content, flags=re.MULTILINE)
            content = re.sub(r'^from customer import', 'from .customer import', content, flags=re.MULTILINE)
            content = re.sub(r'^from problem_statement import', 'from .problem_statement import', content, flags=re.MULTILINE)
            content = re.sub(r'^from status_history import', 'from .status_history import', content, flags=re.MULTILINE)
            content = re.sub(r'^from status import', 'from ..enums.status import', content, flags=re.MULTILINE)
            content = re.sub(r'^from priority import', 'from ..enums.priority import', content, flags=re.MULTILINE)
            content = re.sub(r'^from skill_requirement import', 'from ..value_objects.skill_requirement import', content, flags=re.MULTILINE)
            content = re.sub(r'^from timeline_specification import', 'from ..value_objects.timeline_specification import', content, flags=re.MULTILINE)
            content = re.sub(r'^from geographic_requirement import', 'from ..value_objects.geographic_requirement import', content, flags=re.MULTILINE)
            content = re.sub(r'^from language_requirement import', 'from ..value_objects.language_requirement import', content, flags=re.MULTILINE)
            content = re.sub(r'^from document_attachment import', 'from ..value_objects.document_attachment import', content, flags=re.MULTILINE)
        elif 'domain/events' in str(file_path):
            content = re.sub(r'^from domain_event import', 'from .domain_event import', content, flags=re.MULTILINE)
        elif 'domain/services' in str(file_path):
            # Fix imports for domain services
            content = re.sub(r'^from opportunity import', 'from ..entities.opportunity import', content, flags=re.MULTILINE)
            content = re.sub(r'^from status import', 'from ..enums.status import', content, flags=re.MULTILINE)
            content = re.sub(r'^from priority import', 'from ..enums.priority import', content, flags=re.MULTILINE)
            content = re.sub(r'^from skill_requirement import', 'from ..value_objects.skill_requirement import', content, flags=re.MULTILINE)
            content = re.sub(r'^from timeline_specification import', 'from ..value_objects.timeline_specification import', content, flags=re.MULTILINE)
            content = re.sub(r'^from skill_importance import', 'from ..enums.skill_importance import', content, flags=re.MULTILINE)
            content = re.sub(r'^from timeline_flexibility import', 'from ..enums.timeline_flexibility import', content, flags=re.MULTILINE)
            content = re.sub(r'^from opportunity_validation_service import', 'from .opportunity_validation_service import', content, flags=re.MULTILINE)
        
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
                fix_imports_in_file(file_path)
    
    print("Import fixing completed!")

if __name__ == "__main__":
    main()
