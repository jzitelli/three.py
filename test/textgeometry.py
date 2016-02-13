import logging
_logger = logging.getLogger(__name__)
import json
from flask import Flask, Blueprint, render_template, Markup
from needle.cases import NeedleTestCase
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.split(__file__)[0], os.path.pardir)))
import site_settings
import pyserver
from three import *
from flask_app import main



blueprint = Blueprint("textgeometry", __name__,
                      static_folder=site_settings.STATIC_FOLDER,
                      static_url_path='',
                      template_folder=site_settings.TEMPLATE_FOLDER)



@blueprint.route('/textgeometry')
def _test_text():
    scene = Scene()
    scene.add(Mesh(geometry=TextGeometry(text='textgeometry',
                                         font_url="node_modules/three/fonts/helvetiker_regular.typeface.js",
                                         size=0.1, height=0),
                   material=MeshBasicMaterial(color=0xff00ff),
                   position=[0, 0, -2]))
    return render_template('index.html',
                           json_config=Markup(r"""<script>
var WebVRConfig = %s;
var THREEPY_SCENE = %s;
</script>""" % (json.dumps(WebVRConfig, indent=2),
                json.dumps(scene.export(), indent=2))))



class TextGeometryTest(NeedleTestCase):
    def test_screenshot(self):
        self.driver.get('127.0.0.1:5000/textgeometry')
        self.assertScreenshot('canvas', 'textgeometry')



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
    app.run(host='0.0.0.0')
