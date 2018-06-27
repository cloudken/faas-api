
import exceptions
from six.moves import http_client
import logging
import time

from cloudframe.common import exception
from cloudframe.common.config import HostConfig
from cloudframe.common.config import FaasConfig
from cloudframe.common.rpc import MyRPC
from cloudframe.driver.docker import Instance

LOG = logging.getLogger(__name__)

Fun_list = ['get', 'post', 'put', 'delete']
DEFAULT_FAAS = {
    'dom1_res01_v1_get': 'faas-worker:20180620',
    'dom1_res01_v1_post': 'faas-worker:20180620',
    'dom1_res01_v1_put': 'faas-worker:20180620',
    'dom1_res01_v1_delete': 'faas-worker:20180620',
    'dom1_res02_v1_get': 'image2',
    'dom1_res02_v2_get': None,
}
DEFAULT_HOSTS = [
    {'host_ip': '192.168.1.1', 'host_par': '192.168.1.1'}
]
DEFAULT_REGISTRY = '10.62.99.232:5000'

MAX_INS = 5
MIN_PORT = 30000
MAX_PORT = 32000
HOST_CONFIG = '/root/faas/config/docker_host.conf'
FAAS_CONFIG_PATH = '/root/faas/worker_config'


class FunctionInstances(object):
    def __init__(self):
        self.ins_list = {}
        self.port_idle_list = range(MIN_PORT, MAX_PORT, 1)
        self.port_busy_list = []
        try:
            hc = HostConfig(HOST_CONFIG)
            rv = hc.get_hosts()
            self.hosts = rv[0]
            self.registry = rv[1]
        except exceptions.Exception as e:
            LOG.error('Read host_config(%(config)s) failed, error_info: %(error)s',
                      {'config': HOST_CONFIG, 'error': e.message})
            self.hosts = DEFAULT_HOSTS
            self.registry = DEFAULT_REGISTRY
        self.driver = Instance(self.hosts, self.registry)
        try:
            self.faas = {}
            fc = FaasConfig()
            fc.get_faas_from_path(FAAS_CONFIG_PATH, self.faas)
        except exceptions.Exception as e:
            LOG.error('Read faas_config(%(config)s) failed, error_info: %(error)s',
                      {'config': FAAS_CONFIG_PATH, 'error': e.message})
            self.faas = DEFAULT_FAAS
        LOG.debug('---- config info ----')
        LOG.debug('---- registry: %(registry)s', {'registry': self.registry})
        LOG.debug('---- hosts: %(hosts)s', {'hosts': self.hosts})

    def _get_image(self, domain, version, res, opr, num):
        if num > MAX_INS:
            raise exception.ParameterInvalid(key='num', value=num)
        fun_name = str.lower(opr)
        if fun_name not in Fun_list:
            raise exception.ParameterInvalid(key='function', value=fun_name)
        res_name = domain + '_' + res + '_' + version + '_' + fun_name
        if res_name not in self.faas:
            raise exception.ObjectNotFound(object=res_name)

        image_info = self.faas[res_name]
        if image_info is None:
            raise exception.ImageNotFound(res=res_name, opr=fun_name)
        return image_info

    def _launch_ins(self, image_name):
        try:
            port = self.port_idle_list.pop(len(self.port_idle_list) - 1)
            self.port_busy_list.append(port)
            ins_data = self.driver.create(image_name, port)
            return ins_data
        except:
            raise exception.CreateError(object=image_name)

    def _check_ins(self, ins_data):
        rpc = MyRPC(ins_data)
        try:
            ack = rpc.call_heartbeat()
            if ack[0] is http_client.OK:
                return True
            else:
                return False
        except:
            return False

    def _delete_ins(self, ins_name):
        port = self.ins_list[ins_name]['host_port']
        self.port_busy_list.remove(port)
        self.port_idle_list.append(port)
        self.ins_list.pop(ins_name)

    def get(self, domain, version, res, opr, num):
        image_name = self._get_image(domain, version, res, opr, num)
        ins_name = image_name + '_' + str(num)
        if ins_name not in self.ins_list:
            return None
        else:
            ins_data = self.ins_list[ins_name]
            if not self._check_ins(ins_data):
                self._delete_ins(ins_name)
                return None
            else:
                return ins_data

    def create(self, domain, version, res, opr, num):
        image_name = self._get_image(domain, version, res, opr, num)
        ins_data = self._launch_ins(image_name)
        for index in range(5):
            if self._check_ins(ins_data):
                ins_name = image_name + '_' + str(num)
                self.ins_list[ins_name] = ins_data
                return ins_data
            time.sleep(index)
        raise exception.CreateError(object=image_name)
