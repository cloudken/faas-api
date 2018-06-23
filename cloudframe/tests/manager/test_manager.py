
import mock
from six.moves import http_client
import testtools

from cloudframe.common import exception
from cloudframe.manager.manager import FunctionManager
from cloudframe.driver.docker import Instance
from cloudframe.common.rpc import MyRPC


class TestManagerServers(testtools.TestCase):
    manager = FunctionManager()

    def setUp(self):
        super(TestManagerServers, self).setUp()

    @mock.patch.object(Instance, '_create_instance')
    @mock.patch.object(MyRPC, 'call_function')
    @mock.patch.object(MyRPC, 'call_heartbeat')
    def test_function_call(self, mock_ch, mock_cf, mock_ci):
        domain = 'dom1'
        version = 'v1'
        tenant = 'tenant'
        res = 'res01'
        opr = 'post'
        req = {'name': 'server 1'}
        ack = {'result': 'OK'}
        mock_cf.return_value = http_client.OK, ack
        mock_ch.return_value = http_client.OK, ack
        rv = self.manager.function_call(domain, version, tenant, res, opr, req)
        mock_ci.assert_called_once()
        mock_ch.assert_called_once()
        self.assertEqual(http_client.OK, rv[0])
        self.assertEqual(ack, rv[1])

    @mock.patch.object(Instance, '_create_instance')
    @mock.patch.object(MyRPC, 'call_function')
    @mock.patch.object(MyRPC, 'call_heartbeat')
    def test_function_call_heartbeat(self, mock_ch, mock_cf, mock_ci):
        domain = 'dom1'
        version = 'v1'
        tenant = 'tenant'
        res = 'res01'
        opr = 'post'
        req = {'name': 'server 1'}
        ack = {'result': 'OK'}
        mock_cf.return_value = http_client.OK, ack
        mock_ch.side_effect = [exception.HttpError, exception.HttpError, [http_client.OK, ack]]
        rv = self.manager.function_call(domain, version, tenant, res, opr, req)
        mock_ci.assert_called_once()
        mock_ch.assert_called()
        self.assertEqual(http_client.OK, rv[0])
        self.assertEqual(ack, rv[1])

    @mock.patch.object(Instance, '_create_instance')
    @mock.patch.object(MyRPC, 'call_function')
    def test_function_call_create_error(self, mock_cf, mock_ci):
        domain = 'dom1'
        version = 'v1'
        tenant = 'tenant'
        res = 'res01'
        opr = 'post'
        req = {'name': 'server 1'}
        mock_ci.side_effect = exception.HttpError
        self.assertRaises(exception.CreateError, self.manager.function_call, domain, version, tenant, res, opr, req)

    @mock.patch.object(Instance, '_create_instance')
    @mock.patch.object(MyRPC, 'call_function')
    @mock.patch.object(MyRPC, 'call_heartbeat')
    def test_function_call_heartbeat_error(self, mock_ch, mock_cf, mock_ci):
        domain = 'dom1'
        version = 'v1'
        tenant = 'tenant'
        res = 'res01'
        opr = 'post'
        req = {'name': 'server 1'}
        ack = {'result': 'OK'}
        mock_cf.return_value = http_client.OK, ack
        mock_ch.side_effect = exception.HttpError
        self.assertRaises(exception.CreateError, self.manager.function_call, domain, version, tenant, res, opr, req)

    def test_function_call_no_res(self):
        domain = 'dom1'
        version = 'v1'
        tenant = 'tenant'
        res = 'wrong-res'
        opr = 'put'
        req = {'name': 'server 1'}
        self.assertRaises(exception.ObjectNotFound, self.manager.function_call, domain, version, tenant, res, opr, req)

    def test_function_call_opr_error(self):
        domain = 'dom1'
        version = 'v1'
        tenant = 'tenant'
        res = 'res01'
        opr = 'write'
        req = {'name': 'server 1'}
        self.assertRaises(exception.ParameterInvalid, self.manager.function_call, domain, version, tenant, res, opr, req)
