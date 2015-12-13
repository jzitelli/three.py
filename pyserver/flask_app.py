"""REST thingys to help accomplish:

1. extracting three.js shader library into a file
2. testing
3. ?
"""

import os
import json
import logging
_logger = logging.getLogger(__name__)

from flask import Flask, render_template, request, jsonify, Markup

STATIC_FOLDER = os.getcwd()
app = Flask(__name__,
            static_folder=STATIC_FOLDER,
            static_url_path='')
app.debug = True
app.config['TESTING'] = True

import sys
sys.path.insert(0, os.path.join(os.path.split(__file__)[0], os.pardir))
import pyserver
from pyserver import scenes


@app.route('/')
def index():
    scene = scenes.index_scene()
    return render_template('index.html',
                           json_config=Markup("""<script>
var JSON_SCENE = %s;
</script>""" % json.dumps(scene.export(), indent=2)),
                           threejs_lib='lib/three-r73.js')


@app.route('/config')
def config_page():
    scene = scenes.config_scene(url_prefix='../')
    return render_template('index.html',
                           json_config=Markup("""<script>
var JSON_SCENE = %s;
</script>""" % json.dumps(scene.export(), indent=2)),
                           threejs_lib='lib/three-r73.js')


@app.route("/read")
def read():
    """Handles requests to read file contents"""
    filename = os.path.join(STATIC_FOLDER, request.args['file'])
    response = {}
    try:
        with open(filename, 'r') as f:
            response['text'] = f.read()
    except Exception as err:
        response['error'] = str(err)
    return jsonify(response)


WRITE_FOLDER = os.path.join(os.getcwd(), 'write')
try:
    if not os.path.exists(WRITE_FOLDER):
        raise Exception('write is disabled, you need to create the write folder %s' % WRITE_FOLDER)
    @app.route("/write", methods=['POST'])
    def write():
        filename = os.path.join(WRITE_FOLDER, os.path.split(request.args['file'])[1])
        try:
            if request.json is not None:
                with open(filename, 'w') as f:
                    f.write(json.dumps(request.json))
            else:
                with open(filename, 'w') as f:
                    f.write(request.form['text'])
            response = {'filename': filename}
            _logger.info('wrote %s' % filename)
        except Exception as err:
            response = {'error': str(err)}
        return jsonify(response)
except Exception as err:
    @app.route('/write', methods=['POST'])
    def write():
        filename = os.path.join(WRITE_FOLDER, os.path.split(request.args['file'])[1])
        return jsonify({'filename': filename,
                        'writeDisabled': True})


@app.route('/log', methods=['POST'])
def log():
    """Post message from client to the server log
    """
    msg = request.form['msg']
    _logger.info(msg)
    response = {'status': 0}
    return jsonify(response)


def main():
    _logger.info("app.config:\n%s" % '\n'.join(['%s: %s' % (k, str(v))
                                                for k, v in sorted(app.config.items(),
                                                                   key=lambda i: i[0])]))
    _logger.info("STARTING FLASK APP!!!!!!!!!!!!!")
    app.run(host='0.0.0.0')



test_cannon = None
if app.config.get('TESTING'):
    sys.path.insert(0, os.path.join(os.path.split(__file__)[0], os.path.pardir, 'test'))
    import test_cannon as testcan
    test_cannon = testcan.test_cannon
if test_cannon is not None:
    test_cannon = app.route('/test/cannon')(test_cannon)


if __name__ == "__main__":
    logging.basicConfig(level=(logging.DEBUG if app.debug else logging.INFO),
                        format="%(levelname)s %(name)s %(funcName)s %(lineno)d:  %(message)s")
    main()
