from . import *

import os.path

class BufferGeometry(Three):
    def __init__(self, name=None, vertices=None, indices=None, normals=None, uvs=None):
        Three.__init__(self, name=name)
        self.vertices = vertices
        self.normals = normals
        self.indices = indices
        self.uvs = uvs
    def computeBoundingBox(self):
        vertices = self.vertices.reshape((-1, 3))
        return np.array([[vertices[:,0].min(), vertices[:,1].min(), vertices[:,2].min()],
                         [vertices[:,0].max(), vertices[:,1].max(), vertices[:,2].max()]])
    def json(self):
        d = Three.json(self)
        d['type'] = 'BufferGeometry' # to enforce the type when invoked from subclasses
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
                "type": "Uint16Array",
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
    "Return indices for two triangles comprising the quadrilateral"
    if flip_normals:
        return [[rect_face[0], rect_face[2], rect_face[1]], [rect_face[0], rect_face[3], rect_face[2]]]
    else:
        return [[rect_face[0], rect_face[1], rect_face[2]], [rect_face[0], rect_face[2], rect_face[3]]]


class QuadBufferGeometry(BufferGeometry):
    """Defines two triangles representing a quadrilateral (assuming they are coplanar).
    The indices are (0,1,2), (0,2,3)"""
    def __init__(self, vertices, uvs=None, **kwargs):
        BufferGeometry.__init__(self, vertices=vertices, uvs=uvs, indices=_tri_faces([0,1,2,3]), **kwargs)


class HexaBufferGeometry(BufferGeometry):
    # TODO: check if quads are coplanar
    faces = [[0,1,2,3][::-1], # bottom
             [4,5,6,7], # top
             [0,1,5,4], # front
             [1,2,6,5], # right
             [2,3,7,6], # rear
             [7,3,0,4]] # left
    def __init__(self, vertices=None, **kwargs):
        BufferGeometry.__init__(self, vertices=vertices,
                                indices=[_tri_faces(quad)
                                         for quad in HexaBufferGeometry.faces],
                                **kwargs)


class PrismBufferGeometry(BufferGeometry):
    """Vertex enumeration:
    0,1,2 - bottom triangle
    3,4,5 - top triangle
    The prism has edges (0,3), (1,4), (2,5)
    """
    def __init__(self, vertices, **kwargs):
        indices = [[0,1,2], [3,4,5][::-1]]
        for rect in [[0,1,4,3], [1,2,5,4], [2,0,3,5]]:
            indices += _tri_faces(rect[::-1], flip_normals=False)
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


class BoxBufferGeometry(BoxGeometry):
    pass
