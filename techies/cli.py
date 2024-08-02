import argparse
import os
import sys

from techies.agent import Agent
from techies.task import Task
from techies.crew import Crew
from techies.game_specs import game_specs, specs
from techies.fixture_loader import runtime_config

def get_groq_crew(crewname):
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

def get_openai_crew(crewname):
    import agentops
    from langchain_openai import ChatOpenAI

    agentops.init()

    agent_pool = Agent.eager_load_all(llm=ChatOpenAI(model="gpt-4o", temperature=0.2))
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

    def execute(self, argv):
        parser = argparse.ArgumentParser(prog=self.prog_name, description=f"{self.prog_name} - Command line interface")
        parser.add_argument('command', type=str, help='Command to run')
        parser.add_argument('crew', type=str, help='Crew to use', nargs='?', default="hierarchy_crew")
        parser.add_argument('--ai', type=str, help='AI to use', default="openai", choices=["groq", "openai"])
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
            if options.crew == "hierarchy_crew":
                self.kickoff_hierarchy_crew(args)
            else:
                self.kickoff_default_crew(args)
        else:
            print("Command not found")

    def kickoff_default_crew(self, extra_args):
        parser = argparse.ArgumentParser(prog=self.prog_name, description=f"{self.prog_name} run - Command line interface")
        parser.add_argument('crew', type=str, help='Crew to use')
        options = parser.parse_args(extra_args)

        crew = self.get_crew(options.crew).kickoff()

    def kickoff_hierarchy_crew(self, extra_args):
        parser = argparse.ArgumentParser(prog=self.prog_name, description=f"{self.prog_name} run - Command line interface")
        parser.add_argument('crew', type=str, help='Crew to use')
        parser.add_argument('--game', type=str, help='Game to make', choices=specs.keys())
        options = parser.parse_args(extra_args)

        inputs = { "game_specifications": game_specs(options.game) }
        crew = self.get_crew(options.crew).kickoff(inputs=inputs)


def main():
    cli = CLI()
    cli.execute(sys.argv[1:])
