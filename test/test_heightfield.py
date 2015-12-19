import unittest
import json
import numpy as np
from needle.cases import NeedleTestCase

import os.path
import sys
sys.path.append(os.path.join(os.path.split(__file__)[0], os.path.pardir))

from pyserver.flask_app import app, request, Markup, render_template
from three import *


@app.route('/test/heightfield')
def test_heightfield():
    scene = Scene()
    scene.add(PointLight(color=0xffffff, intensity=1, distance=800,
                         position=[10, 0, 0]))
    heightfieldImage = Image(url='../images/terrain128.png')
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
var THREE_PY_CONFIG = %s;
var JSON_SCENE = %s;
</script>""" % (json.dumps({'controls': request.args.get('controls')}, indent=2),
                json.dumps(scene.export(), indent=2))))


class HeightfieldTest(NeedleTestCase):
    def setUp(self):
        app.debug = True
        app.config['TESTING'] = True
        self.app = flask_app.test_client()
    def test_screenshot(self):
        self.driver.get('/test/heightfield')
        self.assertScreenshot('canvas', 'heightfield_screenshot')


if __name__ == "__main__":
    #unittest.main()
    app.run(host='0.0.0.0')
