import unittest
import json
import numpy as np
from needle.cases import NeedleTestCase

import os.path
import sys
sys.path.append(os.path.join(os.path.split(__file__)[0], os.path.pardir))

from pyserver.flask_app import app, request, Markup, render_template, main
from three import *


@app.route('/test/cannon')
def test_cannon():
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
var THREE_PY_CONFIG = %s;
var JSON_SCENE = %s;
</script>""" % (json.dumps({'controls': request.args.get('controls')}, indent=2),
                json.dumps(scene.export(), indent=2))))


class CANNONTest(NeedleTestCase):
    def setUp(self):
        app.debug = True
        app.config['TESTING'] = True
        self.app = app.test_client()
    def test_screenshot(self):
        self.driver.get('/test/cannon')
        self.assertScreenshot('canvas', 'cannon_screenshot')


if __name__ == "__main__":
    #unittest.main()
    #app.run(host='0.0.0.0')
    import logging
    logging.basicConfig(level=(logging.DEBUG if app.debug else logging.INFO),
                        format="%(levelname)s %(name)s %(funcName)s %(lineno)d:  %(message)s")
    app.config['TESTING'] = True
    main()
