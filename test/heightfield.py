import logging
import json

from flask import Blueprint, Markup, render_template

from needle.cases import NeedleTestCase

from flask_app import WebVRConfig

from three import *



blueprint = Blueprint('heightfield', __name__)



@blueprint.route('/heightfield')
def heightfield():
    scene = Scene()
    scene.add(PointLight(color=0xffffff, intensity=1, distance=800,
                         position=[10, 0, 0]))
    heightfieldImage = Image(url='images/terrain128.png')
    scene.add(HeightfieldMesh(heightfieldImage=heightfieldImage,
                              heightfieldScale=32,
                              material=MeshLambertMaterial(color=0xff0000),
                              rotation=[-0.33*np.pi, 0, 0],
                              position=[0, -20, -32],
                              cannonData={'mass': 0, 'shapes': ['Heightfield']}))
    scene.add(Mesh(geometry=SphereBufferGeometry(radius=1),
                   material=MeshPhongMaterial(color=0xffff00, shading=FlatShading),
                   position=[0, 10, -45],
                   cannonData={'mass': 1, 'shapes': ['Sphere']}))
    scene.add(Mesh(geometry=BoxGeometry(width=1, height=1, depth=1),
                   material=MeshPhongMaterial(color=0xff00ff, shading=FlatShading),
                   position=[4, 10, -45],
                   cannonData={'mass': 1, 'shapes': ['Box']}))
    return render_template('template.html',
                           json_config=Markup(r"""<script>
var WebVRConfig = %s;
var THREEPY_SCENE = %s;
</script>""" % (json.dumps(WebVRConfig, indent=2),
                json.dumps(scene.export(url_prefix="test/"), indent=2))))



class HeightfieldTest(NeedleTestCase):
    def test_screenshot(self):
        self.driver.get('127.0.0.1:5000/heightfield')
        self.assertScreenshot('canvas', 'heightfield')
