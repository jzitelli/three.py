import PIL.Image

from .buffer_geometries import PlaneBufferGeometry
from .objects import Mesh


class HeightfieldMesh(Mesh):
    """A heightfield which is constructed by modifying the z-components of the vertices defined by PlaneBufferGeometry during the three.py.js postprocessing step."""
    def __init__(self, heightfieldImage=None, heightfieldScale=1, width=None, height=None, **kwargs):
        pil_image = PIL.Image.open(heightfieldImage.url)
        width, height = pil_image.width, pil_image.height
        geometry = PlaneBufferGeometry(widthSegments=width-1, heightSegments=height-1,
                                       width=width, height=height)
        Mesh.__init__(self, geometry=geometry, **kwargs)
        if not hasattr(self, 'userData'):
            self.userData = {}
        self.userData['heightfieldImage'] = str(heightfieldImage.uuid)
        self.userData['heightfieldScale'] = heightfieldScale
        self.heightfieldImage = heightfieldImage
    def find_images(self, images=None):
        images = Mesh.find_images(self, images=images)
        images[self.heightfieldImage.uuid] = self.heightfieldImage
        return images
    def json(self):
        d = Mesh.json(self)
        d['type'] = 'Mesh'
        d.pop('heightfieldImage')
        return d
