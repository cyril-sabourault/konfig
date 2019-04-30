import os
import json
import logging
import requests
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

        response = requests.get(access_token_url, headers=headers)
        data = response.json()

        return data.get("access_token", "")

    def get(self, url):
        headers = {
            'Authorization': "Bearer {access_token}".format(access_token=self.access_token)
        }

        response = requests.get(url, headers=headers, verify=False)
        data = response.json()

        return data
