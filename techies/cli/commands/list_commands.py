import click
from techies.cli.utils.deprecator import deprecated_command
from techies.cli.commands.list import _list_crews, _list_agents, _list_tasks, _list_game_specs

@click.command(name="list_crews")
@deprecated_command("list crews")
def list_crews():
    """List available crews."""
    return _list_crews()

@click.command(name="list_agents")
@deprecated_command("list agents")
def list_agents():
    """List available agents."""
    return _list_agents()

@click.command(name="list_tasks")
@deprecated_command("list tasks")
def list_tasks():
    """List available tasks."""
    return _list_tasks()

@click.command(name="list_game_specs")
@deprecated_command("list game_specs")
def list_game_specs():
    """List available game specifications."""
    return _list_game_specs()

