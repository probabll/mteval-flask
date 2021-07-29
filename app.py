from integrate import init, score
from flask import Flask, jsonify, request, abort, Response

from werkzeug.exceptions import BadRequest, InternalServerError

import sys
import socket
import os
import json
import logging


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
scorers = None
app = Flask(__name__)

@app.route("/", methods=['GET'])
def root():
    return "This is a MT evaluation module. Use the /score endpoint for evaluation."

@app.route("/score", methods=['POST'])
def compute_scores():
    return handle_POST(score)

def handle_POST(func):
    """
    Handles POST requests where the body of the request is JSON with keys 
        'hyps', 'refs', and 'srcs'.
    For example, {"hyps": ["hello world"], "refs": ["Hello, world!"], "srcs": ["Ola, mundo."]}
    :param func. The integration function.
    """
    payload = request.json
    if not payload:
        return BadRequest("No payload given")
    try:
        result = func(scorers, hyps=payload["hyps"], refs=payload["refs"], srcs=payload["srcs"], logger=logging)
        return jsonify(result)
    except Exception as e:
        logging.exception(
            "Unexpected Error when handling a POST request. Exception caught: %s.", e)
        return InternalServerError(e)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError(f"Usage: {sys.argv[0]} metric1:arg1=value1:arg2=value2 (...)")
    args = sys.argv[1:]
    scorers = init(args)
    app.run(host='0.0.0.0', port=4000)
