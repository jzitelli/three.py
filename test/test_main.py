import unittest
from needle.cases import NeedleTestCase
import sys
import os.path
sys.path.append(os.path.join(os.path.split(__file__)[0], os.path.pardir))
from pyserver.flask_app import app


class MainTest(NeedleTestCase):
    def setUp(self):
        app.debug = True
        app.config['TESTING'] = True
        self.app = app.test_client()
    def test_screenshot(self):
        self.driver.get('/')
        self.assertScreenshot('canvas', 'screenshot')


if __name__ == "__main__":
    unittest.main()
