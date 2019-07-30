import os
import logging

from ..utils.http import HTTP

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger('cloud_functions')

class Cloud_Functions:
    def __init__(self):
        self.http = HTTP()
        self.project = self.__get_project()
        self.region = self.__get_region()
        self.function_name = self.__get_function_name()
        self.functions_endpoint = self.__get_functions_endpoint()

    def __get_project(self):
        return os.environ.get('GCLOUD_PROJECT')

    def __get_region(self):
        return os.environ.get('FUNCTION_REGION')

    def __get_function_name(self):
        return os.environ.get('FUNCTION_NAME')

    def __get_functions_endpoint(self):
        function_api = 'https://cloudfunctions.googleapis.com/v1'
        self_link = '/projects/{project}/locations/{region}/functions/{function_name}'.format(
            project=self.project,
            region=self.region,
            function_name=self.function_name)

        return function_api + self_link

    def get_environment_variables(self):
        querystring = '?fields=environmentVariables'
        data = self.http.get(self.functions_endpoint + querystring)

        return data.get('environmentVariables', {})
