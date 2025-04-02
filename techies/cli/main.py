import click
from techies.cli.commands import register_commands
from techies.cli.utils.load_tools import load_custom_tools

@click.group()
@click.option('--allow-load-tools', is_flag=True, help='Load custom tool files from runtime directories')
def cli(allow_load_tools):
    """Techies CLI."""
    if allow_load_tools:
        num_tools = load_custom_tools()
        click.echo(f"Loaded {num_tools} custom tool files")
    pass

register_commands(cli)

def main():
    cli()
