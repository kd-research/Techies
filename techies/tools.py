import copy
import inspect
import re
from typing import Type, Optional, Union

from crewai.tools import BaseTool

from .predefined_tools.read_file_tool import ReadFileTool
from .predefined_tools.batch_read_files_tool import BatchReadFilesTool
from .predefined_tools.write_file_tool import WriteFileTool
from .predefined_tools.list_files_tool import ListFilesTool
from .predefined_tools.sound_tools import SearchSoundTool, SaveSoundTool
from .predefined_tools.html_examples_tool import ReadHtmlExamplesTool

# Global registry for tools
_registered_tools = {}

def to_snake_case(name: str) -> str:
    """Convert a string to snake_case format.
    Example: 'ReadFileTool' -> 'read_file_tool'"""
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    return pattern.sub('_', name).lower()

def register_tool(tool_class_or_instance: Union[Type[BaseTool], BaseTool], tool_id: Optional[str] = None, set_no_cache: bool = False) -> str:
    """Register a tool class or tool instance with an optional custom ID.
    If no ID is provided, it will try to use the tool's id attribute,
    or convert the class name to snake_case.
    Returns the tool_id used for registration."""
    
    # Check if tool_class_or_instance is a class (to be instantiated) or an instance
    if inspect.isclass(tool_class_or_instance) and issubclass(tool_class_or_instance, BaseTool):
        # It's a class that inherits from BaseTool, instantiate it
        tool = tool_class_or_instance(base_dir=".")
        tool_class = tool_class_or_instance
    else:
        # It's already an instance (e.g., from the @tool decorator)
        tool = tool_class_or_instance
        tool_class = tool.__class__

    if set_no_cache:
    # Override cache function for the tool
        tool.cache_function = lambda args, result: False

    if tool_id is None:        
        if hasattr(tool_class_or_instance, 'id'):
            tool_id = tool_class_or_instance.id
        elif hasattr(tool, 'id'):
            tool_id = tool.id
        else:
            tool_id = to_snake_case(tool.name)
    
    _registered_tools[tool_id] = tool
    return tool_id

def get_all_tools():
    """Get all tools including both built-in and user-registered tools."""
    base_dir = "."

    # Register all built-in tools
    tool_classes = [
        ReadFileTool, BatchReadFilesTool, WriteFileTool, ListFilesTool,
        SaveSoundTool, SearchSoundTool, ReadHtmlExamplesTool, 
    ]
    
    for tool_class in tool_classes:
        register_tool(tool_class, set_no_cache=True)

    # Return a deep copy of the registered tools dictionary
    return copy.deepcopy(_registered_tools)
