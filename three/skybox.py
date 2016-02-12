from . import *

class Skybox(Mesh):
    def __init__(self, cube_images=None, size=1000, **kwargs):
        if cube_images is None:
            cube_images = ['images/%s.png' % side
                           for side in ('px', 'nx', 'py', 'ny', 'pz', 'nz')]
        geometry = BoxGeometry(width=size, height=size, depth=size)
        shader = deepcopy(ShaderLib['cube'])
        shader['uniforms']['tCube']['value'] = cube_images
        material = ShaderMaterial(side=BackSide, **shader)
        Mesh.__init__(self, geometry=geometry, material=material, **kwargs)
    def json(self):
        d = Mesh.json(self)
        d['type'] = 'Mesh'
        return d
