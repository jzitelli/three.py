import logging
_logger = logging.getLogger(__name__)

import os.path
import json

from flask import Blueprint, request, jsonify

STATIC_FOLDER = os.path.abspath(os.path.split(__file__)[0])

WRITE_FOLDER = os.path.join(STATIC_FOLDER, 'shaderlib')
if not os.path.exists(WRITE_FOLDER):
    raise Exception('write is disabled, you need to create the write folder %s' % WRITE_FOLDER)



blueprint = Blueprint('pyserver', __name__,
                      static_folder=STATIC_FOLDER,
                      static_url_path='')



@blueprint.route("/read")
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



@blueprint.route("/write", methods=['POST'])
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



@blueprint.route('/log', methods=['POST'])
def log():
    """Post message from client to the server log
    """
    msg = request.form['msg']
    _logger.info(msg)
    response = {'status': 0}
    return jsonify(response)
