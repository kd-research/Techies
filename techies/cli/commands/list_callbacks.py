import click
from techies.callbacks import get_all_callbacks

@click.command()
@click.pass_context
def list_callbacks(ctx):
    """List all available callbacks."""
    # Check if --allow-load-scripts was used
    if not ctx.obj.get('allow_load_scripts', False):
        click.echo("Warning: No callbacks are loaded. Use --allow-load-scripts flag to load custom callbacks.")
        return
    
    callbacks = get_all_callbacks()
    
    if not callbacks:
        click.echo("No callbacks available.")
        return
    
    click.echo(f"Found {len(callbacks)} callbacks:")
    click.echo("-" * 80)
    
    for callback_id, callback in callbacks.items():
        click.echo(f"Callback ID: {callback_id}")
        click.echo(f"Function: {callback.__name__}")
        
        # Show docstring if available
        if callback.__doc__:
            doc = callback.__doc__.strip()
            click.echo(f"Description: {doc}")
        else:
            click.echo("No description defined.")
        
        click.echo("-" * 80) 