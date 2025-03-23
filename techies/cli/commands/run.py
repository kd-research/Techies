import click
from techies.cli.utils.dispatch import (
    kickoff_hierarchy_crew,
    kickoff_html5_crew,
    kickoff_default_crew
)
from techies.cli.utils.click_extensions import DefaultRunGroup

@click.group(cls=DefaultRunGroup, invoke_without_command=True)
@click.pass_context
def run(ctx):
    """Run a specific crew.

    Use one of the known subcommands (like 'hierarchy' or 'html5'), or pass a crew name directly.
    """
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())

@run.command("hierarchy")
@click.argument("crew")
@click.option("--game", help="Predefined game specification")
@click.argument("gamefiles", required=False)
def run_hierarchy(crew, game, gamefiles):
    """Run a hierarchy-based crew with game input."""
    kickoff_hierarchy_crew(crewname=crew, game=game, gamefiles=gamefiles)

@run.command("html5")
@click.argument("crew")
@click.option("--game", help="Predefined game specification")
@click.argument("gamefiles", required=False)
def run_html5(crew, game, gamefiles):
    """Run an HTML5 crew with game input and optional scaffold injection."""
    kickoff_html5_crew(crewname=crew, game=game, gamefiles=gamefiles)

# The fallback/default is handled by DefaultRunGroup, not defined as a subcommand
