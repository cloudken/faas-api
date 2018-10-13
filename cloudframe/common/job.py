#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import gevent
from gevent.queue import Queue
import logging


Tasks = Queue()
LOG = logging.getLogger(__name__)


def worker(n):
    while True:
        task = Tasks.get()
        LOG.debug('Worker %d got task %s...' % (n, task))
        gevent.spawn(task[0], task[1])
        LOG.debug('Worker %d task done.' % (n))


def start_worker(num_jobs):
    for i in range(num_jobs):
        gevent.spawn(worker, i)


def rpc_cast(function, **kwargs):
    item = [function, kwargs]
    Tasks.put_nowait(item)


def rpc_call(function, **kwargs):
    item = [function, kwargs]
    Tasks.put(item)
