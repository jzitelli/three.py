import logging
import os.path
import json
import sys
import threading
import nose
from needle.cases import NeedleTestCase
import nose
from nose.plugins.plugintest import run_buffered

from flask import Flask, render_template, Markup

sys.path.insert(0, os.path.abspath(os.path.join(os.path.split(__file__)[0], os.path.pardir)))

from three import *

WebVRConfig = {
    #### webvr-polyfill configuration
    # "FORCE_ENABLE_VR":       True,
    "K_FILTER":              0.98,
    "PREDICTION_TIME_S":     0.020,
    #"TOUCH_PANNER_DISABLED": True,
    #"YAW_ONLY":              True,
    #"MOUSE_KEYBOARD_CONTROLS_DISABLED": True,
    "KEYBOARD_CONTROLS_DISABLED": True
}

DEBUG           = True
PORT            = 5000
STATIC_FOLDER   = os.path.abspath(os.path.join(os.path.split(__file__)[0], os.path.pardir))
TEMPLATE_FOLDER = os.path.abspath(os.path.split(__file__)[0])

test_hrefs = {name: href
              for name, href in [(name, '/%s' % name)
                                 for name in ['layers',
                                              'heightfield',
                                              'cannon',
                                              'pool_table',
                                              'skybox',
                                              'textgeometry']]}

def get_overlay_content():
    return Markup(" <hr> ".join([r"<a href='/'>HOME</a>",
                                 " <br> ".join(['<a href="%s">%s</a>' % (href, name)
                                                for name, href in test_hrefs.items()])]))

import cannon
import heightfield
import layers
import skybox
import textgeometry
import pool_table



app = Flask(__name__,
            static_folder=STATIC_FOLDER,
            static_url_path='',
            template_folder=TEMPLATE_FOLDER)
app.debug = DEBUG
app.testing = True



@app.route('/')
def main_page():
    scene = Scene()
    scene.add(PointLight(color=0xffffff, intensity=1, distance=100, position=[-4, 5, 20]))
    boxMesh = Mesh(geometry=BoxGeometry(width=1, height=1, depth=1),
                   material=MeshPhongMaterial(color=0xff0000, shading=FlatShading),
                   position=[1, 1.5, -3])
    scene.add(boxMesh)
    sphereMesh = Mesh(geometry=SphereBufferGeometry(radius=0.5, widthSegments=11, heightSegments=9),
                      material=MeshLambertMaterial(color=0x00ff00),
                      position=[0, 2.5, -3])
    scene.add(sphereMesh)
    textGeomMesh = Mesh(geometry=TextGeometry(text='three.py',
                                              font_url='node_modules/three/examples/fonts/helvetiker_regular.typeface.js',
                                              size=0.25, height=0.25/16),
                        material=MeshBasicMaterial(color=0x0000ff),
                        position=[-1, 1.5, -3])
    scene.add(textGeomMesh)
    return render_template('template.html',
                           json_config=Markup("""<script>
var WebVRConfig = %s;
var THREEPY_SCENE = %s;
</script>""" % (json.dumps(WebVRConfig, indent=2), json.dumps(scene.export()))),
                           overlay_content=get_overlay_content())



def main():
    app.register_blueprint(cannon.blueprint)
    app.register_blueprint(heightfield.blueprint)
    app.register_blueprint(layers.blueprint)
    app.register_blueprint(skybox.blueprint)
    app.register_blueprint(textgeometry.blueprint)
    app.register_blueprint(pool_table.blueprint)
    _logger = logging.getLogger(threading.current_thread().name);
    _logger.info("app.config:\n%s" % '\n'.join(['%s: %s' % (k, str(v))
                                                for k, v in sorted(app.config.items(),
                                                                   key=lambda i: i[0])]))
    _logger.info(r"""
            ------
        T H R E E . PY
   **************************
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
STARTING FLASK APP!!!!!!!!!!!!!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  **************************
        T H R E E . PY
            ------
""")
    app.run(host='0.0.0.0')

    # argv = [__file__, '-v', '-v', '-v', '--logging-level=DEBUG', '--with-needle-capture', '--with-needle-cleanup-on-success', '--with-save-baseline', __file__]
    # thread = threading.Thread(target=run_buffered, kwargs={'argv': argv})
    # _logger.debug("starting daemon thread...")
    # thread.start()



# class CANNONTest(NeedleTestCase):
#     def setUp(self):
#         self.app = app.test_client()
#     def test_screenshot(self):
#         #self.driver.get('http://127.0.0.1:5000/cannon')
#         self.app.get('/cannon')
#         self.assertScreenshot('canvas', 'cannon')



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format="%(levelname)s %(name)s %(funcName)s %(lineno)d:  %(message)s")
    _logger = logging.getLogger(__name__)
    main()

    #nose.run(argv=argv)
