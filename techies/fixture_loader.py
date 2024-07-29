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
            runtimedirs.append(os.path.join(path, subpath))

    return [runtimedir for runtimedir in runtimedirs if os.path.isdir(runtimedir)]

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

__all__ = ['load_fixture']
