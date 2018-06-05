
from cloudframe.manager.scheduler import FunctionScheduler
from cloudframe.common.rpc import MyRPC

MAX_RETRY = 3


class FunctionManager(object):
    def __init__(self):
        self.scheduler = FunctionScheduler()

    def function_call(self, domain, version, tenant, res, opr, req=None, res_id=None):
        for index in range(MAX_RETRY):
            index = index
            worker_data = self.scheduler.get_worker(domain, version, res, opr)
            if worker_data is not None:
                rpc = MyRPC(worker_data)
                return rpc.call_function(opr, tenant, version, res, res_id, req)
