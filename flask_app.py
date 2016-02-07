import logging
_logger = logging.getLogger(__name__)

import json

from flask import Flask, render_template, Markup

import site_settings

import pyserver

from three import *



app = Flask(__name__,
            static_folder=site_settings.STATIC_FOLDER,
            static_url_path='',
            template_folder=site_settings.TEMPLATE_FOLDER)
app.debug = site_settings.DEBUG
app.register_blueprint(pyserver.blueprint)



def index_scene():
    scene = Scene()
    scene.add(PointLight(color=0xffffff, intensity=1, distance=100, position=[-4, 5, 20]))
    boxMesh = Mesh(geometry=BoxGeometry(width=1, height=1, depth=1),
                   material=MeshPhongMaterial(color=0xff0000, shading=FlatShading),
                   position=[1, 0, -4])
    scene.add(boxMesh)
    sphereMesh = Mesh(geometry=SphereBufferGeometry(radius=0.5, widthSegments=11, heightSegments=9),
                      material=MeshLambertMaterial(color=0x00ff00),
                      position=[0, 1, -4])
    scene.add(sphereMesh)
    textGeomMesh = Mesh(geometry=TextGeometry(text='three.py', font='helvetiker', size=0.25, height=0.25/16),
                        material=MeshBasicMaterial(color=0x0000ff),
                        position=[-1, 0, -4])
    scene.add(textGeomMesh)
    return scene



@app.route('/')
def index():
    scene = index_scene()
    return render_template('index.html',
                           json_config=Markup("""<script>
var JSON_SCENE = %s;
</script>""" % json.dumps(scene.export(), indent=2)))



def main():
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



if __name__ == "__main__":
    logging.basicConfig(level=(logging.DEBUG if app.debug else logging.INFO),
                        format="%(levelname)s %(name)s %(funcName)s %(lineno)d:  %(message)s")
    main()
