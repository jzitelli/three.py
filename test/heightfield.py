import logging
import json

from flask import Blueprint, Flask, Markup, render_template

from needle.cases import NeedleTestCase

import os.path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.split(__file__)[0], os.path.pardir)))

from flask_app import DEBUG, STATIC_FOLDER, TEMPLATE_FOLDER, WebVRConfig

from three import *



blueprint = Blueprint('heightfield', __name__,
                      static_folder=STATIC_FOLDER,
                      static_url_path='',
                      template_folder=TEMPLATE_FOLDER)



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
    return render_template('index.html',
                           json_config=Markup(r"""<script>
var WebVRConfig = %s;
var THREEPY_SCENE = %s;
</script>""" % (json.dumps(WebVRConfig, indent=2),
                json.dumps(scene.export(), indent=2))))



class HeightfieldTest(NeedleTestCase):
    def test_screenshot(self):
        self.driver.get('127.0.0.1:5000/heightfield')
        self.assertScreenshot('canvas', 'heightfield')



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
    app.run('0.0.0.0')
