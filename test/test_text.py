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
def _test_text():
    scene = Scene()
    scene.add(Mesh(geometry=TextGeometry(text='test text', size=0.1, height=0),
                   material=MeshBasicMaterial(color=0xff00ff),
                   position=[0, 0, -4]))
    return render_template('index.html',
                           json_config=Markup(r"""<script>
var THREE_PY_CONFIG = %s;
var JSON_SCENE = %s;
</script>""" % (json.dumps({'controls': request.args.get('controls')}, indent=2),
                json.dumps(scene.export(), indent=2))))


class TextGeometryTest(NeedleTestCase):
    def test_screenshot(self):
        self.driver.get('127.0.0.1:5000/test/text')
        self.assertScreenshot('canvas', 'text_screenshot')


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=(logging.DEBUG if app.debug else logging.INFO),
                        format="%(levelname)s %(name)s %(funcName)s %(lineno)d:  %(message)s")
    app.config['TESTING'] = True
    main()
