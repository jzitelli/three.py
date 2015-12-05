"""Collection of functions which generate three.js scenes."""
from copy import deepcopy
import scipy.ndimage as ndimage

from three import *

FT2METERS   = 0.3048
INCH2METERS = FT2METERS / 12


square = QuadBufferGeometry(vertices=[[-0.5, 0, -0.5], [-0.5, 0, 0.5], [0.5, 0, 0.5], [0.5, 0, -0.5]],
                                 uvs=[(0,1), (0,0), (1,0), (1,1)])


def some_room(length=15.0, width=12.0, height=10.0):
    # TODO: Python 3 vs 2 division thing
    L, W, H = length, width, height
    yMin, yMax = -1.2, -1.2 + H
    xMin, xMax = -L/2, L/2
    zMin, zMax = -W/2, W/2
    yAvg = (yMin + yMax) / 2
    side_colors = [0xaaffff, 0xffffaa, 0xffaaff, 0xffaaaa, 0xaaffaa, 0xaaaaff]
    scene = Scene()
    scene.add(AmbientLight(color=0x151515))
    sphere = SphereBufferGeometry(radius=0.25)
    scene.add(PointLight(color=0xaa0000, intensity=0.8, distance=50,
                         position=[0.45 * L, yAvg, -0.4 * W]))
    scene.add(Mesh(geometry=sphere, position=[0.45 * L, yAvg, -0.4 * W], material=MeshBasicMaterial(color=0xaa0000)))
    scene.add(PointLight(color=0x00aa00, intensity=0.8, distance=50,
                         position=[-0.45 * L, yAvg, -0.4 * W]))
    scene.add(Mesh(geometry=sphere, position=[-0.45 * L, yAvg, -0.4 * W], material=MeshBasicMaterial(color=0x00aa00)))
    cannonData = {'mass': 0, 'shapes': ['Plane']}
    scene.add(Mesh(name="floor", geometry=square,
                   material=MeshBasicMaterial(color=0xffffff,
                                              map=Texture(image=Image(url="images/deck.png"),
                                                          repeat=[L, W], wrap=[RepeatWrapping, RepeatWrapping])),
                   position=[0, yMin, 0],
                   scale=[L, 1, W],
                   userData={'cannonData': cannonData}))
    scene.add(Mesh(name="ceiling", geometry=square,
                   material=MeshPhongMaterial(shading=FlatShading, color=side_colors[1]),
                   position=[0, yMax, 0],
                   rotation=[np.pi, 0, 0],
                   scale=[L, 1, W],
                   userData={'cannonData': cannonData}))
    scene.add(Mesh(name="front", geometry=square,
                   material=MeshPhongMaterial(shading=FlatShading, color=side_colors[2]),
                   position=[0, yAvg, zMax],
                   rotation=[np.pi/2, np.pi, 0],
                   scale=[L, 1, H],
                   userData={'cannonData': cannonData}))
    scene.add(Mesh(name="left", geometry=square,
                   material=MeshPhongMaterial(shading=FlatShading, color=side_colors[3]),
                   position=[xMin, yAvg, 0],
                   rotation=[np.pi/2, np.pi/2, 0],
                   scale=[W, 1, H],
                   userData={'cannonData': cannonData}))
    if ShaderLib is not None:
        shader = deepcopy(ShaderLib['cube'])
        shader['uniforms']['tCube']['value'] = ["images/skybox/%s.jpg" % pos
                                                for pos in ('px', 'nx', 'py', 'ny', 'pz', 'nz')]
        scene.add(Mesh(geometry=BoxGeometry(900, 900, 900),
                       material=ShaderMaterial(side=BackSide, **shader)))
    scene.add(Mesh(geometry=TextGeometry(text="This scene was generated by the Python function 'scenes.some_room'",
                                         parameters={'size': 0.2, 'height': 0.02, 'curveSegments': 3}),
                   material=MeshLambertMaterial(color=0x556699),
                   position=[-4.3, 1.6, -4]))
    return scene.export()


