"""Command-line interface for SysLang"""
import click
import yaml
import json
from pathlib import Path
import sys

@click.group()
@click.version_option()
def main():
    """SysLang - DSL for Transdisciplinary Systemic Analysis"""
    pass

@main.command()
@click.argument("filepath", type=click.Path(exists=True))
def check(filepath):
    """Validate a SysLang model file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        # Basic validation
        if 'system' not in data:
            raise ValueError("Missing 'system' section")
        
        system_name = data['system'].get('name', 'Unnamed')
        principles = data.get('principles', [])
        
        click.echo(click.style("✅ Valid SysLang file", fg="green"))
        click.echo(f"System: {system_name}")
        click.echo(f"Domain: {data['system'].get('domain', 'unspecified')}")
        click.echo(f"Scale: {data['system'].get('scale', 'unspecified')}")
        
        if principles:
            click.echo(f"\nPrinciples ({len(principles)}):")
            for p in principles:
                name = p.get('name', 'unnamed')
                confidence = p.get('confidence', 'not specified')
                click.echo(f"  • {name} (confidence: {confidence})")
        
        tests = data.get('tests', {})
        if tests.get('refutable'):
            click.echo(f"\n🔬 Refutable test: {tests['refutable']}")
        
    except Exception as e:
        click.echo(click.style(f"❌ Error: {str(e)}", fg="red"))
        sys.exit(1)

@main.command()
@click.argument("filepath", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Choice(["text", "json"]), default="text")
def analyze(filepath, output):
    """Analyze a system and generate insights"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        system_name = data['system'].get('name', 'Unnamed')
        principles = data.get('principles', [])
        
        # Generate hypotheses
        hypotheses = []
        for p in principles:
            p_name = p.get('name')
            if p_name == "Modularity":
                hypotheses.append({
                    "description": "System should have modularity index Q > 0.3",
                    "test": "Calculate modularity on interaction graph",
                    "metric": "modularity_index",
                    "threshold": 0.3
                })
            elif p_name == "Bus":
                hypotheses.append({
                    "description": "Connections should scale as O(N), not O(N²)",
                    "test": "Count connections vs components²",
                    "metric": "connection_ratio",
                    "threshold": 0.5
                })
            elif p_name == "Hierarchy":
                hypotheses.append({
                    "description": "System should have clear hierarchical levels",
                    "test": "Analyze control/communication flow",
                    "metric": "hierarchy_depth",
                    "threshold": "2-4 levels"
                })
            elif p_name == "Polarity":
                hypotheses.append({
                    "description": "System should show measurable polarity",
                    "test": "Measure distribution of properties",
                    "metric": "polarity_index",
                    "threshold": "bimodal distribution"
                })
        
        # Generate checklist
        checklist = [
            "Define measurable metrics for each principle",
            "Establish baseline measurements",
            "Test under stress conditions",
            "Validate refutability conditions",
            "Document edge cases and limitations"
        ]
        
        if output == "json":
            result = {
                "system": system_name,
                "hypotheses": hypotheses,
                "checklist": checklist,
                "principles": [p.get('name') for p in principles]
            }
            click.echo(json.dumps(result, indent=2))
        else:
            click.echo(click.style(f"\n🔍 ANALYSIS REPORT: {system_name}", fg="cyan", bold=True))
            
            if hypotheses:
                click.echo(click.style("\n🧪 TESTABLE HYPOTHESES:", fg="yellow"))
                for i, hyp in enumerate(hypotheses, 1):
                    click.echo(f"\n{i}. {hyp['description']}")
                    click.echo(f"   Test: {hyp['test']}")
                    click.echo(f"   Metric: {hyp['metric']} > {hyp['threshold']}")
            
            click.echo(click.style("\n📋 VERIFICATION CHECKLIST:", fg="green"))
            for i, item in enumerate(checklist, 1):
                click.echo(f"{i}. [ ] {item}")
            
            click.echo(click.style("\n🎯 NEXT STEPS:", fg="magenta"))
            click.echo("1. Implement measurement protocols")
            click.echo("2. Collect empirical data")
            click.echo("3. Compare with predictions")
            click.echo("4. Refine model based on results")
        
    except Exception as e:
        click.echo(click.style(f"❌ Error: {str(e)}", fg="red"))
        sys.exit(1)

@main.command()
def principles():
    """List available principles with descriptions"""
    principles_info = {
        "Modularity": {
            "description": "Organization into semi-independent units",
            "category": "Structure",
            "parameters": ["coupling", "cohesion"]
        },
        "Hierarchy": {
            "description": "Nested levels of organization",
            "category": "Structure", 
            "parameters": ["levels", "span", "control"]
        },
        "Bus": {
            "description": "Shared communication channel with arbitration",
            "category": "Structure",
            "parameters": ["arbitration", "protocol", "bandwidth"]
        },
        "Polarity": {
            "description": "Opposed/complementary poles in system",
            "category": "Operator",
            "parameters": ["poles", "type", "strength"]
        },
        "Resilience": {
            "description": "Ability to recover from perturbations",
            "category": "Dynamics",
            "parameters": ["recovery_time", "robustness"]
        },
        "Adaptation": {
            "description": "Adjustment to changing conditions",
            "category": "Dynamics",
            "parameters": ["timescale", "mechanism"]
        },
        "Communication": {
            "description": "Information exchange between components",
            "category": "Information",
            "parameters": ["direction", "protocol", "bandwidth"]
        },
        "Trajectory": {
            "description": "Form and direction of system evolution",
            "category": "Dynamics",
            "parameters": ["shape", "directionality", "stability"]
        }
    }
    
    click.echo(click.style("📚 AVAILABLE PRINCIPLES", fg="cyan", bold=True))
    click.echo("=" * 50)
    
    for name, info in principles_info.items():
        click.echo(click.style(f"\n• {name}", fg="green"))
        click.echo(f"  {info['description']}")
        click.echo(f"  Category: {info['category']}")
        if info['parameters']:
            click.echo(f"  Parameters: {', '.join(info['parameters'])}")

@main.command()
@click.option("--name", prompt="System name")
@click.option("--domain", prompt="Domain (informatics/biology/sociology/engineering)")
@click.option("--output", "-o", default="my_system.syslang.yml")
def new(name, domain, output):
    """Create a new SysLang model interactively"""
    template = f"""system:
  name: "{name}"
  domain: "{domain}"
  scale: "meso"
  description: "Describe your system here"

principles:
  - name: "Modularity"
    parameters:
      coupling: "low"
      cohesion: "high"
    confidence: 0.8

tests:
  refutable: "Describe a test that could refute this design"
  metrics: ["metric1", "metric2"]
  limits: "Conditions where this model doesn't apply"

# Uncomment and customize additional principles:
# - name: "Hierarchy"
#   parameters:
#     levels: 3
#     span: "narrow"
#
# - name: "Bus"
#   parameters:
#     arbitration: "temporal"
#     protocol: "standard"
#
# - name: "Polarity"
#   parameters:
#     poles: ["input", "output"]
#     type: "complementary"
"""
    
    Path(output).write_text(template, encoding='utf-8')
    click.echo(click.style(f"✅ Template created at {output}", fg="green"))
    click.echo(f"Edit it and then run:")
    click.echo(f"  syslang check {output}")
    click.echo(f"  syslang analyze {output}")

@main.command()
@click.argument("filepath", type=click.Path(exists=True))
@click.option("--format", "-f", type=click.Choice(["text", "json"]), default="text")
def validate(filepath):
    """Alias for 'check' command"""
    check.callback(filepath)

if __name__ == "__main__":
    main()