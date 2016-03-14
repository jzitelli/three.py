import logging
import json
import os.path
import sys

from flask import Flask, render_template, Markup, request

sys.path.insert(0, os.path.abspath(os.path.join(os.path.split(__file__)[0], os.path.pardir)))

from three import *

WebVRConfig = {
    #"FORCE_ENABLE_VR":            True,
    "K_FILTER":                   0.98,
    "PREDICTION_TIME_S":          0.020,
    "KEYBOARD_CONTROLS_DISABLED": True
}

DEBUG           = True
PORT            = 5000
STATIC_FOLDER   = os.path.abspath(os.path.join(os.path.split(__file__)[0], os.path.pardir))
TEMPLATE_FOLDER = os.path.abspath(os.path.split(__file__)[0])

def get_test_link_table():
    return Markup(r"""<table>
{trs}
</table>""".format(trs='\n'.join(["<tr>{tds}</tr>".format(tds="<td><a class=button href='{1}'>{0}</a></td> <td><a class=button href='{2}'>(with desk)</a></td>".format(name, href, href+'?model=test/models/vrDesk.json'))
                                  for name, href in [(test, TEST_HREFS[test]) for test in TESTS]])))

def get_overlay_content():
    return Markup(r"""
<h2>Tests:</h2>
""") + get_test_link_table()

import layers
import heightfield
import cannon
import pool_table
import skybox
import textgeometry
import points
import aframe

TESTS = ['layers',
         'heightfield',
         'cannon',
         'pool_table',
         'skybox',
         'textgeometry',
         'points',
         'aframe']

TEST_HREFS = {name: href
              for name, href in [(name, '/%s' % name) for name in TESTS]}

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
    _logger = logging.getLogger(__name__);
    app.register_blueprint(cannon.blueprint)
    app.register_blueprint(heightfield.blueprint)
    app.register_blueprint(layers.blueprint)
    app.register_blueprint(skybox.blueprint)
    app.register_blueprint(textgeometry.blueprint)
    app.register_blueprint(pool_table.blueprint)
    app.register_blueprint(points.blueprint)
    app.register_blueprint(aframe.blueprint)
    _logger.debug("app.config:\n%s" % '\n'.join(['%s: %s' % (k, str(v))
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
    _logger.info("\nTESTS:\n\n%s" % '\n'.join(TESTS))
    app.run(host='0.0.0.0')



if __name__ == "__main__":
    logging.basicConfig(level=(logging.DEBUG if ('-v' in sys.argv and app.debug) else logging.INFO),
                        format="%(levelname)s %(name)s %(funcName)s %(lineno)d:  %(message)s")
    main()
