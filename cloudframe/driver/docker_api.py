
import logging
import random

from cloudframe.common.http_rpc import HRPC
from cloudframe.common.utils import execute
from cloudframe.common.utils import generate_uuid

LOG = logging.getLogger(__name__)

HOST_OK = 'host ok'
HOST_ERROR = 'host error'

WORKER_LOG_LEVEL = 'DEBUG'
WORKER_LIFE_CYCLE = 60


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
        ins_id = self._create_instance(name, image, host, port)
        ins_data['name'] = name
        ins_data['id'] = ins_id
        ins_data['image'] = image
        ins_data['host_ip'] = host['host_ip']

    def _create_instance(self, name, image, host, port):
        LOG.debug('Create instance %(name)s, port %(port)d for image %(image)s on host %(host)s begin...',
                  {'name': name, 'port': port, 'image': image, 'host': host['host_ip']})
        host_api = host['host_api']

        # Create container
        container_url = '/v1.24/containers/create'
        port_str = '50051/tcp'
        env_log = 'LOG_LEVEL=' + WORKER_LOG_LEVEL
        env_life = 'LIFE_CYCLE=' + str(WORKER_LIFE_CYCLE)
        volume_usr = '/root/faas/cf-base/usr:/usr:ro'
        volume_log = '/root/faas/logs/' + name + ':/var/log/cloudframe'
        req = {
            'Image': image,
            'Env': [env_log, env_life],
            'ExposedPorts': {port_str: {}},
            'HostConfig': {
                'Binds': [volume_usr, volume_log],
                'PortBindings': {port_str: [{'HostPort': str(port)}]},
            }
        }
        try:
            rpc = HRPC(host_api, container_url)
            ack = rpc.post(None, req)
            ins_id = ack['Id']
        except Exception:
            # if create error, pull image and create again.
            url = '/v1.24/images/create?fromImage=' + image
            rpc = HRPC(host_api, url)
            rpc.post_no_ack(None, None)
            rpc = HRPC(host_api, container_url)
            ack = rpc.post(None, req)
            ins_id = ack['Id']

        # Start container
        url = '/v1.24/containers/' + ins_id + '/start'
        rpc = HRPC(host_api, url)
        rpc.post_no_ack()

        LOG.debug('Create instance %(name)s end, id is %(id)s.', {'name': name, 'id': ins_id})
        return ins_id

    def destroy(self, ins_data):
        ins_id = ins_data['id']
        host_ip = ins_data['host_ip']
        LOG.debug('Destroy instance %(name)s on host %(host)s begin...',
                  {'name': ins_id, 'host': host_ip})
        host_api = ''
        for host in self.hosts_ok:
            if host_ip == host['host_ip']:
                host_api = host['host_api']
                break
        url = '/v1.24/containers/'
        rpc = HRPC(host_api, url)
        rpc.delete(ins_id)
        LOG.debug('Delete instance %(name)s end.', {'name': ins_id})
