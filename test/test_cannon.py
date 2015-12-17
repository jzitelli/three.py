import unittest
import json
import numpy as np
from needle.cases import NeedleTestCase

import os.path
import sys
sys.path.append(os.path.join(os.path.split(__file__)[0], os.path.pardir))

from three import *


with open(os.path.join(os.path.split(__file__)[0], 'test.html')) as f:
    test_html_string = f.read()


def test_cannon():
    scene = Scene()
    scene.add(Mesh(geometry=SphereBufferGeometry(radius=0.25),
                   material=MeshBasicMaterial(color=0xff0000),
                   cannonData={'mass': 1, 'shapes': ['Sphere']},
                   position=[0, 2, -4]))
    scene.add(Mesh(geometry=BoxGeometry(width=1, height=1, depth=1),
                   material=MeshBasicMaterial(color=0x00ff00),
                   cannonData={'mass': 1, 'shapes': ['Box']},
                   position=[-2, 3, -4]))
    scene.add(Mesh(geometry=CylinderGeometry(radiusTop=0.5, radiusBottom=0.5, height=1, radialSegments=8),
                   material=MeshBasicMaterial(color=0x0000ff),
                   position=[2, 4, -6],
                   cannonData={'mass': 1, 'shapes': ['Cylinder']}))
    scene.add(Mesh(geometry=PlaneBufferGeometry(width=8, height=8),
                   material=MeshBasicMaterial(color=0x5555ff),
                   position=[0, -2, -4],
                   rotation=[-np.pi/2, 0, 0],
                   cannonData={'mass': 0, 'shapes': ['Plane']}))
    # TODO:
    # scene.add(Mesh(geometry=HeightfieldBufferGeometry(image=url_prefix+"images/terrain128.png",
    #                                                   height=4),
    #                material=MeshLambertMaterial(color=0x118822),
    #                rotation=[-np.pi/2, 0, 0],
    #                cannonData={'mass': 0, 'shapes': ['Heightfield']}))
    return render_template_string(test_html_string,
                                  json_config=Markup(r"""<script>
var THREE_PY_CONFIG = %s;
var JSON_SCENE = %s;
</script>""" % (json.dumps({'controls': request.args.get('controls')}, indent=2),
                json.dumps(scene.export(), indent=2))))


import pyserver
from pyserver.flask_app import Markup, render_template_string, app as flask_app, request


class CANNONTest(NeedleTestCase):
    def setUp(self):
        flask_app.debug = True
        flask_app.config['TESTING'] = True
        self.app = flask_app.test_client()
    def test_screenshot(self):
        self.driver.get('127.0.0.1:5000/test/cannon')
        self.assertScreenshot('canvas', 'cannon_screenshot')


if __name__ == "__main__":
    unittest.main()
