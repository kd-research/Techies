import click
from techies.tools import get_all_tools

@click.command()
def list_tools():
    """List all available tools, including custom tools."""
    tools = get_all_tools()
    
    if not tools:
        click.echo("No tools available.")
        return
    
    click.echo(f"Found {len(tools)} tools:")
    click.echo("-" * 80)
    
    for tool_id, tool in tools.items():
        click.echo(f"Tool ID: {tool_id}")
        click.echo(f"Name: {tool.name}")
        click.echo(f"Description: {tool.description}")
        
        if hasattr(tool, 'args_schema') and tool.args_schema:
            click.echo("Arguments:")
            for field_name, field in tool.args_schema.__fields__.items():
                field_desc = field.description or "No description"
                click.echo(f"  - {field_name}: {field_desc}")
        
        click.echo("-" * 80) 