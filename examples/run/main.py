import os
import logging
from flask import Flask, jsonify

from konfig import get_values_from_k8s

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger('main')

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'healthy service :)'


@app.route('/konfig')
def konfig():
    values_from_k8s = get_values_from_k8s()
    return jsonify(values_from_k8s)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT'))
