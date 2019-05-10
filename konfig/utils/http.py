import os
import json
import logging
import requests
from requests import ConnectionError, HTTPError
import urllib3
urllib3.disable_warnings()

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger('http')


class HTTP():
    def __init__(self):
        self.access_token = self.__get_access_token()

    def __get_access_token(self):
        access_token_url = "http://metadata/computeMetadata/v1/instance/service-accounts/default/token"
        headers = {
            'Metadata-Flavor': "Google"
        }

        try:
            response = requests.get(access_token_url, headers=headers)
            response.raise_for_status()
            data = response.json()
        except ConnectionError as e:
            logging.error('{}: {}'.format(type(e), e))
            data = {}

        return data.get("access_token", "")

    def get(self, url):
        headers = {
            'Authorization': "Bearer {access_token}".format(access_token=self.access_token)
        }

        try:
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            data = response.json()
        except (ConnectionError, HTTPError) as e:
            logging.error('{}: {}'.format(type(e), e.message))
            data = {}

        return data
