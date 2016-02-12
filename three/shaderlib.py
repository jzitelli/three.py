import os.path
import json

from . import *

# TODO: http://stackoverflow.com/questions/10935127/way-to-access-resource-files-in-python
SHADERLIB_PATH = os.path.join(os.path.split(__file__)[0], os.path.pardir, 'shaderlib')

try:
    with open(os.path.join(SHADERLIB_PATH, 'ShaderLib.json')) as f:
        ShaderLib = json.loads(f.read())
except Exception as err:
    ShaderLib = None

try:
    with open(os.path.join(SHADERLIB_PATH, 'UniformsLib.json')) as f:
        UniformsLib = json.loads(f.read())
except Exception as err:
    UniformsLib = None

try:
    with open(os.path.join(SHADERLIB_PATH, 'ShaderChunk.json')) as f:
        ShaderChunk = json.loads(f.read())
except Exception as err:
    ShaderChunk = None
