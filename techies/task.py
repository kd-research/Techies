from techies.fixture_loader import load_fixture
from techies.callbacks import get_all_callbacks, validate_callback
from techies.agent import Agent
from crewai import Task as _Task
from typing import List, Tuple, Dict, Tuple, Optional
import jsonschema
from techies.config_schema import TASK_SCHEMA
from functools import lru_cache
from techies.utils import topology_sort_partial


class Task(_Task):
    @staticmethod
    def eager_load_all(agent_pool):
        task_pool = {}
        all_callbacks = get_all_callbacks()
        for config_name in load_fixture('tasks').keys():
            if not config_name.startswith('_'):
                Task(config_name, agent_pool=agent_pool, task_pool=task_pool, callbacks_available=all_callbacks)
        return task_pool

    @staticmethod
    def list_tasks():
        return load_fixture('tasks', result="locations")

    @staticmethod
    def validate(name, recursive=True):
        """
        Validate the task with the given name.
        If recursive=True, also validates all dependencies.
        
        Returns (True, None) on success, (False, 'failure-reason') on failure.
        """
        # For non-recursive validation, just check the schema
        if not recursive:
            return Task._validate_schema(name)
        
        # For recursive validation, first validate this task as a dependent
        ok, reason = Task._validate_as_dependent(name)
        if not ok:
            return False, reason
        
        # Get all tasks in dependency tree
        try:
            vertices, edges = Task._load_tasks_as_depend_graph()
            dependent_tasks = topology_sort_partial(vertices, edges, name)
        except ValueError as e:
            return False, f"Dependency validation failed: {str(e)}"
        
        # Validate all dependencies (excluding the task itself which we've already validated)
        errors = []
        for dependent_task in dependent_tasks:
            if dependent_task != name:  # Skip the task itself
                ok, reason = Task._validate_as_dependent(dependent_task)
                if not ok:
                    errors.append(f"Dependent task '{dependent_task}': {reason}")
        
        if errors:
            return False, f"Task '{name}' has invalid dependencies:\n" + "\n".join(errors)
        
        return True, None

    @staticmethod
    def _load_tasks_as_depend_graph():
        """
        Load all tasks and build a dependency graph.
        
        Returns:
            Tuple[List[str], List[Tuple[str, str]]]: A tuple containing:
                - List of task names (vertices)
                - List of dependency edges as (dependent_task, dependency) tuples
        """
        task_configs = load_fixture('tasks')
        
        # Get all task names (excluding those starting with '_')
        vertices = [task_name for task_name in task_configs.keys() 
                   if not task_name.startswith('_')]
        
        # Build the dependency edges
        edges = []
        for task_name in vertices:
            config = task_configs[task_name]
            depends_on = config.get('depends_on', [])
            
            # Convert to list if it's a string
            if isinstance(depends_on, str):
                depends_on = [depends_on]
                
            # Add edges from dependencies to the current task
            # Note: In a dependency graph, edges point from dependent task to its dependency
            for dependency in depends_on:
                edges.append((task_name, dependency))  # This task depends on dependency
        
        return vertices, edges

    @staticmethod
    @lru_cache(maxsize=128)
    def _validate_schema(name):
        """
        Validate task configuration against the schema.
        
        Args:
            name: Name of the task to validate
            
        Returns:
            Tuple[bool, Optional[str]]: (success, error_message)
        """
        # Check if task exists
        task_configs = load_fixture('tasks')
        if name not in task_configs:
            return False, f"Task '{name}' not found"
        
        # Validate schema
        try:
            jsonschema.validate(task_configs[name], schema=TASK_SCHEMA)
            return True, None
        except jsonschema.exceptions.ValidationError as e:
            return False, f"Task '{name}' schema validation failed: {e.message}"
    
    @staticmethod
    @lru_cache(maxsize=128)
    def _validate_as_dependent(name):
        """
        Validate task dependencies (agent and callback).
        
        Args:
            name: Name of the task to validate
            
        Returns:
            Tuple[bool, Optional[str]]: (success, error_message)
        """
        # First validate schema
        ok, reason = Task._validate_schema(name)
        if not ok:
            return ok, reason
        
        # Get task config
        task_config = load_fixture('tasks')[name]
        
        # Validate agent
        agent_name = task_config.get('agent')
        if agent_name:
            ok, reason = Agent.validate(agent_name, recursive=False)
            if not ok:
                return False, f"Task '{name}' references invalid agent: {reason}"
        
        # Validate callback if present
        callback_id = task_config.get('callback')
        if callback_id:
            ok, reason = validate_callback(callback_id, recursive=False)
            if not ok:
                return False, f"Task '{name}' references invalid callback: {reason}"
        
        return True, None

    @staticmethod
    def task_graph():
        """
        Alias for _load_tasks_as_depend_graph.
        Returns the task dependency graph as (vertices, edges).
        """
        return Task._load_tasks_as_depend_graph()

    def __init__(self, config_name, *, agent_pool, task_pool, callbacks_available=None, **kwargs):
        task_config = load_fixture('tasks')[config_name]

        agent = agent_pool.get(task_config['agent'])
        task_config['agent'] = agent

        context = []
        depends_on = task_config.pop('depends_on', [])
        if isinstance(depends_on, str):
            depends_on = [depends_on]

        for context_name in depends_on:
            context.append(task_pool[context_name])
        task_config['context'] = context

        callback_id = task_config.get('callback', None)
        if callback_id:
            task_config['callback'] = callbacks_available[callback_id]

        task_pool[config_name] = self
        super().__init__(**task_config, **kwargs)
