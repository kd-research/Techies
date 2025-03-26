import click
from techies.crew import Crew
from techies.agent import Agent
from techies.task import Task
from techies.game_specs import specs

@click.command(name="list_crews")
def list_crews():
    """List available crews."""
    click.echo("[Available crews]")
    for crew, path in Crew.list_crews().items():
        click.echo(f"{crew:20s} at {path}")

@click.command(name="list_agents")
def list_agents():
    """List available agents."""
    click.echo(Agent.list_agents())

@click.command(name="list_tasks")
def list_tasks():
    """List available tasks."""
    click.echo(Task.list_tasks())

@click.command(name="list_game_specs")
def list_game_specs():
    """List available game specifications."""
    click.echo("[Available game specifications]")
    click.echo("\t".join(specs.keys()))

