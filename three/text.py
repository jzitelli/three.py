# TODO
from . import *

class Font(Three):
    # TODO
    pass

class TextGeometry(Three):
    def __init__(self, name=None, text=None, **parameters):
        Three.__init__(self, name)
        self.text = text
        self.parameters = parameters
    def json(self):
        d = Three.json(self)
        d['text'] = self.text
        d['parameters'] = self.parameters
        d['url'] = self.parameters['url']
        #d.update({k: v for k, v in self.__dict__.items() if k not in d and v is not None})
        return d
