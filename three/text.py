from . import *

class TextGeometry(Three):
    def __init__(self, name=None, text=None, **parameters):
        Three.__init__(self, name)
        self.text = text
        self.parameters = parameters
    def json(self):
        d = Three.json(self)
        d['text'] = self.text
        d['parameters'] = self.parameters
        return d
