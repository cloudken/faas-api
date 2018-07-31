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

from gevent import monkey
from gevent import pywsgi
import logging

from cloudframe.common import job
from cloudframe.api.flask_app import app

LISTEN_PORT = 5000
COROUTINES_NUM = 10


def main():
    monkey.patch_all()
    LOG = logging.getLogger(__name__)
    LOG.debug("Starting...")
    server = pywsgi.WSGIServer(('0.0.0.0', LISTEN_PORT), app)
    job.start_worker(COROUTINES_NUM)
    server.serve_forever()
