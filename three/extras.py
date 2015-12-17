from scipy import ndimage
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


class HeightfieldMesh(Mesh):
    def __init__(self, url_prefix="", heightfield=None, **kwargs):
        image = ndimage.imread(heightfield)
        width, height = image.shape[0], image.shape[1]
        geometry = PlaneBufferGeometry(widthSegments=image.shape[0]-1, heightSegments=image.shape[1]-1,
                                       width=width, height=height)
        Mesh.__init__(self, geometry=geometry, **kwargs)
        if not hasattr(self, 'userData'):            
            self.userData = {}
        self.userData['heightfield'] = url_prefix + heightfield
    def json(self):
        d = Mesh.json(self)
        d['type'] = 'Mesh'
        return d