def shader_room(length=10, width=10, height=10):
    L, W, H = 1.0*length, 1.0*width, 1.0*height
    yMin, yMax = -1.2, -1.2 + H
    xMin, xMax = -L/2, L/2
    zMin, zMax = -W/2, W/2
    yAvg = (yMin + yMax) / 2
    scene = Scene()
    scene.add(AmbientLight(color=0x151515))
    scene.add(PointLight(color=0x880000, intensity=0.7, distance=50,
                         position=[0.45 * L, 0, -0.4 * W]))
    scene.add(PointLight(color=0x008800, intensity=0.7, distance=50,
                         position=[-0.45 * L, 0, -0.4 * W]))
    cannonData = {'mass': 0, 'shapes': ['Plane']}
    scene.add(Mesh(name="floor", geometry=square,
                   material=MeshBasicMaterial(side=FrontSide, color=0xffffff,
                                              map=Texture(image=Image("deck", url="images/deck.png"),
                                                          repeat=[L, W], wrap=[RepeatWrapping, RepeatWrapping])),
                   receiveShadow=True,
                   position=[0, yMin, 0],
                   scale=[L, 1, W],
                   userData={'cannonData': cannonData}))
    heightmap = 'images/terrain128.png'
    image = ndimage.imread(heightmap)
    scene.add(Mesh(name="heightfield",
                   geometry=PlaneBufferGeometry(width=L, height=W, widthSegments=image.shape[0]-1, heightSegments=image.shape[1]-1),
                   material=MeshLambertMaterial(color=0xffffff, shading=SmoothShading),
                   position=[L, -6, 0],
                   rotation=[-np.pi/2, 0, 0],
                   userData={'cannonData': {'mass': 0.0, 'shapes': ['Heightfield']},
                             'heightmap': heightmap}))
    return scene.export()


def underwater_tomb(length=25.0, width=25.0, height=30.0):
    L, W, H = length, width, height
    yMin, yMax = -1.2, -1.2 + H
    xMin, xMax = -L/2, L/2
    zMin, zMax = -W/2, W/2
    yAvg = (yMin + yMax) / 2
    side_colors = [0xaaffff, 0xffffaa, 0xffaaff, 0xffaaaa, 0xaaffaa, 0xaaaaff]
    scene = Scene()
    sphere = SphereBufferGeometry(radius=0.1)
    scene.add(PointLight(color=0x880000, intensity=0.8, distance=40,
                         position=[0.45 * L, yAvg, -0.4 * W]),
              Mesh(geometry=sphere, material=MeshBasicMaterial(color=0x880000),
                   position=[0.45 * L, yAvg, -0.4 * W]))
    scene.add(PointLight(color=0x008800, intensity=0.8, distance=40,
                         position=[-0.45 * L, yAvg, -0.4 * W]),
              Mesh(geometry=sphere, material=MeshBasicMaterial(color=0x008800),
                   position=[-0.45 * L, yAvg, -0.4 * W]))
    # cannonData = {'mass': 0, 'shapes': ['Plane']}
    # scene.add(Mesh(name="left", geometry=square,
    #                material=MeshPhongMaterial(shading=FlatShading, color=side_colors[3]),
    #                position=[xMin, yAvg, 0],
    #                rotation=[np.pi/2, np.pi/2, 0],
    #                scale=[W,1,H],
    #                userData={'cannonData': cannonData}))
    # scene.add(Mesh(name="right", geometry=square,
    #                material=MeshPhongMaterial(shading=FlatShading, color=side_colors[2]),
    #                position=[xMax, yAvg, 0],
    #                rotation=[np.pi/2, -np.pi/2, 0],
    #                scale=[W,1,H],
    #                userData={'cannonData': cannonData}))
    # scene.add(Mesh(name="front", geometry=square,
    #                material=MeshPhongMaterial(shading=FlatShading, color=side_colors[0]),
    #                position=[0, yAvg, zMax],
    #                rotation=[np.pi/2, np.pi, 0],
    #                scale=[L,1,H],
    #                userData={'cannonData': cannonData}))
    # scene.add(Mesh(name="back", geometry=square,
    #                material=MeshPhongMaterial(shading=FlatShading, color=side_colors[4]),
    #                position=[0, yAvg, zMin],
    #                rotation=[-np.pi/2, np.pi, 0],
    #                scale=[L,1,H],
    #                userData={'cannonData': cannonData}))
    # scene.add(Mesh(name="ceiling", geometry=square,
    #                material=MeshPhongMaterial(shading=FlatShading, color=side_colors[1]),
    #                position=[0, yMax, 0],
    #                rotation=[np.pi, 0, 0],
    #                scale=[L, 1, W],
    #                userData={'cannonData': cannonData}))
    heightmap = 'images/terrain256.png'
    image = ndimage.imread(heightmap)
    scene.add(Mesh(name="heightfield",
                   geometry=PlaneBufferGeometry(width=L, height=W, widthSegments=image.shape[0]-1, heightSegments=image.shape[1]-1),
                   material=MeshLambertMaterial(color=0xffffff, shading=SmoothShading),
                   position=[0, -4, 0],
                   rotation=[-np.pi/2, 0, 0],
                   userData={'cannonData': {
                               'mass': 0.0,
                               'shapes': ['Heightfield']
                              },
                              'heightmap': heightmap
                            }))
    return scene.export()


