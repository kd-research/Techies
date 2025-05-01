import os
import sys
from techies.fixture_loader import find_callbacks
from techies.callbacks import register_callback
from typing import Callable

def load_custom_callbacks():
    """
    Load custom callback files from the runtime directories.
    This function finds callback.py files and Python files in callbacks/ directories
    and executes them as scripts.
    
    The callback files should call register_callback() themselves to register any callbacks.
    Each callback file has access to:
    - register_callback from techies.callbacks
    
    Returns:
        int: Number of callback files loaded
    """
    # Get all callback files
    callback_files = find_callbacks()
    
    # Create a dictionary of globals to expose to the callback scripts
    exposed_globals = {
        '__name__': '__main__',
        'register_callback': register_callback
    }
    
    # Execute each callback file as a script with the exposed globals
    for callback_file in callback_files:
        try:
            # Read the file content
            with open(callback_file, 'r') as f:
                file_content = f.read()
            
            # Execute the file content with exposed globals
            # The callback file is expected to call register_callback() itself
            exec(file_content, exposed_globals)
        except Exception as e:
            print(f"Error loading callback file {callback_file}: {e}")
    
    return len(callback_files) 