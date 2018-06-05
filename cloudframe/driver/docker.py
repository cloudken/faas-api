
import fileinput
import logging
import random

from cloudframe.common.utils import execute
from cloudframe.common.utils import generate_uuid

LOG = logging.getLogger(__name__)

HOSTS = [
    '192.168.1.1',
    '192.168.1.2',
    '192.168.1.3']

REGISTRY_IP = '10.62.99.232'
REGISTRY_PORT = 5000


class Instance(object):
    def __init__(self, registry_ip=None, registry_port=None):
        if registry_ip is None:
            self.registry_ip = REGISTRY_IP
        else:
            self.registry_ip = registry_ip
        if registry_port is None:
            self.registry_port = REGISTRY_PORT
        else:
            self.registry_port = registry_port

    def create(self, app_info, port):
        num = random.randint(0, len(HOSTS) - 1)
        host = HOSTS[num]
        image = 'http://' + self.registry_ip + ':' + self.registry_port + '/' + app_info
        name = app_info + '_' + generate_uuid()
        self._create_instance(name, image, host, port)
        ack = {
            'name': name,
            'image': image,
            'host_ip': host,
            'host_port': port,
            'status': 'OK'
        }
        return ack

    def _create_instance(self, name, image, host, port):
        LOG.debug('Create instance for image %(image)s on host %(host)s begin...',
                  {'image': image, 'host': host})

        # do something
        base_path = '/root/faas/worker-deploy/'
        hosts_file = base_path + 'hosts'
        fo = open(hosts_file, 'w')
        fo.write("[nodes]\n")
        fo.write(host)
        fo.flush()
        fo.close()

        vars_file = base_path + 'vars.yml'
        for line in fileinput.input(vars_file, inplace=1):
            line = line.strip()
            strs = line.split(':')
            if 'image' in strs[0]:
                line = strs[0] + ': ' + image
            if 'name' in strs[0]:
                line = strs[0] + ': ' + name
            if 'port' in strs[0]:
                line = strs[0] + ': ' + port
            print(line)

        ans_file = base_path + 'image_deploy.yml'
        execute('ansible-playbook', ans_file, '-i', hosts_file,
                check_exit_code=[0], run_as_root=True)

        LOG.debug('Create instance for image %(image)s on host %(host)s end.',
                  {'image': image, 'host': host})
