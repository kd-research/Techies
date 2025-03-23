import click
from techies.fixture_loader import runtime_config

@click.command()
def get_runtime_path():
    """Print the runtime configuration path."""
    click.echo(runtime_config())
