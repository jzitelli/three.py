# TODO
from . import *

class TextObject3D(Object3D):
    def __init__(self, text=None, material=None, parameters=None, **kwargs):
        Object3D.__init__(self, **kwargs)
        self.text = text
        self.material = material
        self.parameters = parameters
    def json(self):
        d = Object3D.json(self)
        return d


class TextGeometry(Three):
    def __init__(self, name=None, text=None, **parameters):
        Three.__init__(self, name)
        self.text = text
        self.parameters = parameters
    def json(self):
        d = Three.json(self)
        d['text'] = self.text
        d['parameters'] = self.parameters
        #d.update({k: v for k, v in self.__dict__.items() if k not in d and v is not None})
        return d
