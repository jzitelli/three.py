import unittest
import json
from needle.cases import NeedleTestCase
import numpy as np

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
    return render_template_string(r"""
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">

    <meta name="viewport" content="width=device-width, user-scalable=no, minimum-scale=1.0, maximum-scale=1.0">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />

    <link rel="shortcut icon" href="../favicon.ico">

    <title>three.py test_cannon</title>

    <style>
      body {
        margin: 0;
        overflow: hidden;
      }
      canvas {
        width: 100%;
        height: 100%;
      }
    </style>

<!-- *** begin json_config *** -->
{{ json_config if json_config else '' }}
<!-- *** end json_config *** -->
  </head>


  <body onload="onLoad()">

    <script src="{{ threejs_lib if threejs_lib else '../lib/three-r73.js' }}"></script>

    <script src="../lib/TextGeometry.js"></script>
    <script src="../lib/FontUtils.js"></script>

    <script src="../fonts/Anonymous Pro_Regular.js"></script>
    <script src="../fonts/helvetiker_regular.typeface.js"></script>

    <script src="../lib/cannon.js"></script>
    <script src="../lib/cannon.serialize.js"></script>

    <script src="../js/pyserver.js"></script>
    <script src="../js/three.py.js"></script>

    <script src="../js/main.js"></script>

  </body>

</html>
""", json_config=Markup(r"""<script>
var JSON_SCENE = %s;
</script>""" % json.dumps(scene.export())))


import os
import sys
sys.path.append(os.path.join(os.path.split(__file__)[0], os.path.pardir))
import pyserver
from pyserver.flask_app import Markup, render_template_string, app as flask_app
from pyserver import three
from three import *


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
