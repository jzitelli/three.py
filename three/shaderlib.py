import os.path
import json
import logging
_logger = logging.getLogger(__name__)

from . import *

# TODO: http://stackoverflow.com/questions/10935127/way-to-access-resource-files-in-python
SHADERLIB_PATH = os.path.join(os.path.split(__file__)[0], 'ShaderLib.json')
try:
    with open(SHADERLIB_PATH) as f:
        ShaderLib = json.loads(f.read())
    print('available shaders:\n' + '  \n'.join(ShaderLib.keys()))
except Exception as err:
    print("%s could not be loaded: %s" % (SHADERLIB_PATH, err))
    ShaderLib = None
