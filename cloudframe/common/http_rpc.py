import httplib2
import json
from six.moves import http_client

from restframe.common import exception


class hrpc(object):
    def __init__(self, host, url, timeout=15):
        self.endpoint = host + url
        self.http = httplib2.Http(timeout=timeout)

    def post(self, object_id, input_parameters=None):
        if input_parameters is None:
            body = None
            headers = None
        else:
            body = json.dumps(input_parameters)
            headers = {'Content-Type': 'application/json'}
        url = self.endpoint + object_id
        response, content = self.http.request(url, 'POST', body=body,
                                              headers=headers)
        if response.status in [http_client.OK, http_client.CREATED]:
            return json.loads(content)
        else:
            raise exception.HttpError(response.status)

    def get(self, object_id):
        url = self.endpoint + object_id
        response, content = self.http.request(url, 'GET')
        if response.status == http_client.OK:
            return json.loads(content)
        else:
            raise exception.HttpError(response.status)

    def get_list(self):
        url = self.endpoint
        response, content = self.http.request(url, 'GET')
        if response.status == http_client.OK:
            return json.loads(content)
        else:
            raise exception.HttpError(response.status)

    def delete(self, object_id):
        url = self.endpoint + object_id
        response, content = self.http.request(url, 'DELETE')
        if response.status == http_client.OK:
            return json.loads(content)
        else:
            raise exception.HttpError(response.status)
