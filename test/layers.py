import logging
import json

from flask import Blueprint, Flask, Markup, render_template

from needle.cases import NeedleTestCase

from flask_app import STATIC_FOLDER, TEMPLATE_FOLDER, WebVRConfig

from three import *



blueprint = Blueprint('layers', __name__,
                      static_folder=STATIC_FOLDER,
                      static_url_path='',
                      template_folder=TEMPLATE_FOLDER)



@blueprint.route('/layers')
def layers():
    scene = Scene()
    scene.add(Mesh(geometry=TextGeometry(text='LAYER 1',
                                         font_url='node_modules/three/examples/fonts/helvetiker_regular.typeface.js',
                                         size=0.14, height=0),
                   material=MeshBasicMaterial(color=0xff0000),
                   position=[-2, 0, -3],
                   layers=[1]))
    scene.add(Mesh(geometry=TextGeometry(text='LAYER 2',
                                         font_url='node_modules/three/examples/fonts/helvetiker_regular.typeface.js',
                                         size=0.14, height=0),
                   material=MeshBasicMaterial(color=0x0000ff),
                   position=[1.6, 0, -3],
                   layers=[2]))
    return render_template('template.html',
                           json_config=Markup(r"""<script>
var WebVRConfig = %s;
var THREEPY_SCENE = %s;
</script>""" % (json.dumps(WebVRConfig, indent=2),
                json.dumps(scene.export(), indent=2))))



class LayersTest(NeedleTestCase):
    def test_screenshot(self):
        self.driver.get('127.0.0.1:5000/layers')
        self.assertScreenshot('canvas', 'layers')
