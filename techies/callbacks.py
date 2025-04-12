import copy
import inspect
import re
from typing import Callable, Optional, Dict

# Global registry for callbacks
_registered_callbacks: Dict[str, Callable[[str], str]] = {}

def to_snake_case(name: str) -> str:
    """Convert a string to snake_case format.
    Example: 'FormatOutput' -> 'format_output'"""
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    return pattern.sub('_', name).lower()

def register_callback(callback_function: Callable[[str], str], callback_id: Optional[str] = None) -> str:
    """Register a callback function with an optional custom ID.
    If no ID is provided, it will use the function name.
    Returns the callback_id used for registration."""
    
    # Validate callback signature
    sig = inspect.signature(callback_function)
    if len(sig.parameters) != 1:
        raise ValueError(f"Callback function must accept exactly one parameter, got {len(sig.parameters)}")
    
    # Get callback ID from function name if not provided
    if callback_id is None:
        callback_id = to_snake_case(callback_function.__name__)
    
    _registered_callbacks[callback_id] = callback_function
    return callback_id

def get_all_callbacks():
    """Get all registered callback functions."""
    # Return a deep copy of the registered callbacks dictionary
    return copy.deepcopy(_registered_callbacks) 