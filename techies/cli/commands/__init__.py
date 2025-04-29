from .run import run
from .introduce import introduce
from .list_commands import list_crews, list_agents, list_tasks, list_game_specs
from .crew_ops import new_crew, dump_crew
from .get_runtime_path import get_runtime_path
from .list_tools import list_tools
from .list_callbacks import list_callbacks
from .check import check

def register_commands(cli):
    cli.add_command(run)
    cli.add_command(introduce)
    cli.add_command(list_crews)
    cli.add_command(list_agents)
    cli.add_command(list_tasks)
    cli.add_command(list_game_specs)
    cli.add_command(new_crew)
    cli.add_command(dump_crew)
    cli.add_command(get_runtime_path)
    cli.add_command(list_tools)
    cli.add_command(list_callbacks)
    cli.add_command(check)
