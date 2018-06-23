
import fileinput
import logging
import random

from cloudframe.common.utils import execute
from cloudframe.common.utils import generate_uuid

LOG = logging.getLogger(__name__)
REGISTRY_IP = '10.62.99.232'
REGISTRY_PORT = 5000


class Instance(object):
    def __init__(self, hosts, registry_ip=None, registry_port=None, ):
        if registry_ip is None:
            self.registry_ip = REGISTRY_IP
        else:
            self.registry_ip = registry_ip
        if registry_port is None:
            self.registry_port = REGISTRY_PORT
        else:
            self.registry_port = registry_port
        self.hosts = hosts

    def create(self, app_info, port):
        num = random.randint(0, len(self.hosts) - 1)
        host = self.hosts[num]
        image = self.registry_ip + ':' + str(self.registry_port) + '/' + app_info
        name = 'faas-worker-' + generate_uuid()
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
        LOG.debug('Create instance %(name)s, port %(port)d for image %(image)s on host %(host)s begin...',
                  {'name': name, 'port': port, 'image': image, 'host': host})

        # host
        host_str = host + ' ansible_ssh_pass=cloud ansible_become_pass=cloud'
        base_path = '/root/faas/worker-deploy/'
        hosts_file = base_path + 'hosts'
        fo = open(hosts_file, 'w')
        fo.write("[nodes]\n")
        fo.write(host_str)
        fo.flush()
        fo.close()

        # vars
        vars_file = base_path + 'vars.yml'
        for line in fileinput.input(vars_file, inplace=1):
            line = line.strip()
            strs = line.split(':')
            if 'deploy_image' in strs[0]:
                line = strs[0] + ': ' + image
            if 'deploy_name' in strs[0]:
                line = strs[0] + ': ' + name
            if 'host_port' in strs[0]:
                line = strs[0] + ': ' + str(port)
            print(line)

        # deploy
        ans_file = base_path + 'image_deploy.yml'
        execute('ansible-playbook', ans_file, '-i', hosts_file,
                check_exit_code=[0], run_as_root=True)

        LOG.debug('Create instance %(name)s end.', {'name': name})
