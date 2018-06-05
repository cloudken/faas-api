
import random

from cloudframe.manager.function import FunctionInstances
from cloudframe.manager.function import MAX_INS


class FunctionScheduler(FunctionInstances):
    def __init__(self):
        super(FunctionScheduler, self).__init__()

    def get_worker(self, domain, version, res, opr):
        num = random.randint(1, MAX_INS)
        worker = self.fun.get(domain, version, res, opr, num)
        if worker is None:
            worker = self.fun.create(domain, version, res, opr, num)
        return worker
