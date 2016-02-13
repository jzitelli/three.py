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



blueprint = Blueprint('layers', __name__,
                      static_folder=site_settings.STATIC_FOLDER,
                      static_url_path='',
                      template_folder=site_settings.TEMPLATE_FOLDER)



@blueprint.route('/layers')
def _test_layers():
    scene = Scene()
    scene.add(Mesh(geometry=TextGeometry(text='LAYER 1',
                                         font_url='node_modules/three/examples/fonts/helvetiker_regular.typeface.js',
                                         size=0.14, height=0),
                   material=MeshBasicMaterial(color=0xff0000),
                   position=[-2, 0, -3],
                   layers=[1]))
    scene.add(Mesh(geometry=TextGeometry(text='LAYER 2',
                                         font_url='node_modules/three/examples/fonts/helvetiker_regular.typeface.js',
                                         size=0.14, height=0),
                   material=MeshBasicMaterial(color=0x0000ff),
                   position=[1.6, 0, -3],
                   layers=[2]))
    return render_template('index.html',
                           json_config=Markup(r"""<script>
var WebVRConfig = %s;
var THREEPY_SCENE = %s;
</script>""" % (json.dumps(WebVRConfig, indent=2),
                json.dumps(scene.export(), indent=2))))



class LayersTest(NeedleTestCase):
    def test_screenshot(self):
        self.driver.get('127.0.0.1:5000/layers')
        self.assertScreenshot('canvas', 'layers')



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
