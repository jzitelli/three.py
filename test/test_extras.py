import unittest

from needle.cases import NeedleTestCase

import sys
import os
sys.path.append(os.path.join(os.getcwd(), os.path.pardir))
from pyserver.flask_app import request, render_template, main, app as flask_app


@flask_app.route('test/extras'):
def text_extras():
    pass


class TextGeomObject3DTest(NeedleTestCase):
    def setUp(self):
        flask_app.debug = True
        flask_app.config['TESTING'] = True
        self.app = flask_app.test_client()
    def test_screenshot(self):
        self.driver.get('test/extras')
        self.assertScreenshot('canvas', 'screenshot')
    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
