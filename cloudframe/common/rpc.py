
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
            req_str = json.dumps(req)
            stub = function_pb2_grpc.GreeterStub(self.channel)
            response = stub.Call(function_pb2.FunctionRequest(
                opr=opr, tenant=tenant, version=version,
                resource=res, res_id=res_id, req=req_str))
            return response.return_code, response.ack
        except Exception as e:
            LOG.error('Call function failed, error info: %(error)s', {'error': e})
            raise exception.RpcCallFailed(type='function', error=e)

    def call_heartbeat(self):
        try:
            stub = heartbeat_pb2_grpc.GreeterStub(self.channel)
            response = stub.Call(heartbeat_pb2.HbRequest())
            return response.return_code, response.ack
        except Exception as e:
            LOG.error('Call heartbeat failed, error info: %(error)s', {'error': e})
            raise exception.RpcCallFailed(type='heartbeat', error=e)
