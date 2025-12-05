"""Command-line interface for SysLang - Loads principles from JSON files"""
import click
import yaml
import json
from pathlib import Path
import sys
from datetime import datetime

# Load external data files
def load_principles_library():
    """Load principles from JSON file"""
    principles_path = Path(__file__).parent / "data" / "principles.json"
    with open(principles_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_distribution_patterns():
    """Load distribution patterns from JSON file"""
    patterns_path = Path(__file__).parent / "data" / "patterns.json"
    with open(patterns_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_compatibility_rules():
    """Load compatibility rules from JSON file"""
    compat_path = Path(__file__).parent / "data" / "compatibility.json"
    with open(compat_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Global data (loaded once)
PRINCIPLES_LIB = load_principles_library()
PATTERNS_LIB = load_distribution_patterns()
COMPATIBILITY_RULES = load_compatibility_rules()

@click.group()
@click.version_option()
def main():
    """SysLang - DSL for Transdisciplinary Systemic Analysis"""
    pass

@main.command()
@click.argument("filepath", type=click.Path(exists=True))
def check(filepath):
    """Validate a SysLang model file"""
    # Implementation using PRINCIPLES_LIB
    pass

@main.command()
@click.argument("filepath", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Choice(["text", "json", "html"]), default="text")
def analyze(filepath, output):
    """Analyze a system using principles from JSON"""
    # Implementation using PRINCIPLES_LIB and PATTERNS_LIB
    pass

@main.command()
@click.argument("principle", required=False)
def principles(principle):
    """List principles from JSON library"""
    if principle:
        if principle in PRINCIPLES_LIB["principles"]:
            info = PRINCIPLES_LIB["principles"][principle]
            click.echo(click.style(f"\n{principle}", fg="green", bold=True))
            click.echo(f"Description: {info['description']}")
            click.echo(f"Category: {info['category']}")
            
            # Show parameters from JSON
            if 'parameters' in info:
                click.echo("\nParameters:")
                for param_name, param_info in info['parameters'].items():
                    click.echo(f"  • {param_name}: {param_info['description']}")
                    if 'values' in param_info:
                        click.echo(f"    Values: {', '.join(param_info['values'])}")
        else:
            click.echo(click.style(f"❌ Principle '{principle}' not found", fg="red"))
    else:
        click.echo(click.style("Available Principles:", fg="cyan", bold=True))
        for category, desc in PRINCIPLES_LIB["categories"].items():
            click.echo(f"\n{category}: {desc}")
            principles_in_category = [
                name for name, info in PRINCIPLES_LIB["principles"].items()
                if info["category"] == category
            ]
            for name in sorted(principles_in_category):
                info = PRINCIPLES_LIB["principles"][name]
                icon = "🔄 " if info.get('meta_principle') else "⚙️ " if info.get('operator') else "• "
                click.echo(f"  {icon}{name}")

@main.command()
@click.argument("pattern", required=False)
def patterns(pattern):
    """Show distribution patterns from JSON"""
    patterns_data = PATTERNS_LIB["distribution_patterns"]
    
    if pattern:
        if pattern in patterns_data:
            info = patterns_data[pattern]
            click.echo(click.style(f"\n📊 Distribution Pattern: {pattern}", fg="cyan", bold=True))
            click.echo(f"Description: {info['description']}")
            click.echo(f"Parent principle: {info['parent_principle']}")
            
            click.echo(f"\nSpecific Parameters:")
            for param_name, param_info in info['specific_parameters'].items():
                click.echo(f"  • {param_name}: {param_info['description']}")
        else:
            click.echo(click.style(f"❌ Pattern '{pattern}' not found", fg="red"))
    else:
        click.echo(click.style("Distribution Patterns:", fg="cyan", bold=True))
        for name, info in patterns_data.items():
            click.echo(f"\n• {name}: {info['description']}")

@main.command()
@click.option("--name", prompt="System name")
@click.option("--domain", prompt="Domain")
@click.option("--output", "-o", default="system.syslang.yml")
def new(name, domain, output):
    """Create new model with principles from JSON"""
    # Template generation using PRINCIPLES_LIB
    pass

# Helper functions that use JSON data
def generate_hypothesis(principle_name, parameters):
    """Generate hypothesis based on principle template in JSON"""
    if principle_name in PRINCIPLES_LIB["principles"]:
        principle = PRINCIPLES_LIB["principles"][principle_name]
        
        if 'hypothesis_template' in principle:
            template = principle['hypothesis_template']
            # Fill template with parameter values
            for param, value in parameters.items():
                template = template.replace(f"{{{param}}}", str(value))
            
            # Add default threshold if needed
            if '{threshold}' in template and 'default_threshold' in principle:
                template = template.replace('{threshold}', str(principle['default_threshold']))
            
            return template
    
    return f"System should exhibit {principle_name} characteristics"

# ... rest of helper functions using JSON data

if __name__ == "__main__":
    main()