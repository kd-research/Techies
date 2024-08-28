import argparse
import os
import sys
import fileinput

from techies.agent import Agent
from techies.task import Task
from techies.crew import Crew
from techies.game_specs import game_specs, specs
from techies.fixture_loader import runtime_config

def get_groq_crew(crewname, **kwargs):
    from langchain_groq import ChatGroq

    agent_pool = Agent.eager_load_all(llm=ChatGroq(model="llama3-8b-8192"))
    task_pool = Task.eager_load_all(agent_pool)
    crew = Crew(
        crewname,
        agent_pool=agent_pool,
        task_pool=task_pool,
        embedder={
            "provider": "huggingface",
            "config": {
                "model": "sentence-transformers/all-mpnet-base-v2"
            }
        },
        max_rpm=2
    )

    return crew

def get_openai_crew(crewname, manage_agentops=False):
    if manage_agentops:
        import agentops
        agentops.init()

    from langchain_openai import ChatOpenAI

    agent_pool = Agent.eager_load_all(llm=ChatOpenAI(model="gpt-4o-2024-08-06", temperature=0.2))
    task_pool = Task.eager_load_all(agent_pool)
    if isinstance(crewname, str):
        crew = Crew(crewname, agent_pool=agent_pool, task_pool=task_pool)
        return crew
    elif isinstance(crewname, list):
        crews = [Crew(crew, agent_pool=agent_pool, task_pool=task_pool) for crew in crewname]
        return crews
    else:
        raise ValueError("crewname must be a string or a list of strings")


def get_anthropic_crew(crewname, **kwargs):
    try:
        import agentops
        print("Anthropic crew is not fully supported and is not compatible with agentops. An isolated environment without agentopt install is required.")
        exit(1)
    except ImportError:
        pass

    from langchain_anthropic import ChatAnthropic

    agent_pool = Agent.eager_load_all(llm=ChatAnthropic(model="claude-3-5-sonnet-20240620"))
    task_pool = Task.eager_load_all(agent_pool)
    crew = Crew(crewname, agent_pool=agent_pool, task_pool=task_pool)

    return crew


class CLI:
    def __init__(self):
        self.prog_name = os.path.basename(sys.argv[0])

    def assign_ai_crew(self, ai):
        if ai == "groq":
            self.get_crew = get_groq_crew
        elif ai == "openai":
            self.get_crew = get_openai_crew
        elif ai == "anthropic":
            self.get_crew = get_anthropic_crew

    def execute(self, argv):
        description = f"""{self.prog_name} - Command line interface

Usage:
    {self.prog_name} list_crews
    {self.prog_name} list_agents
    {self.prog_name} list_tasks
    {self.prog_name} list_game_specs
    {self.prog_name} get_runtime_path
    {self.prog_name} run <crew> [--game <game> | <gamefiles>]
    {self.prog_name} help <crew>
        """

        parser = argparse.ArgumentParser(prog=self.prog_name, description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('command', type=str, help='Command to run')
        parser.add_argument('crew', type=str, help='Crew to use', nargs='?', default="hierarchy_crew")
        parser.add_argument('--ai', type=str, help='AI to use', default="openai", choices=["groq", "openai", "anthropic"])
        if not argv:
            parser.print_help()
            sys.exit(1)

        options, args = parser.parse_known_args(argv)

        self.assign_ai_crew(options.ai)

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
        elif options.command == "run":
            args = [options.crew] + args
            if options.crew in ["hierarchy_crew", "hierarchy_crew_v2", "html5_crew"]:
                self.kickoff_hierarchy_crew(args)
            else:
                self.kickoff_default_crew(args)
        elif options.command == "help":
            args = [options.crew, "--help"] + args
            if options.crew in ["hierarchy_crew", "hierarchy_crew_v2", "html5_crew"]:
                self.kickoff_hierarchy_crew(args)
            else:
                self.kickoff_default_crew(args)

        else:
            print("Command not found")

    def kickoff_default_crew(self, extra_args):
        parser = argparse.ArgumentParser(prog=f"{self.prog_name} run", description=f"{extra_args[0]} - Generic crew interface")
        parser.add_argument('crew', type=str, help=f'Crew to use, with {extra_args[0]}')
        options = parser.parse_args(extra_args)

        crew = self.get_crew(options.crew, manage_agentops=True).kickoff()

    def kickoff_hierarchy_crew(self, extra_args):
        parser = argparse.ArgumentParser(prog=f"{self.prog_name} run", description=f"{extra_args[0]} - Description-included crew interface")
        parser.add_argument('crew', type=str, help='Crew to use, with {extra_args[0]}')
        parser.add_argument('--game', type=str, help='Predefined game specification')
        parser.add_argument('gamefiles', type=str, help='Game specification file', nargs='?')
        options = parser.parse_args(extra_args)

        if options.game:
            game_specifications= game_specs(options.game)
        elif options.gamefiles:
            with fileinput.input(files=options.gamefiles) as f:
                game_specifications = "\n".join(f)
        else:
            print("No game specification provided")
            sys.exit(1)

        inputs = { "game_specifications": game_specifications }
        crew = self.get_crew(options.crew, manage_agentops=True).kickoff(inputs)


def main():
    cli = CLI()
    cli.execute(sys.argv[1:])
