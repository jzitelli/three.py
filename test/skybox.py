import logging
import json

from flask import Blueprint, Flask, Markup, render_template

from needle.cases import NeedleTestCase

from flask_app import STATIC_FOLDER, TEMPLATE_FOLDER, WebVRConfig

from three import *



blueprint = Blueprint('skybox', __name__,
                      static_folder=STATIC_FOLDER,
                      static_url_path='',
                      template_folder=TEMPLATE_FOLDER)



@blueprint.route('/skybox')
def skybox():
    scene = Scene()
    scene.add(Skybox(cube_images=['test/images/%s.png' % side
                                  for side in ('px', 'nx', 'py', 'ny', 'pz', 'nz')]))
    return render_template('template.html',
                           json_config=Markup(r"""<script>
var WebVRConfig = %s;
var THREEPY_SCENE = %s;
</script>""" % (json.dumps(WebVRConfig, indent=2),
                json.dumps(scene.export(), indent=2))))



class SkyboxTest(NeedleTestCase):
    def test_screenshot(self):
        self.driver.get('127.0.0.1:5000/skybox')
        self.assertScreenshot('canvas', 'skybox')
