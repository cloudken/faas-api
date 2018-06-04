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

import logging
import sqlite3
import os

os.environ.setdefault('LOG_LEVEL', 'DEBUG')
loglevel_map = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARN': logging.WARN,
    'ERROR': logging.ERROR,
}
logging.basicConfig(
    level=loglevel_map[os.environ['LOG_LEVEL']],
    format='%(asctime)s.%(msecs)03d %(filename)s[line:%(lineno)d]'
           ' %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='/var/log/cloudframe/cf-dbsync.log',
    filemode='a')


def main():
    LOG = logging.getLogger(__name__)
    LOG.debug("Starting...")

    try:
        con = sqlite3.connect('/root/data/cf.db')
        con.execute("CREATE TABLE version \
            (id INTEGER PRIMARY KEY AUTOINCREMENT, \
             ver TEXT UNIQUE NOT NULL, \
             created_at TEXT NOT NULL, \
             updated_at TEXT NOT NULL);")
        con.execute("CREATE TABLE server \
            (id INTEGER PRIMARY KEY AUTOINCREMENT, \
             uuid TEXT UNIQUE NOT NULL, \
             tenant TEXT NOT NULL, \
             name TEXT NOT NULL, \
             created_at TEXT, \
             updated_at TEXT);")
        con.close()
        LOG.debug("Create Tables end.")
    except Exception as e:
        LOG.error('dbsync error: %s' % (e.message))
        return 1
    return 0
