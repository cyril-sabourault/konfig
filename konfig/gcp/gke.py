import os
import json
import logging
import tempfile

from ..utils.http import HTTP
from base64 import b64decode

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger('gke')


class GKE:
    def __init__(self, cluster_id):
        self.GKE_API_URL = "https://container.googleapis.com/"
        self.http = HTTP()
        self.cluster_id = cluster_id
        self.endpoint = self.__get_endpoint()

    def __get_endpoint(self):
        url = self.GKE_API_URL + 'v1/{cluster_id}'.format(
            cluster_id=self.cluster_id)
        data = self.http.get(url)

        return data.get('endpoint')

    def get_resource(self, reference):
        url = "https://{endpoint}/api/v1/namespaces/{namespace}/{kind}s/{resource_name}".format(
            endpoint=self.endpoint,
            namespace=reference.get('namespace'),
            kind=reference.get('kind'),
            resource_name=reference.get('resource_name')
        )
        data = self.http.get(url)
        key = data.get('data').get(reference.get('key'))

        if (reference.get('kind') == 'secret'):
            return b64decode(key).decode('ascii')

        if (reference.get('tempFile') is not None):
            try:
                temp_file = __make_temp_file(key)
                return temp_file
            except (Exception) as e:
                return e

        return key

        def __make_temp_file(content):
            try:
                temp_file = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
                temp_file.write(content)
                temp_file.close()

                return temp_file
            except (Exception) as e:
                logger.error('[ERROR] writing temp file: e ({}): {}'.format(type(e), e))
                return e
