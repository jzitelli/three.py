import logging
import json

from flask import Blueprint, Flask, Markup, render_template

from needle.cases import NeedleTestCase

import os.path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.split(__file__)[0], os.path.pardir)))

from flask_app import DEBUG, STATIC_FOLDER, TEMPLATE_FOLDER, WebVRConfig

from three import *



blueprint = Blueprint('skybox', __name__,
                      static_folder=STATIC_FOLDER,
                      static_url_path='',
                      template_folder=TEMPLATE_FOLDER)



@blueprint.route('/cannon')
def cannon():
    scene = Scene()
    scene.add(PointLight(color=0xffffff, intensity=1, distance=100,
                         position=[-2, 20, 4]))
    scene.add(Mesh(geometry=SphereBufferGeometry(radius=0.25),
                   material=MeshPhongMaterial(color=0xff0000, shading=FlatShading),
                   cannonData={'mass': 1, 'shapes': ['Sphere']},
                   position=[0, 2, -4]))
    scene.add(Mesh(geometry=BoxGeometry(width=1, height=1, depth=1),
                   material=MeshPhongMaterial(color=0x00ff00, shading=FlatShading),
                   cannonData={'mass': 1, 'shapes': ['Box']},
                   position=[-2, 3, -4]))
    scene.add(Mesh(geometry=CylinderGeometry(radiusTop=0.5, radiusBottom=0.5, height=1, radialSegments=8),
                   material=MeshPhongMaterial(color=0x0000ff, shading=FlatShading),
                   position=[2, 4, -6],
                   cannonData={'mass': 1, 'shapes': ['Cylinder']}))
    scene.add(Mesh(geometry=PlaneBufferGeometry(width=8, height=8),
                   material=MeshBasicMaterial(color=0x5555ff),
                   position=[0, -2, -4],
                   rotation=[-np.pi/2, 0, 0],
                   cannonData={'mass': 0, 'shapes': ['Plane']}))
    return render_template('index.html',
                           json_config=Markup(r"""<script>
var WebVRConfig = %s;
var THREEPY_SCENE = %s;
</script>""" % (json.dumps(WebVRConfig, indent=2),
                json.dumps(scene.export(), indent=2))))



class CANNONTest(NeedleTestCase):
    def test_screenshot(self):
        self.driver.get('127.0.0.1:5000/cannon')
        self.assertScreenshot('canvas', 'cannon')



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
