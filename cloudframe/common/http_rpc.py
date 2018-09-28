import httplib2
import json
import logging
from six.moves import http_client

from cloudframe.common import exception

LOG = logging.getLogger(__name__)


class HRPC(object):
    def __init__(self, host, url, timeout=15):
        self.endpoint = host + url
        self.http = httplib2.Http(timeout=timeout)

    def post(self, object_id=None, input_parameters=None):
        if input_parameters is None:
            body = None
            headers = None
        else:
            body = json.dumps(input_parameters)
            headers = {'Content-Type': 'application/json'}
        if object_id is None:
            url = self.endpoint
        else:
            url = self.endpoint + object_id
        LOG.debug('Post: url %(url)s, body %(body)s', {'url': url, 'body': body})
        response, content = self.http.request(url, 'POST', body=body, headers=headers)
        LOG.debug('Post result: status %(st)s, content %(ct)s', {'st': response.status, 'ct': content})
        if response.status in [http_client.OK, http_client.CREATED, http_client.NO_CONTENT]:
            if response.status == http_client.NO_CONTENT:
                return
            else:
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
        if response.status in [http_client.OK, http_client.NO_CONTENT]:
            if response.status == http_client.NO_CONTENT:
                return
            else:
                return json.loads(content)
        else:
            raise exception.HttpError(response.status)

    def put(self, input_parameters, object_id=None):
        if input_parameters is None:
            raise exception.Invalid()
        else:
            body = json.dumps(input_parameters)
            headers = {'Content-Type': 'application/json'}
        if object_id is None:
            url = self.endpoint
        else:
            url = self.endpoint + object_id
        response, content = self.http.request(url, 'PUT', body=body,
                                              headers=headers)
        if response.status == http_client.OK:
            return json.loads(content)
        else:
            raise exception.HttpError(response.status)

    def post_no_ack(self, object_id=None, input_parameters=None):
        if input_parameters is None:
            body = None
            headers = None
        else:
            body = json.dumps(input_parameters)
            headers = {'Content-Type': 'application/json'}
        if object_id is None:
            url = self.endpoint
        else:
            url = self.endpoint + object_id
        LOG.debug('Post_no_ack: url %(url)s, body %(body)s', {'url': url, 'body': body})
        response, content = self.http.request(url, 'POST', body=body, headers=headers)
        LOG.debug('Post_no_ack result: status %(st)s, content %(ct)s', {'st': response.status, 'ct': content})
        if response.status not in [http_client.OK, http_client.CREATED, http_client.NO_CONTENT]:
            raise exception.HttpError(response.status)
