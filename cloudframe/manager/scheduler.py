
import random

from cloudframe.manager.function import FunctionInstances

MAX_INS = 5


class FunctionScheduler(FunctionInstances):
    def __init__(self):
        super(FunctionScheduler, self).__init__()

    def get_worker(self, domain, version, res, opr):
        num = random.randint(1, MAX_INS)
        worker = self.get(domain, version, res, opr, num)
        if worker is None:
            worker = self.create(domain, version, res, opr, num)
        return worker
