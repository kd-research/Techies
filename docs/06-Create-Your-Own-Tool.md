# Creating Your Own Tools in Techies

Techies allows you to extend its functionality by creating and registering your own custom tools. These tools can be used by agents in your crews to perform specialized tasks.

## How Tool Loading Works

Techies automatically discovers and loads custom tool files from your runtime directories when the `--allow-load-tools` flag is set. For security reasons, this flag must be explicitly provided to load custom tools.

```bash
techies --allow-load-tools <command>
```

## Creating a Custom Tool

You can create custom tools in two ways:

1. By subclassing `BaseTool`
2. By using the `tool` decorator

### Tool Files Location

Tools can be defined in two types of locations:
- A `tools.py` file in any runtime directory
- Any Python file within a `tools/` directory in any runtime directory

### Creating a Tool Using BaseTool

Here's an example of creating a custom tool by subclassing `BaseTool`:

```python
# Example custom tool using BaseTool

# These classes are automatically available in tool files
# BaseTool, tool - from crewai.tools
# BaseModel, Field - from pydantic
# register_tool - from techies.tools

class MyToolSchema(BaseModel):
    """Input schema for MyCustomTool."""
    query: str = Field(..., description="The search query to process.")
    
class MyCustomTool(BaseTool):
    name: str = "My Custom Tool"
    id: str = "my_custom_tool"  # Optional, will be auto-generated if not provided
    description: str = "A tool that performs a specialized function."
    args_schema: Type[BaseModel] = MyToolSchema
    
    def _run(self, query: str, **kwargs) -> str:
        # Your tool implementation goes here
        return f"Processed query: {query}"

# Register the tool (required)
register_tool(MyCustomTool)

# Register with custom ID
register_tool(MyCustomTool, tool_id="my_special_tool")
```

### Tool IDs and Registration

When registering a tool, you can provide an explicit ID using the optional `tool_id` parameter:

```python
# Register with custom ID
register_tool(MyCustomTool, tool_id="my_special_tool")
```

This ID is important because it's used in `agents.yaml` when you want to assign tools to agents:

```yaml
agents:
  researcher:
    role: Researcher
    goal: Find information about specific topics
    backstory: An expert researcher with years of experience
    tools:
      - my_special_tool  # This references the custom ID
```

If you don't provide an explicit ID when registering:
1. First, the tool's `id` attribute will be used if it exists
2. If that doesn't exist, the class name will be converted to snake_case (e.g., `MyCustomTool` → `my_custom_tool`)

### Creating a Tool Using the Decorator

Alternatively, you can use the `tool` decorator for simpler tools:

```python
# Example custom tool using decorator

@tool("My Decorator Tool")
def my_tool(query: str) -> str:
    """A simple tool that processes a query.
    
    Args:
        query: The text to process
    
    Returns:
        The processed result
    """
    # Your implementation here
    return f"Processed with decorator: {query}"

# Register the decorated tool
register_tool(my_tool)  # You can also use register_tool(my_tool, tool_id="custom_id")
```

## Important Notes

1. **Security Warning**: The `--allow-load-tools` flag runs code from your runtime directories. Only use this flag if you trust all code in these directories.

2. **Registration**: Tools must call `register_tool()` themselves to be registered with Techies.

3. **Tool IDs**: The ID used when registering a tool is what you'll reference in your agents.yaml file to make the tool available to agents.

4. **Available Imports**: The following imports are automatically available in your tool files:
   - `BaseTool` and `tool` from crewai.tools
   - `BaseModel` and `Field` from pydantic
   - `register_tool` from techies.tools

5. **Execution Context**: Each tool file is executed as a standalone script, not as a module. This means you can use top-level code to register your tools.

6. **Error Handling**: Errors during tool loading are reported but won't stop the application. Check the console output for any loading errors.

## Listing Available Tools

You can see all available tools, including your custom ones, using the `list tools` command:

```bash
techies --allow-load-tools list tools
```

This will show each tool's ID, which is what you need to use in your agents.yaml file.

## Advanced Tool Creation

For more advanced tool creation techniques, including structured tools and custom caching mechanisms, refer to the [CrewAI Tools documentation](https://docs.crewai.com/concepts/tools).

## Examples

### Example 1: Web Search Tool

```python
class WebSearchToolSchema(BaseModel):
    query: str = Field(..., description="The search query.")
    max_results: int = Field(5, description="Maximum number of results to return.")

class WebSearchTool(BaseTool):
    name: str = "Web Search"
    id: str = "web_search"
    description: str = "Search the web for information."
    args_schema: Type[BaseModel] = WebSearchToolSchema
    
    def _run(self, query: str, max_results: int = 5) -> str:
        # Implement web search functionality here
        results = [f"Result {i+1} for '{query}'" for i in range(max_results)]
        return "\n".join(results)

register_tool(WebSearchTool)  # The ID "web_search" will be used from the tool's id attribute
```

### Example 2: Simple Calculator Tool

```python
@tool("Calculator")
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression.
    
    Args:
        expression: The mathematical expression to evaluate
    
    Returns:
        The result of the evaluation
    """
    try:
        # Use safer eval with limited globals/locals
        result = eval(expression, {"__builtins__": {}}, {})
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

# Register with explicit ID for use in agents.yaml
register_tool(calculator, tool_id="math_calculator")
```

## See Also

- [Create Your Own Crew](./05-Create-Your-Own-Crew.md)
- [Modifying Existing Crews](./04-Modifying-Existing-Crews.md)
- [Understand Crew Configurations](./03-Understand-Crew-Configurations.md)
- [Getting Started with Techies](./01-Getting-Started-With-Techies.md)

Created and maintained by [Kaidong Hu](https://hukaidong.com) at [KD Research](https://github.com/kd-research). 