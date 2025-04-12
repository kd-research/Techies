import click
from techies.cli.commands import register_commands
from techies.cli.utils.load_tools import load_custom_tools
from techies.cli.utils.load_callbacks import load_custom_callbacks

@click.group()
@click.option('--allow-load-scripts', is_flag=True, help='Load custom scripts (tools and callbacks) from runtime directories')
@click.pass_context
def cli(ctx, allow_load_scripts):
    """Techies CLI."""
    # Initialize context object if it doesn't exist
    ctx.ensure_object(dict)
    
    # Store the flag in the context
    ctx.obj['allow_load_scripts'] = allow_load_scripts
    
    if allow_load_scripts:
        num_tools = load_custom_tools()
        num_callbacks = load_custom_callbacks()
        click.echo(f"Loaded {num_tools} custom tool files and {num_callbacks} custom callback files")

register_commands(cli)

def main():
    cli(obj={})
