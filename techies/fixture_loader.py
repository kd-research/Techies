import os
import yaml
import warnings

_fixture_dir = os.path.normpath(__file__ + '/../fixtures')

def load_fixture(fixture_name, result="objects"):
    merged = {}
    indexies = {}

    for runtimedir in runtimedirs():
        for extension in ['yaml', 'yml']:
            filename = os.path.join(runtimedir, f"{fixture_name}.{extension}")
            if os.path.isfile(filename):
                populate_fixture_from_file(merged, filename, indexies)

    if result == "objects":
        return merged
    elif result == "locations":
        return indexies

def runtime_config():
    # Only include current directory if .techiesbase is not present
    if os.path.isfile('.techiesbase'):
        runtimedir_default = _fixture_dir
    else:
        runtimedir_default = os.pathsep.join([_fixture_dir, "."])

    return os.environ.get('TECHIES_RUNTIME', runtimedir_default)

def runtimedirs():
    runtimedirs = []

    # Add runtime and first level subdirectories
    for path in runtime_config().split(os.pathsep):
        runtimedirs.append(path)
        for subpath in os.listdir(path):
            # avoid hidden or "_" prefixed directories
            if subpath.startswith('.') or subpath.startswith('_'):
                continue
            runtimedirs.append(os.path.join(path, subpath))

    realpaths = [os.path.realpath(d) for d in runtimedirs if os.path.isdir(d)]
    return set(realpaths)

def populate_fixture_from_file(merged, filename, indexies):
    with open(filename, 'r') as f:
        obj = yaml.load(f, Loader=yaml.FullLoader)

    for key in list(obj.keys()):
        if key.startswith('_'):
            obj.pop(key)

    conflicts = merged.keys() & obj.keys()
    for key in conflicts:
        warnings.warn(f"Instance {key} is defined multiple times. \n\tCurrent key located at {filename}\n\tWhile it has been defined in {indexies[key]}")

    merged.update(obj)
    indexies.update({key: filename for key in obj.keys()})

def find_scripts(script_type):
    """Find all [type].py files and Python files in [type]/ folders under runtimedirs.
    Only searches first level in [type]/ folders. Skips hidden and underscore-prefixed files.
    
    Args:
        script_type (str): Type of scripts to find (tools or callbacks)
    
    Returns:
        list: List of file paths
    """
    script_files = []
    
    for runtimedir in runtimedirs():
        # Look for [type].py in the root of each runtime directory
        script_py = os.path.join(runtimedir, f'{script_type}.py')
        if os.path.isfile(script_py):
            script_files.append(script_py)
            
        # Look for Python files in [type]/ folder (first level only)
        script_dir = os.path.join(runtimedir, script_type)
        if os.path.isdir(script_dir):
            for item in os.listdir(script_dir):
                # Skip hidden files and underscore-prefixed files
                if item.startswith('.') or item.startswith('_'):
                    continue
                if item.endswith('.py'):
                    script_files.append(os.path.join(script_dir, item))

    print(script_files)
    
    return script_files

def find_tools():
    """Find all tools.py files and Python files in tools/ folders under runtimedirs."""
    return find_scripts("tools")

def find_callbacks():
    """Find all callbacks.py files and Python files in callbacks/ folders under runtimedirs.""" 
    return find_scripts("callbacks")

__all__ = ['load_fixture', 'find_tools', 'find_callbacks']
