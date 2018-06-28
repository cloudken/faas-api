
from six.moves import http_client
import logging
import time

from cloudframe.common import exception
from cloudframe.common.config import HostConfig
from cloudframe.common.config import FaasConfig
from cloudframe.common.rpc import MyRPC
from cloudframe.driver.docker import Instance

LOG = logging.getLogger(__name__)

FUN_LIST = ['get', 'post', 'put', 'delete']
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
DEFAULT_HOST_GLOBAL = {
    'registry': '10.62.99.232:5000',
    'min_port': 30000,
    'max_port': 32000,
}
MAX_INS = 10

HOST_CONFIG = '/root/faas/config/docker_host.conf'
FAAS_CONFIG_PATH = '/root/faas/config/worker_config'


class FunctionInstances(object):
    def __init__(self):
        try:
            hc = HostConfig(HOST_CONFIG)
            rv = hc.get_host_info()
            self.hosts = rv[0]
            self.host_global = rv[1]
        except Exception as e:
            LOG.error('Read host_config(%(config)s) failed, error_info: %(error)s',
                      {'config': HOST_CONFIG, 'error': e})
            self.hosts = DEFAULT_HOSTS
            self.host_global = DEFAULT_HOST_GLOBAL
        self.driver = Instance(self.hosts, self.host_global['registry'])
        try:
            self.faas = {}
            fc = FaasConfig(FUN_LIST)
            fc.get_faas_from_path(FAAS_CONFIG_PATH, self.faas)
        except Exception as e:
            LOG.error('Read faas_config(%(config)s) failed, error_info: %(error)s',
                      {'config': FAAS_CONFIG_PATH, 'error': e})
            self.faas = DEFAULT_FAAS
        self.ins_list = {}
        self.port_idle_list = list(range(self.host_global['min_port'], self.host_global['max_port'], 1))
        self.port_busy_list = []
        LOG.debug('---- config info ----')
        LOG.debug('---- global: %(global)s', {'global': self.host_global})
        for host in self.hosts:
            LOG.debug('---- host: %(host)s', {'hosts': host})

    def _get_image(self, domain, version, res, opr, num):
        if num > MAX_INS:
            raise exception.ParameterInvalid(key='num', value=num)
        fun_name = str.lower(opr)
        if fun_name not in FUN_LIST:
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
        except Exception:
            raise exception.CreateError(object=image_name)

    def _check_ins(self, ins_data):
        rpc = MyRPC(ins_data)
        try:
            ack = rpc.call_heartbeat()
            if ack[0] is http_client.OK:
                return True
            else:
                LOG.error('Call heartbeat for [%(name)s, %(host_ip)s] failed, result_code is %(code)d.',
                          {'name': ins_data['name'], 'host_ip': ins_data['host_ip'], 'code': ack[0]})
                return False
        except Exception as e:
            LOG.error('Call heartbeat for [%(name)s, %(host_ip)s] failed, error_info: %(error)s',
                      {'name': ins_data['name'], 'host_ip': ins_data['host_ip'], 'error': e})
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
