import click
from techies.crew import Crew
from techies.task import Task
from techies.agent import Agent
from techies.tools import validate_tool
from techies.callbacks import validate_callback

@click.group()
def check():
    """Check validity of crews, tasks, or agents."""
    pass

@check.command()
@click.argument('name')
@click.option('--recursive/--no-recursive', '-R/-r', default=True, help='Enable or disable recursive validation (default: enabled).')
def crew(name, recursive):
    """Check a crew by name."""
    ok, reason = Crew.validate(name, recursive=recursive)
    if ok:
        click.echo(f"Checked crew '{name}' (recursive={recursive}): OK")
    else:
        click.echo(f"Checked crew '{name}' (recursive={recursive}): FAILED - {reason}")

@check.command()
@click.argument('name')
@click.option('--recursive/--no-recursive', '-R/-r', default=True, help='Enable or disable recursive validation (default: enabled).')
def task(name, recursive):
    """Check a task by name."""
    ok, reason = Task.validate(name, recursive=recursive)
    if ok:
        click.echo(f"Checked task '{name}' (recursive={recursive}): OK")
    else:
        click.echo(f"Checked task '{name}' (recursive={recursive}): FAILED - {reason}")

@check.command()
@click.argument('name')
@click.option('--recursive/--no-recursive', '-R/-r', default=True, help='Enable or disable recursive validation (default: enabled).')
def agent(name, recursive):
    """Check an agent by name."""
    ok, reason = Agent.validate(name, recursive=recursive)
    if ok:
        click.echo(f"Checked agent '{name}' (recursive={recursive}): OK")
    else:
        click.echo(f"Checked agent '{name}' (recursive={recursive}): FAILED - {reason}")

@check.command()
@click.argument('name')
@click.option('--recursive/--no-recursive', '-R/-r', default=True, help='Enable or disable recursive validation (default: enabled).')
def tool(name, recursive):
    """Check a tool by id."""
    ok, reason = validate_tool(name, recursive=recursive)
    if ok:
        click.echo(f"Checked tool '{name}' (recursive={recursive}): OK")
    else:
        click.echo(f"Checked tool '{name}' (recursive={recursive}): FAILED - {reason}")

@check.command()
@click.argument('name')
@click.option('--recursive/--no-recursive', '-R/-r', default=True, help='Enable or disable recursive validation (default: enabled).')
def callback(name, recursive):
    """Check a callback by id."""
    ok, reason = validate_callback(name, recursive=recursive)
    if ok:
        click.echo(f"Checked callback '{name}' (recursive={recursive}): OK")
    else:
        click.echo(f"Checked callback '{name}' (recursive={recursive}): FAILED - {reason}") 