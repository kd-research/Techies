import click
from techies.cli.utils.dispatch import (
    kickoff_hierarchy_crew,
    kickoff_html5_crew,
    kickoff_mechanicsgen_crew,
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

@run.command("hierarchy_crew")
@click.option("--game", help="Predefined game specification")
@click.argument("gamefiles", required=False)
def run_hierarchy_crew(*args, **kwargs):
    click.echo("Running hierarchy crew")
    args = ["hierarchy_crew"] + list(args)
    kickoff_hierarchy_crew(*args, **kwargs)

@run.command("hierarchy_crew_v2")
@click.option("--game", help="Predefined game specification")
@click.argument("gamefiles", required=False)
def run_hierarchy_crew_v2(*args, **kwargs):
    click.echo("Running hierarchy crew v2")
    args = ["hierarchy_crew_v2"] + list(args)
    kickoff_hierarchy_crew(*args, **kwargs)

@run.command("html5_crew")
@click.option("--game", help="Predefined game specification")
@click.argument("gamefiles", required=False)
def run_html5(*args, **kwargs):
    click.echo("Running HTML5 crew")
    args = ["html5_crew"] + list(args)
    kickoff_html5_crew(*args, **kwargs)