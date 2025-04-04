import argparse
import os
import sys
import fileinput
import shutil

from techies.agent import Agent
from techies.task import Task
from techies.crew import Crew
from techies.game_specs import game_specs, specs
from techies.fixture_loader import runtime_config
from importlib.metadata import version

def get_system_crew(crewname, manage_agentops=False, introduce_only=False):
    if manage_agentops:
        import agentops
        agentops.init()

    agent_pool = Agent.eager_load_all()
    task_pool = Task.eager_load_all(agent_pool)
    if isinstance(crewname, str):
        crew = Crew(crewname, agent_pool=agent_pool, task_pool=task_pool, introduce_only=introduce_only)
        return crew
    elif isinstance(crewname, list):
        crews = [Crew(crew, agent_pool=agent_pool, task_pool=task_pool, introduce_only=introduce_only) for crew in crewname]
        return crews
    else:
        raise ValueError("crewname must be a string or a list of strings")

class CLI:
    def __init__(self):
        self.prog_name = os.path.basename(sys.argv[0])

    def execute(self, argv):
        description = f"""{self.prog_name} - Command line interface

Usage:
    {self.prog_name} list_crews
    {self.prog_name} list_agents
    {self.prog_name} list_tasks
    {self.prog_name} list_game_specs
    {self.prog_name} get_runtime_path
    {self.prog_name} introduce <crew>
    {self.prog_name} run <crew> [--game <game> | <gamefiles>]
    {self.prog_name} help <crew>
        """

        parser = argparse.ArgumentParser(prog=self.prog_name, description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('command', type=str, help='Command to run')
        parser.add_argument('crew', type=str, help='Crew to use', nargs='?', default="hierarchy_crew")

        if not argv or (argv[0] == "help" and len(argv) == 1):
            parser.print_help()
            sys.exit(1)

        options, args = parser.parse_known_args(argv)

        if options.command == "list_crews":
            print("[Available crews]")
            for crew, path in Crew.list_crews().items():
                print(f"{crew:20s} at {path}")
        elif options.command == "list_agents":
            print(Agent.list_agents())
        elif options.command == "list_tasks":
            print(Task.list_tasks())
        elif options.command == "list_game_specs":
            print("[Available game specifications]")
            print("\t".join(specs.keys()))
        elif options.command == "get_runtime_path":
            print(runtime_config())
        elif options.command == "introduce":
            self.introduce_crew(options.crew)
        elif options.command == "run":
            args = [options.crew] + args
            if options.crew in ["hierarchy_crew", "hierarchy_crew_v2"]:
                self.kickoff_hierarchy_crew(args)
            elif options.crew in ["html5_crew"]:
                self.kickoff_html5_crew(args)
            else:
                self.kickoff_default_crew(args)
        elif options.command == "help":
            args = [options.crew, "--help"] + args
            if options.crew in ["hierarchy_crew", "hierarchy_crew_v2"]:
                self.kickoff_hierarchy_crew(args)
            elif options.crew in ["html5_crew"]:
                self.kickoff_html5_crew(args)
            else:
                self.kickoff_default_crew(args)
        else:
            print("Command not found")

    def introduce_crew(self, crewname):
        crew = get_system_crew(crewname, introduce_only=True)
        crew.kickoff()

    def kickoff_default_crew(self, extra_args):
        parser = argparse.ArgumentParser(prog=f"{self.prog_name} run", description=f"{extra_args[0]} - Generic crew interface")
        parser.add_argument('crew', type=str, help=f'Crew to use, with {extra_args[0]}')
        options = parser.parse_args(extra_args)

        get_system_crew(options.crew, manage_agentops=True).kickoff()

    def kickoff_hierarchy_crew(self, extra_args):
        parser = argparse.ArgumentParser(prog=f"{self.prog_name} run", description=f"{extra_args[0]} - Description-included crew interface")
        parser.add_argument('crew', type=str, help='Crew to use, with {extra_args[0]}')
        parser.add_argument('--game', type=str, help='Predefined game specification')
        parser.add_argument('gamefiles', type=str, help='Game specification file', nargs='?')
        options = parser.parse_args(extra_args)

        if options.game:
            game_specifications = game_specs(options.game)
        elif options.gamefiles:
            with fileinput.input(files=options.gamefiles) as f:
                game_specifications = "\n".join(f)
        else:
            print("No game specification provided")
            sys.exit(1)

        inputs = { "game_specifications": game_specifications }
        get_system_crew(options.crew, manage_agentops=True).kickoff(inputs)

    def kickoff_html5_crew(self, extra_args):
        if "--help" in extra_args:
            self.kickoff_hierarchy_crew(extra_args)
            return

        if not os.path.exists("game.html"):
            scaffold_file_path = os.path.normpath(__file__ + "/../refs/build/game.html")
            shutil.copy(scaffold_file_path, "game.html")

        self.kickoff_hierarchy_crew(extra_args)

def main():
    cli = CLI()
    cli.execute(sys.argv[1:])
