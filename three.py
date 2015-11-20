"""Define three.js objects from Python with this module.

These Python classes can be serialized and loaded (w/ some massaging, see three.py.js) by THREE.ObjectLoader.
"""

import json
import uuid
from collections import defaultdict
import numpy as np


class Object3D(Three):
    def __init__(self, name=None, position=(0,0,0), rotation=(0,0,0), scale=(1,1,1), visible=None, castShadow=None, receiveShadow=None, userData=None, **kwargs):
        # TODO: use kwargs, don't convert to ndarray?
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
    def __init__(self, **kwargs):
        Object3D.__init__(self, **kwargs)


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


class Light(Object3D):
    def __init__(self, color=0xffffff, intensity=None, distance=None,
                 shadowCameraNear=None, shadowCameraFar=None, shadowCameraFov=None,
                 **kwargs):
        Object3D.__init__(self, **kwargs)
        self.color = color
        self.intensity = intensity
        self.distance  = distance
        self.shadowCameraNear = shadowCameraNear
        self.shadowCameraFar  = shadowCameraFar
        self.shadowCameraFov  = shadowCameraFov


class AmbientLight(Light):
    pass


class PointLight(Light):
    pass


class DirectionalLight(Light):
    # TODO: specifying direction
    def __init__(self, target=None, **kwargs):
        Light.__init__(self, **kwargs)
        self.target = target


class SpotLight(Light):
    # TODO: set target (ObjectLoader does not support)
    def __init__(self, angle=None, exponent=None, decay=None, target=None, **kwargs):
        Light.__init__(self, **kwargs)
        self.angle = angle
        self.exponent = exponent
        self.decay = decay
        self.target = target


class PerspectiveCamera(Object3D):
    def __init__(self, fov=50, aspect=1, near=0.1, far=1000, **kwargs):
        Object3D.__init__(self, **kwargs)
        self.fov = fov
        self.aspect = aspect
        self.near = near
        self.far = far


class Material(Three):
    def __init__(self, name=None, **kwargs):
        Three.__init__(self, name)
        self.__dict__.update(kwargs)
    def json(self):
        d = Three.json(self)
        for k in ['map', 'alphaMap', 'bumpMap', 'normalMap', 'displacementMap', 'specularMap', 'envMap', 'lightMap', 'aoMap']:
            if k in self.__dict__:
                try:
                    d[k] = unicode(self.__dict__[k].uuid)
                except NameError:
                    d[k] = str(self.__dict__[k].uuid)
        d.update({k: v for k, v in self.__dict__.items() if k not in d})
        return d


class MeshBasicMaterial(Material):
    pass


class MeshLambertMaterial(Material):
    pass


class MeshPhongMaterial(Material):
    pass


class ShaderMaterial(Material):
    def __init__(self, vertexShader=None, fragmentShader=None, uniforms=None, **kwargs):
        Material.__init__(self, **kwargs)
        self.vertexShader = vertexShader
        self.fragmentShader = fragmentShader
        self.uniforms = uniforms


class RawShaderMaterial(ShaderMaterial):
    pass


class Texture(Three):
    def __init__(self, name=None, minFilter=LinearMipMapLinearFilter, magFilter=LinearFilter,
                 mapping=UVMapping, anisotropy=1,
                 image=None, wrap=None, repeat=None):
        Three.__init__(self, name)
        self.minFilter = minFilter
        self.magFilter = magFilter
        self.mapping = mapping
        self.anisotropy = anisotropy
        self.image = image
        self.repeat = repeat
        self.wrap = wrap
    def json(self):
        d = Three.json(self)
        if self.image:
            try:
                d['image'] = unicode(self.image.uuid)
            except NameError:
                d['image'] = str(self.image.uuid)
        d.update({k: v for k, v in self.__dict__.items() if v is not None and k not in d})
        return d


class Image(Three):
    def __init__(self, name=None, url=None):
        Three.__init__(self, name)
        self.url = url
    def json(self):
        d = Three.json(self)
        d['url'] = self.url
        return d


