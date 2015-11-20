from collections import defaultdict
import uuid

import numpy as np


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
        """Returns a dict which can be JSON serialized (by json.dumps)"""
        try:
            return {"type": self.__class__.__name__,
                    "uuid": unicode(self.uuid),
                    "name": self.name}
        except NameError:
            return {"type": self.__class__.__name__,
                    "uuid": str(self.uuid),
                    "name": self.name}


class Object3D(Three):
    def __init__(self, name=None, position=(0,0,0), rotation=(0,0,0), scale=(1,1,1), visible=None, castShadow=None, receiveShadow=None, userData=None, **kwargs):
        Three.__init__(self, name)
        self.position = np.array(position, dtype=np.float64)
        self.rotation = np.array(rotation, dtype=np.float64)
        self.scale = np.array(scale, dtype=np.float64)
        self.children = []
        self.visible = visible
        self.castShadow = castShadow
        self.receiveShadow = receiveShadow
        self.userData = userData
    def add(self, *objs):
        self.children += objs
    def find_geometries(self, geometries=None):
        if geometries is None:
            geometries = {}
        for c in self.children:
            if hasattr(c, 'geometry'):
                geometries[c.geometry.uuid] = c.geometry
            c.find_geometries(geometries)
        return geometries
    def find_materials(self, materials=None):
        if materials is None:
            materials = {}
        for c in self.children:
            if hasattr(c, 'material'):
                materials[c.material.uuid] = c.material
            c.find_materials(materials)
        return materials
    def find_textures(self):
        textures = {}
        materials = self.find_materials()
        for mat in materials.values():
            if hasattr(mat, 'map'):
                textures[mat.map.uuid] = mat.map
            if hasattr(mat, 'bumpMap'):
                textures[mat.bumpMap.uuid] = mat.bumpMap
            # TODO
        return textures
    def find_images(self):
        images = {}
        textures = self.find_textures()
        for tex in textures.values():
            if hasattr(tex, 'image'):
                images[tex.image.uuid] = tex.image
        return images
    def json(self):
        d = Three.json(self)
        # TODO: ? 
        d['position'] = list(self.position.ravel())
        d['rotation'] = list(self.rotation.ravel())
        d['scale'] = list(self.scale.ravel())
        d['children'] = [c.json() for c in self.children]
        d.update({k: v for k, v in self.__dict__.items()
                  if v is not None and k not in d})
        return d
    def export(self, geometries=None, materials=None, textures=None, images=None):
        if geometries is None:
            geometries = self.find_geometries()
        if materials is None:
            materials = self.find_materials()
        if textures is None:
            textures = self.find_textures()
        if images is None:
            images = self.find_images()
        return {'object': self.json(),
                "geometries": [g.json() for g in geometries.values()],
                "materials": [m.json() for m in materials.values()],
                "textures": [t.json() for t in textures.values()],
                "images": [i.json() for i in images.values()]}


class Scene(Object3D):
	pass


class Mesh(Object3D):
    def __init__(self, geometry=None, material=None, **kwargs):
        Object3D.__init__(self, **kwargs)
        self.geometry = geometry
        self.material = material
    def json(self):
        d = Object3D.json(self)
        try:
            d.update({"material": unicode(self.material.uuid),
                      "geometry": unicode(self.geometry.uuid)})
        except NameError:
            d.update({"material": str(self.material.uuid),
                      "geometry": str(self.geometry.uuid)})
        return d
