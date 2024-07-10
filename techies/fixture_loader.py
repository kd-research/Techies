import os
import yaml

_fixture_dir = os.path.normpath(__file__ + '/../../fixtures')

def load_fixture(fixture_name):
    fixture_path = os.path.join(_fixture_dir, fixture_name+'.yml')
    with open(fixture_path, 'r') as f:
        obj = yaml.load(f, Loader=yaml.FullLoader)

    return obj

__all__ = ['load_fixture']
