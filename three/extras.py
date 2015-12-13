from . import *

class TextGeomObject3D(Object3D):
    def __init__(self, text=None, material=None, parameters=None, **kwargs):
        Object3D.__init__(self, **kwargs)
        self.text = text
        self.material = material
        self.parameters = parameters
    def json(self):
        d = Object3D.json(self)
        return d
