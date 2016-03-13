import logging
import json

from flask import Blueprint, Markup, render_template

from needle.cases import NeedleTestCase

from flask_app import WebVRConfig

from three import *



blueprint = Blueprint(__name__, __name__)



@blueprint.route('/%s' % __name__)
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
