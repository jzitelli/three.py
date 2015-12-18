from scipy import ndimage
from . import *


# class HeightfieldBufferGeometry(Three):
#     def __init__(self, heightfield=None, size=1, **kwargs):
#         Three.__init__(self, **kwargs)
#         self.heightfield = heightfield
#         self.size = size


class HeightfieldMesh(Mesh):
    def __init__(self, url_prefix="", heightfield=None, heightfieldScale=1, width=None, height=None, **kwargs):
        image = ndimage.imread(heightfield)
        if width is None:
            width = image.shape[0]
        if height is None:
            height = image.shape[1]
        geometry = PlaneBufferGeometry(widthSegments=image.shape[0]-1, heightSegments=image.shape[1]-1,
                                       width=width, height=height)
        Mesh.__init__(self, geometry=geometry, **kwargs)
        if not hasattr(self, 'userData'):
            self.userData = {}
        self.userData['heightfield'] = url_prefix + heightfield
        self.userData['heightfieldScale'] = heightfieldScale
    def find_images(self, images=None):
        images = Mesh.find_images(self, images=images)
        image = Image(url=self.userData['heightfield'])
        images[image.uuid] = image
        return images
    def json(self):
        d = Mesh.json(self)
        d['type'] = 'Mesh'
        return d
