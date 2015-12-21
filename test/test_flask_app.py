"""See http://flask.pocoo.org/docs/0.10/testing/
"""
import unittest

import os.path
import sys
THREEPYDIR = os.path.abspath(os.path.join(os.path.split(__file__)[0], os.path.pardir))
if THREEPYDIR not in sys.path:
    sys.path.insert(0, THREEPYDIR)
from pyserver.flask_app import app


class FlaskAppTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_index(self):
        response = self.app.get('/')
        print(response)
        assert(response)

    def test_log(self):
        response = self.app.post('/log', data={'msg': 'testing 1 w23 gaemah'})
        print(response)
        assert(response)


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=(logging.DEBUG if app.debug else logging.INFO),
                        format="%(levelname)s %(name)s %(funcName)s %(lineno)d:  %(message)s")
    unittest.main()
