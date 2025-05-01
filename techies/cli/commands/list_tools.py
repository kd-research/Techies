import click
from techies.cli.utils.deprecator import deprecated_command
from techies.cli.commands.list import _list_tools

@click.command(name="list_tools")
@deprecated_command("list tools")
def list_tools():
    """List all available tools, including custom tools."""
    return _list_tools() 