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

import sys
sys.path.append(os.getcwd())
import three


@app.route('/')
def index():
    scene = three.Scene()
    boxMesh = three.Mesh(geometry=three.BoxGeometry(width=1, height=1, depth=1),
                         material=three.MeshBasicMaterial(color=0xff0000),
                         position=[1, 0, -4])
    scene.add(boxMesh)
    sphereMesh = three.Mesh(geometry=three.SphereBufferGeometry(radius=0.5),
                            material=three.MeshBasicMaterial(color=0x00ff00),
                            position=[0, 1, -4])
    scene.add(sphereMesh)
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
if not os.path.exists(WRITE_FOLDER):
    raise Exception('create the write folder %s' % WRITE_FOLDER)
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
    except Exception as err:
        response = {'error': str(err)}
    return jsonify(response)


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


if __name__ == "__main__":
    logging.basicConfig(level=(logging.DEBUG if app.debug else logging.INFO),
                        format="%(asctime)s %(levelname)s %(name)s %(funcName)s %(lineno)d:  %(message)s")
    main()
