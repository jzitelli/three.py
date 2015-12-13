import unittest

from needle.cases import NeedleTestCase

import sys
import os
sys.path.append(os.path.join(os.path.split(__file__)[0], os.path.pardir))
import pyserver
from pyserver.flask_app import app as flask_app


class MainTest(NeedleTestCase):
    def setUp(self):
        flask_app.debug = True
        flask_app.config['TESTING'] = True
        self.app = flask_app.test_client()
    def test_screenshot(self):
        self.driver.get('127.0.0.1:5000')
        self.assertScreenshot('canvas', 'screenshot')


if __name__ == "__main__":
    unittest.main()
