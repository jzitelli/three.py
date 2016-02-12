import json
from needle.cases import NeedleTestCase
from flask import Blueprint, Flask, Markup, render_template
import os.path
import sys
THREEPYDIR = os.path.abspath(os.path.join(os.path.split(__file__)[0], os.path.pardir))
if THREEPYDIR not in sys.path:
    sys.path.insert(0, THREEPYDIR)
import pyserver
import site_settings
from flask_app import WebVRConfig
from three import *



blueprint = Blueprint('/test_layers', __name__,
                      static_folder=site_settings.STATIC_FOLDER,
                      static_url_path='',
                      template_folder=site_settings.TEMPLATE_FOLDER)



@blueprint.route('/test_heightfield')
def _test_heightfield():
    scene = Scene()
    scene.add(PointLight(color=0xffffff, intensity=1, distance=800,
                         position=[10, 0, 0]))
    heightfieldImage = Image(url='images/terrain128.png')
    scene.add(HeightfieldMesh(heightfieldImage=heightfieldImage,
                              heightfieldScale=32,
                              material=MeshLambertMaterial(color=0xff0000),
                              rotation=[-np.pi/4, 0, 0],
                              position=[0, -24, -32],
                              cannonData={'mass': 0, 'shapes': ['Heightfield']}))
    scene.add(Mesh(geometry=SphereBufferGeometry(radius=1),
                   material=MeshPhongMaterial(color=0xffff00, shading=FlatShading),
                   position=[0, 10, -40],
                   cannonData={'mass': 1, 'shapes': ['Sphere']}))
    scene.add(Mesh(geometry=BoxGeometry(width=1, height=1, depth=1),
                   material=MeshPhongMaterial(color=0xff00ff, shading=FlatShading),
                   position=[4, 10, -40],
                   cannonData={'mass': 1, 'shapes': ['Box']}))
    return render_template('index.html',
                           json_config=Markup(r"""<script>
var WebVRConfig = %s;
var THREEPY_SCENE = %s;
</script>""" % (json.dumps(WebVRConfig, indent=2),
                json.dumps(scene.export(), indent=2))))



class HeightfieldTest(NeedleTestCase):
    def test_screenshot(self):
        self.driver.get('127.0.0.1:5000/test_heightfield')
        self.assertScreenshot('canvas', 'test_heightfield')



if __name__ == "__main__":
    import logging
    app = Flask(__name__,
                static_folder=site_settings.STATIC_FOLDER,
                static_url_path='',
                template_folder=site_settings.TEMPLATE_FOLDER)
    app.debug = site_settings.DEBUG
    app.testing = True
    app.register_blueprint(pyserver.blueprint)
    app.register_blueprint(blueprint)
    logging.basicConfig(level=(logging.DEBUG if app.debug else logging.INFO),
                        format="%(levelname)s %(name)s %(funcName)s %(lineno)d:  %(message)s")
    app.run('0.0.0.0')
