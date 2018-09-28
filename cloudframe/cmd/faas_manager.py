# -*- encoding: utf-8 -*-
#
# Copyright 2013 Hewlett-Packard Development Company, L.P.
# All Rights Reserved.
#
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

"""
The Framework Service
"""

from concurrent import futures
from gevent import monkey
# from gevent import threadpool
# import grpc
import grpc._cython.cygrpc
import logging
import time

from cloudframe.common import job
from cloudframe.protos import worker_pb2_grpc
from cloudframe.api.grpc_service import WorkerServicer

COROUTINES_NUM = 10
LIFE_CYCLE = 60 * 60
MAX_WORKERS = 10
HOST_PORT = 50051


def main():
    monkey.patch_all()
    grpc._cython.cygrpc.init_grpc_gevent()
    LOG = logging.getLogger(__name__)
    LOG.debug("Starting...")
    job.start_worker(COROUTINES_NUM)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_WORKERS))
    worker_pb2_grpc.add_GreeterServicer_to_server(WorkerServicer(), server)
    host = '[::]:' + str(HOST_PORT)
    server.add_insecure_port(host)
    LOG.debug("Starting grpc server...")
    server.start()
    try:
        while True:
            time.sleep(LIFE_CYCLE)
    except KeyboardInterrupt:
        exit(0)


if __name__ == "__main__":
    main()
