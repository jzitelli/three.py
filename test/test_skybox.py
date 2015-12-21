import unittest
import json
import numpy as np
from needle.cases import NeedleTestCase

import os.path
import sys
sys.path.append(os.path.join(os.path.split(__file__)[0], os.path.pardir))

from pyserver.flask_app import app, request, Markup, render_template, main
from three import *


@app.route('/test/skybox')
def test_skybox():
    scene = Scene()
    scene.add(Skybox(cube_images=['../images/%s.png' % side
                                  for side in ('px', 'nx', 'py', 'ny', 'pz', 'nz')]))
    return render_template('index.html',
                           json_config=Markup(r"""<script>
var THREE_PY_CONFIG = %s;
var JSON_SCENE = %s;
</script>""" % (json.dumps({'controls': request.args.get('controls')}, indent=2),
                json.dumps(scene.export(), indent=2))))


class SkyboxTest(NeedleTestCase):
    def setUp(self):
        app.debug = True
        app.config['TESTING'] = True
        self.app = flask_app.test_client()
    def test_screenshot(self):
        self.driver.get('/test/skybox')
        self.assertScreenshot('canvas', 'skybox_screenshot')


if __name__ == "__main__":
    #unittest.main()
    #app.run(host='0.0.0.0')
    import logging
    logging.basicConfig(level=(logging.DEBUG if app.debug else logging.INFO),
                        format="%(levelname)s %(name)s %(funcName)s %(lineno)d:  %(message)s")
    app.config['TESTING'] = True
    main()