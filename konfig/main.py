import os
import logging

from urllib.parse import urlparse, parse_qs

from .gcp.cloud_functions import Cloud_Functions
from .gcp.cloud_run import Cloud_Run
from .gcp.gke import GKE

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger('konfig')


def get_values_from_k8s():
    runtime = __get_runtime()
    environment_variables = runtime.get_environment_variables()

    registered_gkes = {}
    values_from_k8s = {}
    for key, value in environment_variables.items():
        if (not __is_reference(value)):
            continue

        print(key + ': ' + value)
        reference = __parse_reference(value)
        if (not reference):
            logger.warning('reference is badly constructed')
            continue

        gke = registered_gkes.get(reference.get('cluster_id'))
        if (gke is None):
            gke = GKE(reference.get('cluster_id'))
            registered_gkes[reference.get('cluster_id')] = gke

        resource = gke.get_resource(reference)
        os.environ[key] = resource
        values_from_k8s[key] = resource

        print('resource ({}): {}'.format(type(resource), resource))
        print('---')

    return values_from_k8s


def __get_runtime():
    if (os.environ.get('FUNCTION_NAME')):
        return Cloud_Functions()

    if (os.environ.get('K_SERVICE')):
        return Cloud_Run()

    return None


def __is_reference(value):
    if (value.startswith('$SecretKeyRef:') or value.startswith('$ConfigMapKeyRef:')):
        return True
    return False


def __parse_reference(value):
    if (value.startswith('$ConfigMapKeyRef:')):
        path = value.split('$ConfigMapKeyRef:')[1]
        kind = 'configmap'

    if (value.startswith('$SecretKeyRef:')):
        path = value.split('$SecretKeyRef:')[1]
        kind = 'secret'

    try:
        url = urlparse(path)
        qs = parse_qs(url.query)

        temp_file = qs.get('tempFile')[0]
    except (IndexError, TypeError) as e:
        temp_file = None

    try:
        ss = path.split('/')
        cluster_id = '/'.join(ss[i] for i in range(1, 7))

        namespace = ss[8]
        resource_name = ss[10]
        key = ss[12]
    except (IndexError, Exception) as e:
        return {}

    reference = {
        "kind": kind,
        "cluster_id": cluster_id,
        "namespace": namespace,
        "resource_name": resource_name,
        "key": key,
        "tempFile": temp_file
    }

    return reference


# __get_tempFile('$SecretKeyRef:/projects/sandbox-csabourault/zones/europe-west1-b/clusters/k0/namespaces/default/secrets/env/keys/config.json?tempFile=true')
reference = __parse_reference(
    '$SecretKeyRef:/projects/sandbox-csabourault/zones/europe-west1-b/clusters/k0/namespaces/default/secrets/env/keys/config.json?tempFile=')
print('[DEBUG] reference ({}): {}'.format(type(reference), reference))