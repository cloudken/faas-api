
import logging

from cloudframe.common.rpc import MyRPC
from cloudframe.common import exception
from cloudframe.manager.scheduler import FunctionScheduler

LOG = logging.getLogger(__name__)

MAX_RETRY = 5
FAAS_DYING = 1033


class FunctionManager(object):
    def __init__(self):
        self.scheduler = FunctionScheduler()

    def function_call(self, domain, version, tenant, res, opr, req=None, res_id=None):
        for index in range(MAX_RETRY):
            LOG.debug('FunctionManager, try %(index)d times...', {'index': index + 1})
            worker_data = self.scheduler.get_worker(domain, version, res, opr)
            if worker_data is not None:
                try:
                    rpc = MyRPC(worker_data)
                    rv = rpc.call_function(opr, tenant, version, res, res_id, req)
                    if rv[0] == FAAS_DYING:
                        self.scheduler.set_worker_dying(worker_data)
                    else:
                        return rv
                except Exception as e:
                    LOG.debug('FunctionManager call failed, error info %(error)s', {'error': e})
                    self.scheduler.set_worker_dying(worker_data)
        raise exception.RpcCallFailed(type='function', error='too many error')

    def put_faasinfo(self, faas_input):
        self.scheduler.put_faas(faas_input)

    def get_worker(self, domain, version, res, opr):
        return self.scheduler.get_worker(domain, version, res, opr)
