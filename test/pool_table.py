"""
three.js/Cannon.js pool table definition
"""
import json

from flask import Blueprint, Markup, render_template

from flask_app import WebVRConfig

from three import *

import numpy as np



blueprint = Blueprint('pool_table', __name__)

@blueprint.route('/pool_table')
def _pool_table():
    scene = pool_hall()
    scene.add(PointLight(intensity=0.5, position=[2, 4, -1]))
    return render_template('template.html',
                           json_config=Markup(r"""<script>
var WebVRConfig = %s;
var THREEPY_SCENE = %s;
</script>""" % (json.dumps(WebVRConfig, indent=2),
                json.dumps(scene.export(url_prefix="test/")))))



IN2METER = 0.0254
FT2METER = IN2METER / 12



def pool_table(L_table=2.3368, W_table=None, H_table=0.74295,
               L_playable=None, W_playable=None,
               ball_diameter=2.25*IN2METER,
               W_cushion=2*IN2METER, H_cushion=None, W_rail=None,
               **kwargs):
    """
    Creates parameterized three.js pool table

    :param L_table: length of the pool table (longer than the playable surface); default is 8ft.
    :param W_table: width the of the pool table; usually half the length.
    :param H_table: height of the playable surface; if no transformations are applied to the pool table
                    `Object3D`, the base/bottom of the pool table is at `y=0` and the playable surface is at `y=H_table`.
    :param L_playable: length of the playable area, I still don't understand exactly what it refers to
    :param W_cushion: width of the cushions
    :param H_cushion: height of the nose of the cushions; default is 63.5% of ball diameter
    """
    if W_table is None:
        W_table = 0.5*L_table
    if L_playable is None:
        L_playable = L_table - 2*W_cushion
    if W_playable is None:
        W_playable = W_table - 2*W_cushion
    if H_cushion is None:
        H_cushion = 0.635 * ball_diameter
    if W_rail is None:
        W_rail = 1.5*W_cushion
    H_rail = 1.25 * H_cushion

    poolTable = Object3D(name="poolTable")

    headSpotMaterial = MeshLambertMaterial(name="headSpotMaterial", color=0xcccccc)
    surfaceMaterial = MeshPhongMaterial(name="surfaceMaterial", color=0x00aa00, shininess=5, shading=FlatShading)
    cushionMaterial = MeshPhongMaterial(name="cushionMaterial", color=0x028844, shininess=5, shading=FlatShading)
    railMaterial = MeshPhongMaterial(name="railMaterial", color=0xdda400, shininess=10, shading=FlatShading)

    thickness = IN2METER
    playableSurfaceGeom = BoxBufferGeometry(W_playable, thickness, L_playable)
    playableSurfaceMesh = Mesh(name='playableSurfaceMesh',
                               geometry=playableSurfaceGeom,
                               material=surfaceMaterial,
                               position=[0, H_table - 0.5*thickness, 0],
                               receiveShadow=True,
                               userData={'cannonData': {'mass': 0,
                                                        'shapes': ['Box']}})
    poolTable.add(playableSurfaceMesh)

    ball_radius = ball_diameter / 2
    spotGeom = CircleBufferGeometry(name='spotGeom', radius=0.7*ball_radius, segments=5)
    headSpotMesh = Mesh(geometry=spotGeom,
                        material=headSpotMaterial,
                        position=[0, H_table + 0.0002, 0.25*L_table],
                        rotation=[-np.pi/2, 0, 0],
                        receiveShadow=True)
    poolTable.add(headSpotMesh)

    H_nose = 0.5 * H_cushion
    W_nose = 0.05 * W_cushion

    sqrt2 = np.sqrt(2)

    headCushionGeom = HexaBufferGeometry(vertices=np.array([
        # bottom quad:
        [[-0.5*W_playable + 0.4*W_cushion,       0,                   0.5*W_cushion],
         [ 0.5*W_playable - 0.4*W_cushion,       0,                   0.5*W_cushion],
         [ 0.5*W_playable - 1.2*sqrt2*W_cushion, H_cushion - H_nose, -0.5*W_cushion + W_nose],
         [-0.5*W_playable + 1.2*sqrt2*W_cushion, H_cushion - H_nose, -0.5*W_cushion + W_nose]],
        # top quad:
        [[-0.5*W_playable + 0.4*W_cushion,       H_rail,     0.5*W_cushion],
         [ 0.5*W_playable - 0.4*W_cushion,       H_rail,     0.5*W_cushion],
         [ 0.5*W_playable - 1.2*sqrt2*W_cushion, H_cushion, -0.5*W_cushion],
         [-0.5*W_playable + 1.2*sqrt2*W_cushion, H_cushion, -0.5*W_cushion]]]))

    rightHeadCushionGeom = HexaBufferGeometry(vertices=headCushionGeom.vertices.copy())
    rightHeadCushionGeom.vertices[0, 2, 0] = 0.5*W_playable - 0.6*sqrt2*W_cushion
    rightHeadCushionGeom.vertices[1, 2, 0] = rightHeadCushionGeom.vertices[0, 2, 0]

    leftHeadCushionGeom = HexaBufferGeometry(vertices=headCushionGeom.vertices.copy())
    leftHeadCushionGeom.vertices[0, 3, 0] = -0.5*W_playable + 0.6*sqrt2*W_cushion
    leftHeadCushionGeom.vertices[1, 3, 0] = leftHeadCushionGeom.vertices[0, 3, 0]

    cushionData = {'cannonData': {'mass': 0, 'shapes': ['ConvexPolyhedron']}}

    headCushionMesh = Mesh(name='headCushionMesh',
                           geometry=headCushionGeom,
                           material=cushionMaterial,
                           position=[0, H_table, 0.5*L_table - 0.5*W_cushion],
                           receiveShadow=True,
                           userData=cushionData)
    poolTable.add(headCushionMesh)
    footCushionMesh = Mesh(name='footCushionMesh',
                           geometry=headCushionGeom,
                           material=cushionMaterial,
                           position=[0, H_table, -0.5*L_table + 0.5*W_cushion],
                           rotation=[0, np.pi, 0],
                           receiveShadow=True,
                           userData=cushionData)
    poolTable.add(footCushionMesh)
    leftHeadCushionMesh = Mesh(name='leftHeadCushionMesh',
                               geometry=leftHeadCushionGeom,
                               material=cushionMaterial,
                               position=[-0.5*W_table + 0.5*W_cushion, H_table, 0.25*L_table],
                               rotation=[0, -np.pi/2, 0],
                               receiveShadow=True,
                               userData=cushionData)
    poolTable.add(leftHeadCushionMesh)
    leftFootCushionMesh = Mesh(name='leftFootCushionMesh',
                               geometry=rightHeadCushionGeom,
                               material=cushionMaterial,
                               position=[-0.5*W_table + 0.5*W_cushion, H_table, -0.25*L_table],
                               rotation=[0, -np.pi/2, 0],
                               receiveShadow=True,
                               userData=cushionData)
    poolTable.add(leftFootCushionMesh)
    rightHeadCushionMesh = Mesh(name='rightHeadCushionMesh',
                                geometry=rightHeadCushionGeom,
                                material=cushionMaterial,
                                position=[0.5*W_table - 0.5*W_cushion, H_table, 0.25*L_table],
                                rotation=[0, np.pi/2, 0],
                                receiveShadow=True,
                                userData=cushionData)
    poolTable.add(rightHeadCushionMesh)
    rightFootCushionMesh = Mesh(name='rightFootCushionMesh',
                                geometry=leftHeadCushionGeom,
                                material=cushionMaterial,
                                position=[0.5*W_table - 0.5*W_cushion, H_table, -0.25*L_table],
                                rotation=[0, np.pi/2, 0],
                                receiveShadow=True,
                                userData=cushionData)
    poolTable.add(rightFootCushionMesh)

    headRailGeom = BoxBufferGeometry(W_playable - 2*0.4*W_cushion, H_rail, W_rail)
    railData = {'cannonData': {'mass': 0, 'shapes': ['Box']}}
    headRailMesh = Mesh(name='headRailMesh',
                        geometry=headRailGeom,
                        material=railMaterial,
                        position=[0, H_table + 0.5*H_rail, 0.5*L_table + 0.5*W_rail],
                        receiveShadow=True,
                        userData=railData)
    poolTable.add(headRailMesh)
    footRailMesh = Mesh(name='footRailMesh',
                        geometry=headRailGeom,
                        material=railMaterial,
                        position=[0, H_table + 0.5*H_rail, -(0.5*L_table + 0.5*W_rail)],
                        rotation=[0, np.pi, 0],
                        receiveShadow=True,
                        userData=railData)
    poolTable.add(footRailMesh)
    leftHeadRailMesh = Mesh(name='leftHeadRailMesh',
                            geometry=headRailGeom,
                            material=railMaterial,
                            position=[-(0.5*W_table + 0.5*W_rail), H_table + 0.5*H_rail, 0.25*L_table],
                            rotation=[0, np.pi/2, 0],
                            receiveShadow=True,
                            userData=railData)
    poolTable.add(leftHeadRailMesh)
    rightHeadRailMesh = Mesh(name='rightHeadRailMesh',
                             geometry=headRailGeom,
                             material=railMaterial,
                             position=[0.5*W_table + 0.5*W_rail, H_table + 0.5*H_rail, 0.25*L_table],
                             rotation=[0, np.pi/2, 0],
                             receiveShadow=True,
                             userData=railData)
    poolTable.add(rightHeadRailMesh)
    leftFootRailMesh = Mesh(name='leftFootRailMesh',
                            geometry=headRailGeom,
                            material=railMaterial,
                            position=[-(0.5*W_table + 0.5*W_rail), H_table + 0.5*H_rail, -0.25*L_table],
                            rotation=[0, np.pi/2, 0],
                            receiveShadow=True,
                            userData=railData)
    poolTable.add(leftFootRailMesh)
    rightFootRailMesh = Mesh(name='rightFootRailMesh',
                             geometry=headRailGeom,
                             material=railMaterial,
                             position=[0.5*W_table + 0.5*W_rail, H_table + 0.5*H_rail, -0.25*L_table],
                             rotation=[0, np.pi/2, 0],
                             receiveShadow=True,
                             userData=railData)
    poolTable.add(rightFootRailMesh)

    return poolTable



