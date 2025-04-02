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

def find_tools():
    """Find all tools.py files and Python files in tools/ folders under runtimedirs.
    Only searches first level in tools/ folders. Skips hidden and underscore-prefixed files."""
    tool_files = []
    
    for runtimedir in runtimedirs():
        # Look for tools.py in the root of each runtime directory
        tools_py = os.path.join(runtimedir, 'tools.py')
        if os.path.isfile(tools_py):
            tool_files.append(tools_py)
            
        # Look for Python files in tools/ folder (first level only)
        tools_dir = os.path.join(runtimedir, 'tools')
        if os.path.isdir(tools_dir):
            for item in os.listdir(tools_dir):
                # Skip hidden files and underscore-prefixed files
                if item.startswith('.') or item.startswith('_'):
                    continue
                if item.endswith('.py'):
                    tool_files.append(os.path.join(tools_dir, item))
    
    return tool_files

__all__ = ['load_fixture', 'find_tools']
