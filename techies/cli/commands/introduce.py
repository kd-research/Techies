import click
from techies.cli.utils.crew_helpers import get_system_crew

@click.command()
@click.argument("crew")
def introduce(crew):
    """Introduce a crew."""
    crew_instance = get_system_crew(crew, introduce_only=True)
    crew_instance.kickoff()
