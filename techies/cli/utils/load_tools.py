import os
import sys
from techies.fixture_loader import find_tools
from techies.tools import register_tool
from crewai.tools import BaseTool, tool
from pydantic import BaseModel, Field

def load_custom_tools():
    """
    Load custom tool files from the runtime directories.
    This function finds tool.py files and Python files in tools/ directories
    and executes them as scripts.
    
    The tool files should call register_tool() themselves to register any tools.
    Each tool file has access to:
    - BaseTool, tool from crewai.tools
    - BaseModel, Field from pydantic
    - register_tool from techies.tools
    
    Returns:
        int: Number of tool files loaded
    """
    # Get all tool files
    tool_files = find_tools()
    
    # Create a dictionary of globals to expose to the tool scripts
    exposed_globals = {
        'BaseTool': BaseTool,
        'tool': tool,
        'BaseModel': BaseModel,
        'Field': Field,
        'register_tool': register_tool
    }
    
    # Execute each tool file as a script with the exposed globals
    for tool_file in tool_files:
        try:
            # Read the file content
            with open(tool_file, 'r') as f:
                file_content = f.read()
            
            # Execute the file content with exposed globals
            # The tool file is expected to call register_tool() itself
            exec(file_content, exposed_globals)
        except Exception as e:
            print(f"Error loading tool file {tool_file}: {e}")
    
    return len(tool_files) 