class Geometry(Three):
    def __init__(self, name=None, vertices=None, colors=None, faces=None):
        Three.__init__(self, name)
        self.vertices = vertices
        self.colors = colors
        self.faces = faces
    def json(self):
        d = Three.json(self)
        d.update({k: v for k, v in self.__dict__.items() if k not in d and v is not None})
        return d


class BoxGeometry(Geometry):
    def __init__(self, width=1, height=1, depth=1, widthSegments=1, heightSegments=1, depthSegments=1, **kwargs):
        Three.__init__(self, **kwargs)
        self.width = width
        self.height = height
        self.depth = depth
        self.widthSegments = widthSegments
        self.heightSegments = heightSegments
        self.depthSegments = depthSegments


class CylinderGeometry(Geometry):
    def __init__(self, radiusTop=20, radiusBottom=20, height=100,
                 radialSegments=8, heightSegments=1,
                 openEnded=False, thetaStart=None, thetaLength=None, **kwargs):
        Three.__init__(self)
        self.radiusTop = radiusTop
        self.radiusBottom = radiusBottom
        self.height = height
        self.radialSegments = radialSegments
        self.heightSegments = heightSegments
        self.openEnded = openEnded
        self.thetaStart = thetaStart
        self.thetaLength = thetaLength


class DodecahedronGeometry(Geometry):
    def __init__(self, radius=1, detail=0, **kwargs):
        Geometry.__init__(self)
        self.radius = radius
        self.detail = detail


class TorusGeometry(Three):
    def __init__(self, name=None, radius=100, tube=40, radialSegments=8, tubularSegments=6, arc=2*np.pi):
        Three.__init__(self, name)
        self.radius = radius
        self.tube = tube
        self.radialSegments = radialSegments
        self.tubularSegments = tubularSegments
        self.arc = arc


class OctahedronGeometry(Three):
    def __init__(self, name=None, radius=1, detail=0):
        Three.__init__(self, name)
        self.radius = radius
        self.detail = detail


class PolyhedronGeometry(Three):
    def __init__(self, name=None, vertices=None, faces=None, radius=None, detail=0):
        Three.__init__(self, name)
        self.vertices = vertices
        self.faces = faces
        self.radius = radius
        self.detail = detail


class BufferGeometry(Three):
    def __init__(self, name=None, vertices=None, indices=None, normals=None, uvs=None):
        Three.__init__(self, name)
        self.vertices = vertices
        self.normals = normals
        self.indices = indices
        self.uvs = uvs
    def json(self):
        d = Three.json(self)
        d['type'] = "BufferGeometry"
        d.update({"data": {
                    "attributes": {
                      "position": {
                        "type": "Float32Array",
                        "itemSize": 3,
                        "array": np.array(self.vertices).ravel().tolist()
                      }
                    }
                  }})
        if self.indices:
            d['data']['index'] = {
                "itemSize": 1,
                "type": "Uint32Array",
                "array": np.array(self.indices).ravel().tolist()
            }
        if self.normals:
            d['data']['attributes']['normal'] = {
                "type": "Float32Array",
                "itemSize": 3,
                "array": np.array(self.normals).ravel().tolist()
            }
        if self.uvs:
            d['data']['attributes']['uv'] = {
                "type": "Float32Array",
                "itemSize": 2,
                "array": np.array(self.uvs).ravel().tolist()
            }
        return d


def _tri_faces(rect_face, flip_normals=False):
    "Return indices for two triangles comprising the rectangle"
    faces = [[rect_face[0], rect_face[1], rect_face[2]], [rect_face[0], rect_face[2], rect_face[3]]]
    if flip_normals:
        faces[0] = faces[0][::-1]
        faces[1] = faces[1][::-1]
    return faces


