
import fileinput
import logging
import os
import random
import shutil

from cloudframe.common.utils import execute
from cloudframe.common.utils import generate_uuid

LOG = logging.getLogger(__name__)

HOST_OK = 'host ok'
HOST_ERROR = 'host error'


class Instance(object):
    def __init__(self, hosts, registry_info):
        self.registry = registry_info
        self.hosts_ok = []
        self.hosts_error = []
        for host in hosts:
            try:
                self._deploy_host(host)
                self.hosts_ok.append(host)
            except Exception as e:
                LOG.error('Deploy host_%(host)s failed, error_info: %(error)s',
                          {'host': host['host_ip'], 'error': e})
                self.hosts_error.append(host)

    def _deploy_host(self, host):
        LOG.debug('Deploy host %(host)s begin...', {'host': host['host_ip']})

        # host
        host_par = host['host_par']
        base_path = '/root/faas/deploy/'
        hosts_file = base_path + 'hosts'
        fo = open(hosts_file, 'w')
        fo.write("[nodes]\n")
        fo.write(host_par)
        fo.flush()
        fo.close()

        # deploy
        ans_file = base_path + 'host_deploy.yml'
        execute('ansible-playbook', ans_file, '-i', hosts_file,
                check_exit_code=[0], run_as_root=True)

        LOG.debug('Deploy host %(host)s end.', {'host': host['host_ip']})

    def create(self, app_info, port, ins_data):
        num = random.randint(0, len(self.hosts_ok) - 1)
        host = self.hosts_ok[num]
        image = self.registry + '/' + app_info
        name = 'faas-worker-' + generate_uuid()
        self._create_instance(name, image, host, port)
        ins_data['name'] = name
        ins_data['image'] = image
        ins_data['host_ip'] = host['host_ip']

    def _create_instance(self, name, image, host, port):
        LOG.debug('Create instance %(name)s, port %(port)d for image %(image)s on host %(host)s begin...',
                  {'name': name, 'port': port, 'image': image, 'host': host['host_ip']})

        # mkdir and copy files
        src_path = '/root/faas/deploy/'
        base_path = src_path + name + '/'
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        src_file = src_path + 'vars.yml'
        shutil.copy(src_file, base_path)
        src_file = src_path + 'image_deploy.yml'
        shutil.copy(src_file, base_path)

        # host
        # host_str = host + ' ansible_ssh_pass=cloud ansible_become_pass=cloud'
        host_par = host['host_par']
        hosts_file = base_path + 'hosts'
        fo = open(hosts_file, 'w')
        fo.write("[nodes]\n")
        fo.write(host_par)
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

        # remove dir
        shutil.rmtree(base_path)
        LOG.debug('Create instance %(name)s end.', {'name': name})
