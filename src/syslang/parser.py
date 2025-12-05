"""Parser for SysLang YAML files"""
import yaml
from typing import Dict, Any, List
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Principle:
    """Represents a principle in a SysLang model"""
    name: str
    parameters: Dict[str, Any]
    confidence: float = 1.0

@dataclass
class SystemModel:
    """Represents a complete SysLang model"""
    name: str
    domain: str
    scale: str
    description: str = ""
    principles: List[Principle] = None
    components: List[Dict] = None
    relations: List[Dict] = None
    tests: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.principles is None:
            self.principles = []
        if self.components is None:
            self.components = []
        if self.relations is None:
            self.relations = []
        if self.tests is None:
            self.tests = {}

def load_syslang(filepath: str) -> SystemModel:
    """
    Load and parse a SysLang YAML file
    
    Args:
        filepath: Path to the .syslang.yml file
        
    Returns:
        SystemModel object
        
    Raises:
        ValueError: If the file is invalid
        FileNotFoundError: If file doesn't exist
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # Validate basic structure
    if not isinstance(data, dict):
        raise ValueError("Invalid file format: expected YAML dictionary")
    
    system_data = data.get('system', {})
    if not system_data:
        raise ValueError("Missing 'system' section")
    
    # Extract system info
    name = system_data.get('name', 'Unnamed System')
    domain = system_data.get('domain', 'unspecified')
    scale = system_data.get('scale', 'unspecified')
    description = system_data.get('description', '')
    
    # Parse principles
    principles = []
    for p_data in data.get('principles', []):
        if 'name' not in p_data:
            continue
        
        principle = Principle(
            name=p_data['name'],
            parameters=p_data.get('parameters', {}),
            confidence=p_data.get('confidence', 1.0)
        )
        principles.append(principle)
    
    # Create model
    model = SystemModel(
        name=name,
        domain=domain,
        scale=scale,
        description=description,
        principles=principles,
        components=data.get('components', []),
        relations=data.get('relations', []),
        tests=data.get('tests', {})
    )
    
    return model

def save_syslang(model: SystemModel, filepath: str) -> None:
    """
    Save a SystemModel to a YAML file
    
    Args:
        model: SystemModel to save
        filepath: Path where to save the file
    """
    data = {
        'system': {
            'name': model.name,
            'domain': model.domain,
            'scale': model.scale,
            'description': model.description
        }
    }
    
    if model.principles:
        data['principles'] = []
        for principle in model.principles:
            p_data = {
                'name': principle.name,
                'parameters': principle.parameters
            }
            if principle.confidence != 1.0:
                p_data['confidence'] = principle.confidence
            data['principles'].append(p_data)
    
    if model.components:
        data['components'] = model.components
    
    if model.relations:
        data['relations'] = model.relations
    
    if model.tests:
        data['tests'] = model.tests
    
    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)