"""Flask application enabling server-side execution of Python code entered in
Primrose editors.

This script may be executed from the Primrose root directory to host a local
server (with a subset of the functionality available from the Tornado server [see start.py]) ::

    $ python pyserver/flask_app.py

The server can then be accessed locally at 127.0.0.1:5000."""

import os
import sys
import json
from copy import deepcopy
import logging
_logger = logging.getLogger(__name__)

from flask import Flask, render_template, request, jsonify

STATIC_FOLDER = os.getcwd()
app = Flask(__name__,
            static_folder=STATIC_FOLDER,
            static_url_path='')


@app.route('/')
def index():
    return render_template('index.html')


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


@app.route("/write", methods=['POST'])
def write():
    filename = os.path.join(os.getcwd(), 'writes', os.path.split(request.args['file'])[1])
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