class QuadBufferGeometry(BufferGeometry):
    """Defines two triangles representing a quadrilateral (assuming they are coplanar).
    """
    def __init__(self, vertices, uvs=None, **kwargs):
        BufferGeometry.__init__(self, vertices=vertices, uvs=uvs, indices=_tri_faces([0,1,2,3]), **kwargs)


class HexaBufferGeometry(BufferGeometry):
    """Hexahedron w/ conventional (to me) vertex enumeration
    """
    def __init__(self, vertices, **kwargs):
        rects = [[0,1,2,3], # bottom
                 [4,7,6,5], # top
                 [0,4,5,1], # back
                 [2,1,5,6], # right
                 [3,2,6,7], # front
                 [0,3,7,4]] # left
        BufferGeometry.__init__(self, vertices=vertices,
            indices=[_tri_faces(rect) for rect in rects],
            **kwargs)


class PrismBufferGeometry(BufferGeometry):
    """Vertex enumeration:
    0,1,2 - bottom triangle
    3,4,5 - top triangle
    The prism has edges (0,3), (1,4), (2,5)
    """
    def __init__(self, vertices, **kwargs):
        indices = [[0,1,2][::-1], [3,4,5]]
        for rect in [[0,1,4,3], [1,2,5,4], [2,0,3,5]]:
            indices += _tri_faces(rect)
        BufferGeometry.__init__(self, vertices=vertices,
                                indices=indices, **kwargs)


class TetrahedronBufferGeometry(BufferGeometry):
    def __init__(self, vertices, **kwargs):
        indices = [[0,1,2],
                   [0,3,1],
                   [0,2,3],
                   [3,2,1]]
        BufferGeometry.__init__(self, vertices=vertices, indices=indices, **kwargs)


class PlaneBufferGeometry(Three):
    def __init__(self, name=None, width=1, height=1, widthSegments=1, heightSegments=1):
        Three.__init__(self, name)
        self.width = width
        self.height = height
        self.widthSegments = widthSegments
        self.heightSegments = heightSegments
    def json(self):
        d = Three.json(self)
        d.update({k: v for k, v in self.__dict__.items() if k not in d})
        return d


class SphereBufferGeometry(Three):
    def __init__(self, name=None, radius=50, widthSegments=8, heightSegments=6, phiStart=None, phiLength=None, thetaStart=None, thetaLength=None):
        Three.__init__(self, name)
        self.radius = radius
        self.widthSegments = widthSegments
        self.heightSegments = heightSegments
        self.phiStart = phiStart
        self.phiLength = phiLength
        self.thetaStart = thetaStart
        self.thetaLength = thetaLength
    def json(self):
        d = Three.json(self)
        d.update({k: v for k, v in self.__dict__.items() if k not in d and v is not None})
        return d


class CircleBufferGeometry(Three):
    def __init__(self, name=None, radius=50, segments=8, thetaStart=None, thetaLength=None):
        Three.__init__(self, name)
        self.radius = radius
        self.segments = segments
        self.thetaStart = thetaStart
        self.thetaLength = thetaLength
    def json(self):
        d = Three.json(self)
        d.update({k: v for k, v in self.__dict__.items() if k not in d and v is not None})
        return d


class TextGeometry(Three):
    def __init__(self, name=None, text=None, parameters=None):
        Three.__init__(self, name)
        self.text = text
        self.parameters = parameters
    def json(self):
        d = Three.json(self)
        d.update({k: v for k, v in self.__dict__.items() if k not in d and v is not None})
        return d


def text_geom_alphabet(**kwargs):
    """Constructs a dict mapping string character -> TextGeometry
    """
    alphas  = "abcdefghijklmnopqrstuvwxyz"
    alphas += alphas.upper()
    digits  = '0123456789'
    symbols = r""",./;'[]\-=<>?:"{}|_+`~!@#$%^&*()"""
    characters = alphas + digits + symbols
    geometries = {c: TextGeometry(name="%s TextGeometry" % c, text=c, parameters=kwargs)
                  for c in characters}
    return geometries
