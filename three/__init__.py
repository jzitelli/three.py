import json
import uuid
from collections import defaultdict

import numpy as np


# TODO: use pyexecjs to automatically define all three.js global constants
FrontSide  = 0
BackSide   = 1
DoubleSide = 2

FlatShading   = 1
SmoothShading = 2

NoColors     = 0
FaceColors   = 1
VertexColors = 2

UVMapping             = 300
CubeReflectionMapping = 301
CubeRefractionMapping = 302

RepeatWrapping         = 1000
ClampToEdgeWrapping    = 1001
MirroredRepeatWrapping = 1002

NearestFilter              = 1003
NearestMipMapNearestFilter = 1004
NearestMipMapLinearFilter  = 1005
LinearFilter               = 1006
LinearMipMapNearestFilter  = 1007
LinearMipMapLinearFilter   = 1008


# TODO: JSON encoder for Three objects
class Three(object):
    instance_num = defaultdict(int)
    def __init__(self, name=None):
        if name is None:
            type = self.__class__.__name__
            name = "unnamed %s %d" % (type, Three.instance_num[type])
            Three.instance_num[type] += 1
        self.name = name
        self.uuid = uuid.uuid4()
    def json(self):
        """Returns a dict which can be JSON-serialized (by json.dumps)"""
        try:
            return {"type": self.__class__.__name__,
                    "uuid": unicode(self.uuid),
                    "name": self.name}
        except NameError:
            return {"type": self.__class__.__name__,
                    "uuid": str(self.uuid),
                    "name": self.name}

        
# TODO: refactor url -> uri, add robust URI support
class Image(Three):
    def __init__(self, name=None, url=None):
        Three.__init__(self, name)
        self.url = url
    def json(self):
        d = Three.json(self)
        if self.url:
            d['url'] = self.url
        return d


# TODO: reorganize package hierarchy to make explicit separation between three.js "native" classes and which are "derived" / "convenience" classes introduced by three.py
from .objects import *
from .lights import *
from .materials import *
from .geometries import *
from .buffer_geometries import *

from .text import *
from .heightfields import *
