import unittest

from needle.cases import NeedleTestCase

import sys
import os
sys.path.append(os.path.join(os.getcwd(), os.path.pardir))
from pyserver.flask_app import request, render_template, main, app as flask_app
from Flask import render_template_string


class TextGeomObject3DTest(NeedleTestCase):
    def setUp(self):
        flask_app.debug = True
        flask_app.config['TESTING'] = True
        self.app = flask_app.test_client()
    def test_screenshot(self):
        self.driver.get('127.0.0.1:5000/test/extras')
        self.assertScreenshot('canvas', 'screenshot')


@flask_app.route('/test/extras')
def text_extras():
    return render_template_string(r"""
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">

    <meta name="viewport" content="width=device-width, user-scalable=no, minimum-scale=1.0, maximum-scale=1.0">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />

    <link rel="shortcut icon" href="../favicon.ico">

    <title>three.py test_extras</title>

    <style>
      body {
        margin: 0;
        overflow: hidden;
      }
      canvas {
        width: 100%;
        height: 100%;
      }
    </style>

<!-- *** begin json_config *** -->
{{ json_config if json_config else '' }}
<!-- *** end json_config *** -->
  </head>


  <body onload="onLoad()">

    <script src="{{ threejs_lib if threejs_lib else '../lib/three-r73.js' }}"></script>

    <script src="../lib/TextGeometry.js"></script>
    <script src="../lib/FontUtils.js"></script>

    <script src="../fonts/Anonymous Pro_Regular.js"></script>
    <script src="../fonts/helvetiker_regular.typeface.js"></script>

    <script src="../lib/cannon.js"></script>

    <script src="../js/pyserver.js"></script>
    <script src="../js/three.py.js"></script>
    <script src="../js/threeExtract.js"></script>

    <script src="../js/main.js"></script>

  </body>

</html>
""", json_config=Markup(r"""<script>
var JSON_SCENE = %s;
</script>""" % json.dumps(scene.export())))


if __name__ == "__main__":
    unittest.main()
