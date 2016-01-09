import threading
import unittest
import nose

import os.path
import sys
# NEEDLEDIR = os.path.abspath(os.path.join(os.path.split(__file__)[0], 'needle'))
# sys.path.insert(0, NEEDLEDIR)
import needle

THREEPYDIR = os.path.abspath(os.path.join(os.path.split(__file__)[0], os.path.pardir))
sys.path.insert(0, THREEPYDIR)
from pyserver.flask_app import app, render_template, Markup, main, json, request


#from test_flask_app import FlaskAppTest

from test_cannon import CANNONTest
from test_heightfield import HeightfieldTest
from test_skybox import SkyboxTest
from test_text import TextGeometryTest

# from test_main import *

from three import *


@app.route('/test')
def _test_page():
    scene = Scene()
    scene.add(Mesh(geometry=PlaneBufferGeometry(width=8, height=8),
                   material=MeshBasicMaterial(color=0x5555ff),
                   position=[0, -2, -4],
                   rotation=[-np.pi/2, 0, 0],
                   cannonData={'mass': 0, 'shapes': ['Plane']}))
    return render_template('test.html',
                           links=Markup('\n<br>\n'.join([r"<a href='%s'>%s</a>" % (endpoint, endpoint)
                                                         for endpoint in ('test/cannon',
                                                                          'test/heightfield',
                                                                          'test/skybox')])),
                           json_config=Markup(r"""<script>
var THREE_PY_CONFIG = %s;
var JSON_SCENE = %s;
</script>""" % (json.dumps({'controls': request.args.get('controls')}, indent=2),
                json.dumps(scene.export(), indent=2))))


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=(logging.DEBUG if app.debug else logging.INFO),
                        format="%(levelname)s %(name)s %(funcName)s %(lineno)d:  %(message)s")

    app.config['TESTING'] = True
    app.debug = False

    def run_tests():
        nose.runmodule()
        # nose.main(addplugins=[NeedleCapturePlugin, SaveBaselinePlugin])
        # nose.main(addplugins=['needle-capture', 'save-baseline', 'needle-cleanup-on-success'])
        # unittest.main(argv=['run_tests.py'])
        # threading.main_thread().join()

    client_thread = threading.Thread(target=run_tests, name='client')
    # client_thread = threading.Timer(4, run_tests)
    client_thread.start()

    main()
