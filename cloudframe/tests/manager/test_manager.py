
import mock
from six.moves import http_client
import testtools

# from cloudframe.common import exception
from cloudframe.manager.manager import FunctionManager
from cloudframe.driver.docker import Instance
from cloudframe.common.rpc import MyRPC


class TestManagerServers(testtools.TestCase):
    manager = FunctionManager()

    def setUp(self):
        super(TestManagerServers, self).setUp()

    @mock.patch.object(Instance, '_create_instance')
    @mock.patch.object(MyRPC, 'call_function')
    def test_function_call(self, mock_cf, mock_ci):
        domain = 'dom1'
        version = 'v1'
        tenant = 'tenant'
        res = 'res1'
        opr = 'post'
        req = {'name': 'server 1'}
        ack = {'result': 'OK'}
        mock_cf.return_value = http_client.OK, ack
        rv = self.manager.function_call(domain, version, tenant, res, opr, req)
        mock_ci.assert_called_once()
        self.assertEqual(http_client.OK, rv[0])
        self.assertEqual(ack, rv[1])
