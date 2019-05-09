import os
import json
import logging
from flask import Flask, jsonify
from gcp.cloud_functions import Cloud_Functions
from gcp.cloud_run import Cloud_Run
from gcp.gke import GKE

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger('main')

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'healthy service :)'


@app.route('/konfig')
# def konfig():
def konfig(e):
    runtime = get_runtime()
    environment_variables = runtime.get_environment_variables()

    registered_gkes = {}
    values_from_k8s = {}
    for key, value in environment_variables.items():
        if (not is_reference(value)):
            continue

        print(key + ': ' + value)
        reference = parse_reference(value)

        gke = registered_gkes.get(reference.get('cluster_id'))
        if (gke is None):
            gke = GKE(reference.get('cluster_id'))
            registered_gkes[reference.get('cluster_id')] = gke

        resource = gke.get_resource(reference)
        os.environ[key] = resource
        values_from_k8s[key] = resource

        print('resource ({}): {}'.format(type(resource), resource))
        print('---')
    return json.dumps(values_from_k8s)
    # return jsonify(values_from_k8s)


def get_runtime():
    if (os.environ.get('FUNCTION_NAME')):
        return Cloud_Functions()

    if (os.environ.get('K_SERVICE')):
        return Cloud_Run()

    return None


def is_reference(value):
    if (value.startswith('$SecretKeyRef:') or value.startswith('$ConfigMapKeyRef:')):
        return True
    return False


def parse_reference(value):
    if (value.startswith('$ConfigMapKeyRef:')):
        path = value.split('$ConfigMapKeyRef:')[1]
        kind = 'configmap'

    if (value.startswith('$SecretKeyRef:')):
        path = value.split('$SecretKeyRef:')[1]
        kind = 'secret'

    ss = path.split('/')
    cluster_id = '/'.join(ss[i] for i in range(1, 7))

    namespace = ss[8]
    resource_name = ss[10]
    key = ss[12]

    return {
        "cluster_id": cluster_id,
        "namespace": namespace,
        "kind": kind,
        "resource_name": resource_name,
        "key": key
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT'))
