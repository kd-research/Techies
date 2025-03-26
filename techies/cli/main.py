import click
from techies.cli.commands import register_commands

@click.group()
def cli():
    """Techies CLI."""
    pass

register_commands(cli)

def main():
    cli()
