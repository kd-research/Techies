import click
from techies.cli.utils.deprecator import deprecated_command
from techies.cli.commands.list import _list_callbacks

@click.command(name="list_callbacks")
@click.pass_context
@deprecated_command("list callbacks")
def list_callbacks(ctx):
    """List all available callbacks."""
    return _list_callbacks(ctx) 