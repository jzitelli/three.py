import logging
import json

from flask import Blueprint, Markup, render_template

from needle.cases import NeedleTestCase

from flask_app import WebVRConfig

from three import *



blueprint = Blueprint('cannon', __name__)



@blueprint.route('/cannon')
def cannon():
    scene = Scene()
    scene.add(PointLight(color=0xffffff, intensity=1, distance=100,
                         position=[-2, 20, 4]))
    scene.add(Mesh(geometry=SphereBufferGeometry(radius=0.25),
                   material=MeshPhongMaterial(color=0xff0000, shading=FlatShading),
                   cannonData={'mass': 1, 'shapes': ['Sphere']},
                   position=[0, 4, -4]))
    scene.add(Mesh(geometry=BoxBufferGeometry(width=1, height=1, depth=1),
                   material=MeshPhongMaterial(color=0x00ff00, shading=FlatShading),
                   cannonData={'mass': 1, 'shapes': ['Box']},
                   position=[-2, 4, -4]))
    scene.add(Mesh(geometry=CylinderGeometry(radiusTop=0.5, radiusBottom=0.5, height=1, radialSegments=8),
                   material=MeshPhongMaterial(color=0x0000ff, shading=FlatShading),
                   position=[2, 8, -6],
                   cannonData={'mass': 1, 'shapes': ['Cylinder']}))
    scene.add(Mesh(geometry=PlaneBufferGeometry(width=8, height=8),
                   material=MeshBasicMaterial(color=0x5555ff),
                   position=[0, -1, -4],
                   rotation=[-np.pi/2, 0, 0],
                   cannonData={'mass': 0, 'shapes': ['Plane']}))
    return render_template('template.html',
                           json_config=Markup(r"""<script>
var WebVRConfig = %s;
var THREEPY_SCENE = %s;
</script>""" % (json.dumps(WebVRConfig, indent=2),
                json.dumps(scene.export(), indent=2))))



class CANNONTest(NeedleTestCase):
    def test_screenshot(self):
        self.driver.get('127.0.0.1:5000/cannon')
        self.assertScreenshot('canvas', 'cannon')
