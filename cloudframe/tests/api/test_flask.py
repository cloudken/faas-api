
from flask import json
import mock
from six.moves import http_client

from cloudframe.common import exception
from cloudframe.manager.manager import FunctionManager
from cloudframe.tests.api.base import ApiTestCase


class TestFlaskAPIServers(ApiTestCase):
    def setUp(self):
        super(TestFlaskAPIServers, self).setUp()

    @mock.patch.object(FunctionManager, 'function_call')
    def test_post(self, mock_fc):
        server = {"name": "server 1"}
        headers = {'content-type': 'application/json',
                   "Accept": "application/json"}
        server_str = json.dumps(server)
        mock_fc.return_value = http_client.OK, server_str
        rv = self.app.post('/domain/v1/tenants/admin/resoures',
                           data=json.dumps(server), headers=headers)
        mock_fc.assert_called_once_with(mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, server)
        result = json.loads(rv.data)
        self.assertEqual(server, result)

    @mock.patch.object(FunctionManager, 'function_call')
    def test_post_error(self, mock_fc):
        server = {"name": "server 1"}
        headers = {'content-type': 'application/json',
                   "Accept": "application/json"}
        mock_fc.side_effect = exception.Invalid
        rv = self.app.post('/domain/v1/tenants/admin/resoures',
                           data=json.dumps(server), headers=headers)
        mock_fc.assert_called_once_with(mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, server)
        self.assertEqual(http_client.BAD_REQUEST, rv.status_code)

    @mock.patch.object(FunctionManager, 'function_call')
    def test_put(self, mock_fc):
        server = {'name': 'server 1'}
        headers = {'content-type': 'application/json',
                   "Accept": "application/json"}
        server_str = json.dumps(server)
        mock_fc.return_value = http_client.OK, server_str
        rv = self.app.put('/domain/v1/tenants/admin/resoures/1234',
                          data=json.dumps(server), headers=headers)
        mock_fc.assert_called_once()
        result = json.loads(rv.data)
        self.assertEqual(server, result)

    @mock.patch.object(FunctionManager, 'function_call')
    def test_put_error(self, mock_fc):
        server = {'name': 'server 1'}
        headers = {'content-type': 'application/json',
                   "Accept": "application/json"}
        mock_fc.side_effect = exception.NotFound
        rv = self.app.put('/domain/v1/tenants/admin/resoures/1234',
                          data=json.dumps(server), headers=headers)
        mock_fc.assert_called_once()
        self.assertEqual(http_client.NOT_FOUND, rv.status_code)

    def test_put_noreq_error(self):
        rv = self.app.put('/domain/v1/tenants/admin/resoures/1234')
        self.assertEqual(http_client.BAD_REQUEST, rv.status_code)
