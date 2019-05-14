from requests import ConnectionError, HTTPError
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

    def __get(self, headers, url, json=True):
        try:
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()

            if (json):
                data = response.json()
            else:
                data = response.text
        except (ConnectionError, HTTPError) as e:
            logging.error('{}: {}'.format(type(e), e))
            data = {}

        return data

    def __get_access_token(self):
        access_token_url = "/v1/instance/service-accounts/default/token"

        data = self.get_metadata(access_token_url, json=True)
        return data.get("access_token", "")

    def get(self, url):
        headers = {
            'Authorization': "Bearer {access_token}".format(access_token=self.access_token)
        }

        return self.__get(headers, url)

    def get_metadata(self, url, json=False):
        metadata_server = "http://metadata/computeMetadata"
        headers = {
            'Metadata-Flavor': 'Google'
        }

        json = json or False
        return self.__get(headers, metadata_server + url, json=json)