def basement():
    L, W, H = 20, 20, 8 * FT2METERS
    scene = Scene()
    floor = Mesh(name="floor", geometry=square,
                 material=MeshBasicMaterial(color=0xffffff,
                                            map=Texture(image=Image("deck", url="images/deck.png"), repeat=[L, W], wrap=[RepeatWrapping, RepeatWrapping])),
                 position=[0, 0, 0],
                 scale=[L,1,W],
                 userData={'cannonData': cannonData})
    scene.add(floor)
    def desk():
        top = Mesh(geometry=BoxGeometry(47 * IN2METERS, 1.75 * IN2METERS, 24 * IN2METERS),
            material=MeshLambertMaterial(color=0xaaaaaa))
        top.position[1] = (29 - 1.75 / 2) * IN2METERS
        obj = Object3D()
        obj.add(top)
        return obj
    scene.add(desk())
    return scene.export()


def pool_hall():
    scene = Scene()
    L, W = 7, 7
    scene.add(PointLight(color=0x225522, position=[6, 2, 0.5], intensity=0.5))
    floor = Mesh(name="floor", geometry=square,
                 material=MeshBasicMaterial(color=0xffffff,
                                            map=Texture(image=Image("deck", url="images/deck.png"), repeat=[L, W], wrap=[RepeatWrapping, RepeatWrapping])),
                 position=[0, 0, 0],
                 scale=[L,1,W])
    scene.add(floor)
    # 8ft table:
    y_table = 0.876
    pool_table = Mesh(geometry=BoxGeometry(1.17, y_table, 2.34),
                      material=MeshPhongMaterial(color=0x00aa00, shininess=5), #MeshLambertMaterial(color=0x00aa00),
                      position=[0, y_table / 2, 0],
                      receiveShadow=True,
                      userData={'cannonData': {'mass': 0, 'shapes': ['Box']}})
    scene.add(pool_table)
    # TODO: lights casting shadows w/ CrapLoader
    # spotLight = SpotLight(color=0xffffff, intensity=2, distance=6, position=[0, 3*y_table, 0],
    #                       castShadow=True, shadowCameraNear=0.2, shadowCameraFar=2*y_table, shadowCameraFov=80)
    # scene.add(spotLight)
    radius = 0.05715 / 2
    sphere = SphereBufferGeometry(radius=radius, widthSegments=16, heightSegments=32)
    userData = {'cannonData': {'mass': 0.17, 'shapes': ['Sphere']}}
    cue_ball = Mesh(geometry=sphere,
                    material=MeshPhongMaterial(color=0xeeeeee),
                    position=[0, y_table + radius + 0.001, 0.7],
                    castShadow=True,
                    userData=userData)
    scene.add(cue_ball)
    ball01 = Mesh(geometry=sphere, material=MeshPhongMaterial(color=0xee0000),
                  position=[0, y_table + radius + 0.001, -0.7], castShadow=True, userData=userData)
    scene.add(ball01)
    ball02 = Mesh(geometry=sphere, material=MeshPhongMaterial(color=0x00ee00),
                  position=[0, y_table + radius + 0.001, 0], castShadow=True, userData=userData)
    scene.add(ball02)
    ball03 = Mesh(geometry=sphere, material=MeshPhongMaterial(color=0xddee00),
                  position=[1.17 / 3, y_table + radius + 0.001, 0], castShadow=True, userData=userData)
    scene.add(ball03)
    if ShaderLib is not None:
        shader = deepcopy(ShaderLib['cube'])
        shader['uniforms']['tCube']['value'] = ["images/skybox/%s.jpg" % pos
                                                for pos in ('px', 'nx', 'py', 'ny', 'pz', 'nz')]
        scene.add(Mesh(geometry=BoxGeometry(900, 900, 900),
                       material=ShaderMaterial(side=BackSide, **shader)))
    return scene.export()
