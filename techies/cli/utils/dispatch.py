import os
import sys
import fileinput
import shutil

from techies.cli.utils.crew_helpers import get_system_crew
from techies.game_specs import game_specs

def kickoff_default_crew(crewname):
    crew = get_system_crew(crewname, manage_agentops=True)
    crew.kickoff()

def kickoff_hierarchy_crew(crewname, game=None, gamefiles=None):
    if not game and not gamefiles:
        click.echo("Error: either --game or gamefiles must be provided.", err=True)
        sys.exit(1)

    if game:
        game_specifications = game_specs(game)
    else:
        with fileinput.input(files=gamefiles) as f:
            game_specifications = "\n".join(f)

    inputs = { "game_specifications": game_specifications }
    crew = get_system_crew(crewname, manage_agentops=True)
    crew.kickoff(inputs)

def kickoff_html5_crew(crewname, game=None, gamefiles=None):
    if not os.path.exists("game.html"):
        scaffold_file_path = os.path.normpath(__file__ + "/../../../refs/build/game.html")
        shutil.copy(scaffold_file_path, "game.html")

    kickoff_hierarchy_crew(crewname, game=game, gamefiles=gamefiles)
