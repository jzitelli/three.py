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



blueprint = Blueprint('skybox', __name__,
                      static_folder=site_settings.STATIC_FOLDER,
                      static_url_path='',
                      template_folder=site_settings.TEMPLATE_FOLDER)



@blueprint.route('/skybox')
def _test_skybox():
    scene = Scene()
    scene.add(Skybox(cube_images=['../images/%s.png' % side
                                  for side in ('px', 'nx', 'py', 'ny', 'pz', 'nz')]))
    return render_template('index.html',
                           json_config=Markup(r"""<script>
var WebVRConfig = %s;
var THREEPY_SCENE = %s;
</script>""" % (json.dumps(WebVRConfig, indent=2),
                json.dumps(scene.export(), indent=2))))



class SkyboxTest(NeedleTestCase):
    def test_screenshot(self):
        self.driver.get('127.0.0.1:5000/skybox')
        self.assertScreenshot('canvas', 'skybox')



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
