import logging
import json

from flask import Flask, Blueprint, render_template, Markup

from needle.cases import NeedleTestCase

import os.path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.split(__file__)[0], os.path.pardir)))

from flask_app import DEBUG, STATIC_FOLDER, TEMPLATE_FOLDER, WebVRConfig

from three import *



blueprint = Blueprint("textgeometry", __name__,
                      static_folder=STATIC_FOLDER,
                      static_url_path='',
                      template_folder=TEMPLATE_FOLDER)



@blueprint.route('/textgeometry')
def textgeometry():
    scene = Scene()
    scene.add(DirectionalLight(color=0xffffff, intensity=1, position=(-2,1,1)))
    scene.add(Mesh(geometry=TextGeometry(text='textgeometry',
                                         font_url="node_modules/three/examples/fonts/helvetiker_regular.typeface.js",
                                         size=0.3, height=0.02),
                   material=MeshLambertMaterial(color=0xff00ff),
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
    app = Flask(__name__,
                static_folder=STATIC_FOLDER,
                static_url_path='',
                template_folder=TEMPLATE_FOLDER)
    app.debug = DEBUG
    app.testing = True
    app.register_blueprint(blueprint)
    logging.basicConfig(level=(logging.DEBUG if app.debug else logging.INFO),
                        format="%(levelname)s %(name)s %(funcName)s %(lineno)d:  %(message)s")
    app.run(host='0.0.0.0')
