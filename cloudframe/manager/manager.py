
from cloudframe.manager.scheduler import FunctionScheduler
from cloudframe.common.rpc import MyRPC

MAX_RETRY = 5
FAAS_DYING = 1033


class FunctionManager(object):
    def __init__(self):
        self.scheduler = FunctionScheduler()

    def function_call(self, domain, version, tenant, res, opr, req=None, res_id=None):
        for index in range(MAX_RETRY):
            index = index
            worker_data = self.scheduler.get_worker(domain, version, res, opr)
            if worker_data is not None:
                rpc = MyRPC(worker_data)
                rv = rpc.call_function(opr, tenant, version, res, res_id, req)
                if rv[0] == FAAS_DYING:
                    self.scheduler.set_worker_dying(worker_data)
                else:
                    return rv
