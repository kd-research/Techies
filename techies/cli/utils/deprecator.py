import click
import functools
import warnings

def deprecated_command(new_command_path):
    """
    Decorator to mark a command as deprecated with a migration path.
    
    Args:
        new_command_path (str): The new command to use instead (e.g., 'list agents')
    
    Returns:
        callable: A decorator that will show a deprecation warning when the command is used
    """
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            # Show deprecation warning
            warning_message = (
                f"WARNING: This command is deprecated and will be removed in v2.0. "
                f"Please use 'techies {new_command_path}' instead."
            )
            click.secho(warning_message, fg='yellow')
            
            # Log a deprecation warning (for logs)
            warnings.warn(
                f"Command '{f.__name__}' is deprecated. Use '{new_command_path}' instead.",
                DeprecationWarning, 
                stacklevel=2
            )
            
            # Call the original function
            return f(*args, **kwargs)
        return wrapper
    return decorator 