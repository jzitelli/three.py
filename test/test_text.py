import unittest
import json
import numpy as np
from needle.cases import NeedleTestCase

import os.path
import sys
THREEPYDIR = os.path.abspath(os.path.join(os.path.split(__file__)[0], os.path.pardir))
if THREEPYDIR not in sys.path:
    sys.path.insert(0, THREEPYDIR)
from pyserver.flask_app import app, request, Markup, render_template, main
from three import *


@app.route('/test/text')
def test_text():
    scene = Scene()
    scene.add(Mesh(geometry=BoxGeometry(width=1, height=1, depth=1),
                   material=MeshPhongMaterial(color=0xff00ff, shading=FlatShading),
                   position=[4, 10, -40]))
    return render_template('index.html',
                           json_config=Markup(r"""<script>
var THREE_PY_CONFIG = %s;
var JSON_SCENE = %s;
</script>""" % (json.dumps({'controls': request.args.get('controls')}, indent=2),
                json.dumps(scene.export(), indent=2))))


class TextGeometryTest(NeedleTestCase):
    def setUp(self):
        app.debug = True
        app.config['TESTING'] = True
        self.app = app.test_client()
    def test_screenshot(self):
        self.driver.get('/test/text')
        self.assertScreenshot('canvas', 'text_screenshot')


if __name__ == "__main__":
    #unittest.main()
    #app.run(host='0.0.0.0')
    import logging
    logging.basicConfig(level=(logging.DEBUG if app.debug else logging.INFO),
                        format="%(levelname)s %(name)s %(funcName)s %(lineno)d:  %(message)s")
    app.config['TESTING'] = True
    main()
