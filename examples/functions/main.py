import os
import json
import logging

from konfig import get_values_from_k8s

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger('main')


def konfig():
    values_from_k8s = get_values_from_k8s()
    return json.dumps(values_from_k8s)
