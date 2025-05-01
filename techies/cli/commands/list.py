import click
from techies.crew import Crew
from techies.agent import Agent
from techies.task import Task
from techies.game_specs import specs
from techies.tools import get_all_tools
from techies.callbacks import get_all_callbacks

@click.group(name="list")
def list_group():
    """List available resources."""
    pass

# Implementation functions

def _list_crews():
    """List available crews (implementation)."""
    click.echo("[Available crews]")
    for crew, path in Crew.list_crews().items():
        click.echo(f"{crew:20s} at {path}")

def _list_agents():
    """List available agents (implementation)."""
    click.echo("[Available agents]")
    for agent, path in Agent.list_agents().items():
        click.echo(f"{agent:20s} at {path}")

def _list_tasks():
    """List available tasks (implementation)."""
    click.echo("[Available tasks]")
    for task, path in Task.list_tasks().items():
        click.echo(f"{task:20s} at {path}")

def _list_game_specs():
    """List available game specifications (implementation)."""
    click.echo("[Available game specifications]")
    click.echo("\t".join(specs.keys()))

def _list_tools():
    """List all available tools (implementation)."""
    tools_dict = get_all_tools()
    
    if not tools_dict:
        click.echo("No tools available.")
        return
    
    click.echo(f"Found {len(tools_dict)} tools:")
    click.echo("-" * 80)
    
    for tool_id, tool in tools_dict.items():
        click.echo(f"Tool ID: {tool_id}")
        click.echo(f"Name: {tool.name}")
        click.echo(f"Description: {tool.description}")
        
        if hasattr(tool, 'args_schema') and tool.args_schema:
            click.echo("Arguments:")
            for field_name, field in tool.args_schema.__fields__.items():
                field_desc = field.description or "No description"
                click.echo(f"  - {field_name}: {field_desc}")
        
        click.echo("-" * 80)

def _list_callbacks(ctx):
    """List all available callbacks (implementation)."""
    # Check if --allow-load-scripts was used
    if not ctx.obj.get('allow_load_scripts', False):
        click.echo("Warning: No callbacks are loaded. Use --allow-load-scripts flag to load custom callbacks.")
        return
    
    callbacks_dict = get_all_callbacks()
    
    if not callbacks_dict:
        click.echo("No callbacks available.")
        return
    
    click.echo(f"Found {len(callbacks_dict)} callbacks:")
    click.echo("-" * 80)
    
    for callback_id, callback in callbacks_dict.items():
        click.echo(f"Callback ID: {callback_id}")
        click.echo(f"Function: {callback.__name__}")
        
        # Show docstring if available
        if callback.__doc__:
            doc = callback.__doc__.strip()
            click.echo(f"Description: {doc}")
        else:
            click.echo("No description defined.")
        
        click.echo("-" * 80)

# Command decorators for the list group

@list_group.command(name="crews")
def crews():
    """List available crews."""
    return _list_crews()

@list_group.command(name="agents")
def agents():
    """List available agents."""
    return _list_agents()

@list_group.command(name="tasks")
def tasks():
    """List available tasks."""
    return _list_tasks()

@list_group.command(name="game_specs")
def game_specs():
    """List available game specifications."""
    return _list_game_specs()

@list_group.command(name="tools")
def tools():
    """List all available tools, including custom tools."""
    return _list_tools()

@list_group.command(name="callbacks")
@click.pass_context
def callbacks(ctx):
    """List all available callbacks."""
    return _list_callbacks(ctx)