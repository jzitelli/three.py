from needle.cases import NeedleTestCase

import os.path
import sys
THREEPYDIR = os.path.abspath(os.path.join(os.path.split(__file__)[0], os.path.pardir))
if THREEPYDIR not in sys.path:
    sys.path.insert(0, THREEPYDIR)
from pyserver.flask_app import app, main


class MainTest(NeedleTestCase):
    def test_screenshot(self):
        self.driver.get('127.0.0.1:5000')
        self.assertScreenshot('canvas', 'screenshot')


if __name__ == "__main__":
    #app.run(host='0.0.0.0')
    import logging
    logging.basicConfig(level=(logging.DEBUG if app.debug else logging.INFO),
                        format="%(levelname)s %(name)s %(funcName)s %(lineno)d:  %(message)s")
    app.config['TESTING'] = True
    main()
