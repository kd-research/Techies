import pytest
import copy
from crewai.tools import BaseTool, tool
from pydantic import BaseModel, Field
from typing import Type
from techies.tools import get_all_tools, _registered_tools, register_tool, to_snake_case

class CustomToolSchema(BaseModel):
    param: str = Field(type=str, description="A test parameter")

class CustomTool(BaseTool):
    name: str = "Custom Test Tool"
    id: str = "custom_test_tool"
    description: str = "A test tool for unit testing"
    args_schema: Type[BaseModel] = CustomToolSchema
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def _run(self, **kwargs) -> str:
        return f"Custom tool ran with param: {kwargs.get('param', 'none')}"

def test_register_tool_function():
    """Test that register_tool correctly registers a custom tool."""
    # Clear any registered tools from previous tests
    _registered_tools.clear()
    
    # Register a custom tool
    tool_id = register_tool(CustomTool)
    
    # Verify the tool was registered with the correct ID
    assert tool_id == "custom_test_tool"
    assert tool_id in _registered_tools
    assert isinstance(_registered_tools[tool_id], CustomTool)

def test_register_tool_with_custom_id():
    """Test that register_tool works with a custom tool ID."""
    # Clear any registered tools from previous tests
    _registered_tools.clear()
    
    # Register a custom tool with a custom ID
    custom_id = "my_custom_id"
    tool_id = register_tool(CustomTool, custom_id)
    
    # Verify the tool was registered with the custom ID
    assert tool_id == custom_id
    assert tool_id in _registered_tools
    assert isinstance(_registered_tools[tool_id], CustomTool)

def test_register_tool_with_crewai_decorator():
    """Test that register_tool works with tools created using crewai's tool decorator."""
    # Clear any registered tools from previous tests
    _registered_tools.clear()
    
    # Create a tool using crewai's decorator
    @tool("Decorated Test Tool")
    def decorated_test_tool(test_param: str) -> str:
        """A test tool created with the decorator.
        
        Args:
            test_param: A test parameter
        """
        return f"Decorated tool ran with param: {test_param}"
    
    # Register the decorated tool
    tool_id = register_tool(decorated_test_tool, "decorated_test_tool")
    
    # Verify the tool was registered
    assert tool_id == "decorated_test_tool"
    assert tool_id in _registered_tools
    # The type check is skipped since crewai's tool decorator returns a different type

def test_register_tool_with_crewai_decorator_no_explicit_id():
    """Test that register_tool derives the correct ID from a camel case decorated tool name."""
    # Clear any registered tools from previous tests
    _registered_tools.clear()
    
    # Create a tool using crewai's decorator with camel case name
    @tool("CamelCaseToolName")
    def camel_case_tool(test_param: str) -> str:
        """A test tool with camel case name.
        
        Args:
            test_param: A test parameter
        """
        return f"CamelCase tool ran with param: {test_param}"
    
    # Register the decorated tool without explicit ID
    tool_id = register_tool(camel_case_tool)
    
    # The expected ID should be snake_case of the tool name
    expected_id = to_snake_case("CamelCaseToolName")
    
    # Verify the tool was registered with the correct ID
    assert tool_id == expected_id, f"Expected ID {expected_id}, got {tool_id}"
    assert tool_id in _registered_tools

def test_get_all_tools_returns_all_tools():
    """Test that get_all_tools returns all expected tools."""
    # Clear any registered tools from previous tests
    _registered_tools.clear()
    
    # Get all tools
    tools = get_all_tools()
    
    # Check if we have the expected number of tools
    expected_tool_ids = [
        'read_file',
        'batch_read_files',
        'write_file',
        'list_files',
        'save_sound',
        'search_sound',
        'read_examples_html'
    ]
    
    # Assert that all expected tools are present with their actual IDs
    for tool_id in expected_tool_ids:
        # Check if the tool exists with either the base ID or with _tool suffix
        assert (tool_id in tools) or (f"{tool_id}_tool" in tools), f"Tool '{tool_id}' not found in get_all_tools result"
        
        # Get the tool instance
        available_tool = tools.get(tool_id, tools.get(f"{tool_id}_tool"))
        # Check that the tool has a cache_function attribute and it's not None
        assert hasattr(available_tool, "cache_function"), f"Tool '{tool_id}' missing cache_function attribute"
        assert available_tool.cache_function is not None, f"Tool '{tool_id}' has None cache_function"

def test_get_all_tools_returns_deep_copy():
    """Test that get_all_tools returns a deep copy of the tools dictionary."""
    # Clear any registered tools from previous tests
    _registered_tools.clear()
    
    # Register a custom tool that we'll use for testing the deep copy
    custom_tool_id = register_tool(CustomTool)
    
    # Get all tools
    tools = get_all_tools()
    
    # Verify the custom tool is in the returned dictionary
    assert custom_tool_id in tools
    
    # Delete the custom tool from the returned dictionary
    del tools[custom_tool_id]
    
    # Get tools again and verify the custom tool is still there in the new copy
    tools_again = get_all_tools()
    assert custom_tool_id in tools_again, "get_all_tools should return a deep copy, not a reference"