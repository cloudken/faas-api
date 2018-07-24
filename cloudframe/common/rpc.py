
import grpc
import json
import logging

from cloudframe.common import exception
from cloudframe.protos import function_pb2
from cloudframe.protos import function_pb2_grpc
from cloudframe.protos import heartbeat_pb2
from cloudframe.protos import heartbeat_pb2_grpc

LOG = logging.getLogger(__name__)


class MyRPC(object):
    def __init__(self, worker_data):
        self.host = worker_data['host_ip'] + ':' + str(worker_data['host_port'])
        self.channel = grpc.insecure_channel(self.host)

    def call_function(self, opr, tenant, version, res, res_id, req):
        try:
            LOG.debug('call_function [resource %(res)s, version %(ver)s, operation %(opr)s, host %(host)s] begin...',
                      {'res': res, 'ver': version, 'opr': opr, 'host': self.host})
            req_str = json.dumps(req)
            stub = function_pb2_grpc.GreeterStub(self.channel)
            response = stub.Call(function_pb2.FunctionRequest(
                opr=opr, tenant=tenant, version=version,
                resource=res, res_id=res_id, req=req_str))
            LOG.debug('call_function [resource %(res)s, version %(ver)s, operation %(opr)s, host %(host)s] end, return_code %(code)s.',
                      {'res': res, 'ver': version, 'opr': opr, 'host': self.host, 'code': response.return_code})
            return response.return_code, response.ack
        except Exception as e:
            LOG.error('call_function [host %(host)s] failed, error info: %(error)s',
                      {'host': self.host, 'error': e})
            raise exception.RpcCallFailed(type='function', error=e)

    def call_heartbeat(self):
        try:
            LOG.debug('call_heartbeat [host %(host)s] begin...', {'host': self.host})
            stub = heartbeat_pb2_grpc.GreeterStub(self.channel)
            response = stub.Call(heartbeat_pb2.HbRequest())
            LOG.debug('call_heartbeat [host %(host)s] end, return_code %(code)s.',
                      {'host': self.host, 'code': response.return_code})
            return response.return_code, response.ack
        except Exception as e:
            LOG.error('call_heartbeat [host %(host)s] failed, error info: %(error)s',
                      {'host': self.host, 'error': e})
            raise exception.RpcCallFailed(type='heartbeat', error=e)
