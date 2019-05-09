import os
import json
import logging
from utils.http import HTTP

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger('cloud_run')


class Cloud_Run:
    def __init__(self):
        self.http = HTTP()
        self.region = self.__get_region()
        self.service = self.__get_service()
        self.project = self.__get_project()
        self.run_endpoint = self.__get_run_endpoint()

    def __get_run_endpoint(self):
        return "https://{region}-run.googleapis.com/apis/serving.knative.dev/v1alpha1/{service_name}".format(
            region=self.region,
            service_name=self.__get_service_name())

    def __get_region(self):
        return "us-central1"

    def __get_service(self):
        return os.environ.get("K_SERVICE")

    def __get_project(self):
        return os.environ.get("GOOGLE_CLOUD_PROJECT")

    def __get_service_name(self):
        if (self.service == "") or (self.project == ""):
            logger.warning(
                "If you're running locally, have you `source local.env`?")

        return "namespaces/{project}/services/{service}".format(
            project=self.project,
            service=self.service)

    def get_environment_variables(self):
        querystring = "?fields=spec.runLatest.configuration.revisionTemplate.spec.container.env"

        try:
            data = self.http.get(self.run_endpoint + querystring)
            if (len(data) == 0):
                return {}

            environment_variables = data.get('spec').get('runLatest').get(
                'configuration').get('revisionTemplate').get('spec').get('container').get('env')

            if (len(environment_variables) == 0):
                return {}
        except AttributeError as e:
            logging.error('{}: {}'.format(type(e), e.message))
            return {}

        return {
            env_var.get('name'): env_var.get('value')
            for env_var in environment_variables
        }
