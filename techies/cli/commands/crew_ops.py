import os
import click

from pathlib import Path
from shutil import copytree
from techies.crew import Crew

_fixture_dir = os.path.normpath(__file__ + '/../../../fixtures')

@click.command(name="scaffold")
@click.argument("crewname")
def new_crew(crewname):
    """Create a new crew."""
    template_dir = Path(_fixture_dir) / ".template"
    copytree(template_dir, crewname)
    

@click.command(name="dump")
@click.argument("crew_name")
def dump_crew(crew_name):
    """Dump a crew's code."""
    crew_locations = Crew.list_crews()
    if crew_name not in crew_locations:
        click.echo(f"Crew {crew_name} not found.")
        return

    # dump crew's parent directory to cwd
    crew_path = Path(crew_locations[crew_name]).parent
    copytree(crew_path, crew_name)
    click.echo(f"Crew {crew_name} dumped to {crew_name}/")
