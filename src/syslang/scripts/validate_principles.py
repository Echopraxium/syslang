#!/usr/bin/env python3
"""
Validate SysLang JSON files against their schemas
"""

import json
import jsonschema
from pathlib import Path
import sys

def load_schema(schema_name):
    """Load a JSON schema file"""
    schema_path = Path(__file__).parent / "schemas" / f"{schema_name}.json"
    with open(schema_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def validate_file(file_path, schema):
    """Validate a JSON file against a schema"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        jsonschema.validate(data, schema)
        print(f"✅ {file_path.name} is valid")
        return True
        
    except jsonschema.ValidationError as e:
        print(f"❌ {file_path.name} validation error:")
        print(f"   Path: {e.json_path}")
        print(f"   Error: {e.message}")
        if e.context:
            for sub_error in e.context:
                print(f"   Context: {sub_error.message}")
        return False
        
    except json.JSONDecodeError as e:
        print(f"❌ {file_path.name} JSON syntax error:")
        print(f"   Line {e.lineno}, Column {e.colno}: {e.msg}")
        return False

def main():
    """Validate all SysLang data files"""
    data_dir = Path(__file__).parent / "data"
    
    # Load schemas
    principles_schema = load_schema("principles_schema")
    patterns_schema = load_schema("patterns_schema")
    compatibility_schema = load_schema("compatibility_schema")
    
    print("🔍 Validating SysLang data files...")
    print("=" * 50)
    
    all_valid = True
    
    # Validate principles.json
    principles_file = data_dir / "principles.json"
    if principles_file.exists():
        all_valid &= validate_file(principles_file, principles_schema)
    else:
        print(f"⚠️  {principles_file.name} not found")
    
    # Validate patterns.json
    patterns_file = data_dir / "patterns.json"
    if patterns_file.exists():
        all_valid &= validate_file(patterns_file, patterns_schema)
    else:
        print(f"⚠️  {patterns_file.name} not found")
    
    # Validate compatibility.json
    compatibility_file = data_dir / "compatibility.json"
    if compatibility_file.exists():
        all_valid &= validate_file(compatibility_file, compatibility_schema)
    else:
        print(f"⚠️  {compatibility_file.name} not found")
    
    print("=" * 50)
    
    if all_valid:
        print("🎉 All files are valid!")
        sys.exit(0)
    else:
        print("❌ Some files failed validation")
        sys.exit(1)

if __name__ == "__main__":
    main()