def pool_hall(useSkybox=False,
              L_table=2.3368,
              H_table=0.74295,
              ball_diameter=2.25*IN2METER,
              url_prefix="",
              **kwargs):
    """
    Defines a three.js scene containing a pool table + billiard balls.
    """
    scene = Scene()
    L_room, W_room = 10, 10
    floorMesh = Mesh(name="floorMesh",
                     geometry=PlaneBufferGeometry(width=W_room, height=L_room),
                     material=MeshBasicMaterial(color=0xffffff,
                                                map=Texture(image=Image(url=url_prefix+"images/marble.png"),
                                                            repeat=[2.5, 2.5], wrap=[RepeatWrapping, RepeatWrapping])),
                     position=[0, 0, 0],
                     rotation=[-np.pi/2, 0, 0],
                     userData={'cannonData': {'mass': 0,
                                              'shapes': ['Plane']}})
    scene.add(floorMesh)

    if useSkybox:
        scene.add(Skybox(cube_images=[url_prefix + "images/%s.png" % pos
                                      for pos in ('px', 'nx', 'py', 'ny', 'pz', 'nz')]))

    poolTable = pool_table(L_table=L_table, H_table=H_table, ball_diameter=ball_diameter,
                           **kwargs)
    scene.add(poolTable)

    # balls:
    ball_colors = []
    ball_colors.append(0xddddde); white  = ball_colors[-1]
    ball_colors.append(0xeeee00); yellow = ball_colors[-1]
    ball_colors.append(0x0000ee); blue   = ball_colors[-1]
    ball_colors.append(0xee0000); red    = ball_colors[-1]
    ball_colors.append(0xee00ee); purple = ball_colors[-1]
    ball_colors.append(0xee7700); orange = ball_colors[-1]
    ball_colors.append(0x00ee00); green  = ball_colors[-1]
    ball_colors.append(0xbb2244); maroon = ball_colors[-1]
    ball_colors.append(0x111111); black  = ball_colors[-1]
    ball_colors = ball_colors + ball_colors[1:-1]

    num_balls = len(ball_colors)
    ball_radius = ball_diameter / 2
    sphere = SphereBufferGeometry(radius=ball_radius,
                                  widthSegments=16,
                                  heightSegments=12)
    stripeGeom = SphereBufferGeometry(radius=1.012*ball_radius,
                                      widthSegments=16,
                                      heightSegments=8,
                                      thetaStart=np.pi/3,
                                      thetaLength=np.pi/3)

    ball_materials = [MeshPhongMaterial(name='ballMaterial %d' % i,
                                        color=color,
                                        shading=SmoothShading)
                      for i, color in enumerate(ball_colors)]

    ballData = {'cannonData': {'mass': 0.17, 'shapes': ['Sphere'],
                               'linearDamping': 0.25, 'angularDamping': 0.32}}

    y_position = H_table + ball_radius + 0.0001 # epsilon distance which the ball will fall from initial position

    # triangle racked:
    d = 0.04*ball_radius # separation between racked balls
    side_length = 4 * (ball_diameter + d)
    x_positions = np.concatenate([np.linspace(0,                        0.5 * side_length,                         5),
                                  np.linspace(-0.5*(ball_diameter + d), 0.5 * side_length - (ball_diameter + d),   4),
                                  np.linspace(-(ball_diameter + d),     0.5 * side_length - 2*(ball_diameter + d), 3),
                                  np.linspace(-1.5*(ball_diameter + d), 0.5 * side_length - 3*(ball_diameter + d), 2),
                                  np.array([  -2*(ball_diameter + d)])])
    z_positions = np.concatenate([np.linspace(0,                                    np.sqrt(3)/2 * side_length, 5),
                                  np.linspace(0.5*np.sqrt(3) * (ball_diameter + d), np.sqrt(3)/2 * side_length, 4),
                                  np.linspace(np.sqrt(3) * (ball_diameter + d),     np.sqrt(3)/2 * side_length, 3),
                                  np.linspace(1.5*np.sqrt(3) * (ball_diameter + d), np.sqrt(3)/2 * side_length, 2),
                                  np.array([  np.sqrt(3)/2 * side_length])])
    z_positions *= -1
    z_positions -= L_table / 8

    # cue ball at head spot:
    x_positions = [0] + list(x_positions)
    z_positions = [L_table / 4] + list(z_positions)

    for i, material in enumerate(ball_materials[:9] + 7*[ball_materials[0]]):
        ballMesh = Mesh(name="ballMesh %d" % i,
                        geometry=sphere,
                        position=[x_positions[i], y_position, z_positions[i]],
                        material=material,
                        userData=ballData,
                        castShadow=True)
        scene.add(ballMesh)
        if i > 8:
            stripeMesh = Mesh(name="ballStripeMesh %d" % i,
                              material=ball_materials[i-8],
                              geometry=stripeGeom)
            ballMesh.add(stripeMesh)

    return scene
