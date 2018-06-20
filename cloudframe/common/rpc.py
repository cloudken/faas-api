
import grpc
import json

from cloudframe.protos import function_pb2
from cloudframe.protos import function_pb2_grpc
from cloudframe.protos import heartbeat_pb2
from cloudframe.protos import heartbeat_pb2_grpc


class MyRPC(object):
    def __init__(self, worker_data):
        self.host = worker_data['host_ip'] + ':' + str(worker_data['host_port'])
        self.channel = grpc.insecure_channel(self.host)

    def call_function(self, opr, tenant, version, res, res_id, req):
        req_str = json.dumps(req)
        stub = function_pb2_grpc.GreeterStub(self.channel)
        response = stub.Call(function_pb2.FunctionRequest(
            opr=opr, tenant=tenant, version=version,
            resource=res, res_id=res_id, req=req_str))
        return response.return_code, response.ack

    def call_heartbeat(self):
        stub = heartbeat_pb2_grpc.GreeterStub(self.channel)
        response = stub.Call(heartbeat_pb2.HbRequest())
        return response.return_code, response.ack
