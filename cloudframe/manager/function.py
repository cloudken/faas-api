
from six.moves import http_client
from datetime import datetime, timedelta
import logging
import time

from cloudframe.common import exception
from cloudframe.common.config import HostConfig
from cloudframe.common.config import FaasConfig
from cloudframe.common.job import Tasks
from cloudframe.common.rpc import MyRPC
from cloudframe.driver.docker_api import Instance

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

MAX_INS = 20

HOST_CONFIG = '/root/faas/config/docker_host.conf'
FAAS_CONFIG_PATH = '/root/faas/config/worker_config'

INS_STATUS_OK = 'ok'
INS_STATUS_INIT = 'initializing'
INS_STATUS_CHECKING = 'heartbeat checking'
INS_STATUS_ERROR = 'error'
INS_STATUS_END = 'end'
INS_STATUS_DYING = 'dying'


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
            fc.get_faas_list(self.faas, FAAS_CONFIG_PATH)
        except Exception as e:
            LOG.error('Read faas_config failed, error_info: %(error)s',
                      {'error': e})
            self.faas = DEFAULT_FAAS
        self.ins_list = {}
        self.finished_ins_list = []
        self.port_idle_list = list(range(self.host_global['min_port'], self.host_global['max_port'], 1))
        self.port_busy_list = []
        LOG.debug('---- config info ----')
        LOG.debug('---- global: %(global)s', {'global': self.host_global})
        for host in self.hosts:
            LOG.debug('---- host: %(host)s', {'host': host})

        delay = {
            'checking_time': 30,
            'aging_time': 300
        }
        item = [self._check_dead_worker, delay]
        Tasks.put_nowait(item)

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

    def _launch_ins(self, image_name, ins_data):
        try:
            port = self.port_idle_list.pop(len(self.port_idle_list) - 1)
            self.port_busy_list.append(port)
            ins_data['host_port'] = port
            self.driver.create(image_name, port, ins_data)
        except Exception as e:
            ins_data['status'] = INS_STATUS_ERROR
            LOG.error('Launch instance %(name)s failed, error_info: %(error)s',
                      {'name': image_name, 'error': e})

    def _check_ins(self, ins_data):
        try:
            rpc = MyRPC(ins_data)
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
        try:
            port = self.ins_list[ins_name]['host_port']
            self.port_busy_list.remove(port)
            self.port_idle_list.insert(0, port)
            ins_data = self.ins_list.pop(ins_name)
            ins_data['status'] = INS_STATUS_END
            ins_data['finished_at'] = datetime.now()
            self.finished_ins_list.append(ins_data)
            LOG.debug('FaaS-instance %(ins)s should be finished, info: %(info)s',
                      {'ins': ins_name, 'info': ins_data})
        except Exception as e:
            LOG.error('Delete instance %(name)s failed, error_info: %(error)s',
                      {'name': ins_name, 'error': e})

    def _destroy_ins(self, ins_data):
        try:
            LOG.debug('Destroy instance, info: %(info)s', {'info': ins_data})
            if ins_data['name'] != 'faas_no_name':
                self.driver.destroy(ins_data)
            self.finished_ins_list.remove(ins_data)
        except Exception as e:
            LOG.error('Destroy instance failed, error_info: %(error)s', {'error': e})

    def get(self, domain, version, res, opr, num):
        image_name = self._get_image(domain, version, res, opr, num)
        ins_name = image_name + '_' + str(num)
        if ins_name not in self.ins_list:
            return None
        else:
            ins_data = self.ins_list[ins_name]
            LOG.debug('FaaS-instance get, name: %(ins)s, info: %(info)s',
                      {'ins': ins_name, 'info': ins_data})
            if ins_data['status'] == INS_STATUS_OK:
                return ins_data
            elif ins_data['status'] == INS_STATUS_INIT or ins_data['status'] == INS_STATUS_CHECKING:
                for index in range(8):
                    time.sleep(index)
                    if ins_data['status'] == INS_STATUS_OK:
                        return ins_data
                self._delete_ins(ins_name)
                return None
            else:
                self._delete_ins(ins_name)
                return None

    def create(self, domain, version, res, opr, num):
        image_name = self._get_image(domain, version, res, opr, num)
        ins_name = image_name + '_' + str(num)
        LOG.debug('Create FaaS-instance %(ins)s begin...', {'ins': ins_name})
        ins_data = {
            'ins_name': ins_name,
            'name': 'faas_no_name',
            'created_at': datetime.now(),
            'status': INS_STATUS_INIT
        }
        self.ins_list[ins_name] = ins_data
        self._launch_ins(image_name, ins_data)
        if ins_data['status'] == INS_STATUS_ERROR:
            self._delete_ins(ins_name)
            raise exception.CreateError(object=image_name)
        ins_data['status'] = INS_STATUS_CHECKING
        for index in range(5):
            if self._check_ins(ins_data):
                ins_data['status'] = INS_STATUS_OK
                ins_data['started_at'] = datetime.now()
                LOG.debug('Create FaaS-instance %(ins)s success, info: %(info)s',
                          {'ins': ins_name, 'info': ins_data})
                item = [self._check_worker_status, ins_name]
                Tasks.put_nowait(item)
                return ins_data
            time.sleep(index)
        self._delete_ins(ins_name)
        raise exception.CreateError(object=image_name)

    def set_worker_dying(self, ins_data):
        ins_data['status'] = INS_STATUS_DYING
        LOG.debug('FaaS-instance set dying, info: %(info)s', {'info': ins_data})

    def get_worker_by_name(self, ins_name, ins_id):
        if ins_name not in self.ins_list:
            raise exception.ObjectNotFound(object=ins_name)
        ins_data = self.ins_list[ins_name]
        if ins_data['ins_name'] != ins_name or ins_data['id'] != ins_id:
            LOG.error('get_worker_by_name: par is illegal; input: %(i_name)s, %(i_id)s; local: %(l_name)s, %(l_id)s',
                      {'i_name': ins_name, 'i_id': ins_id, 'l_name': ins_data['ins_name'], 'l_id': ins_data['id']})
            raise exception.ObjectNotFound(object=ins_name)
        return ins_data

    def _check_worker_status(self, ins_name):
        LOG.debug('Checking worker %(name)s status...', {'name': ins_name})
        if ins_name not in self.ins_list:
            return
        ins_data = self.ins_list[ins_name]
        if ins_data['status'] == INS_STATUS_OK:
            if self._check_ins(ins_data):
                time.sleep(5)
                item = [self._check_worker_status, ins_name]
                Tasks.put_nowait(item)
            else:
                ins_data['status'] = INS_STATUS_DYING
                item = [self._check_worker_status, ins_name]
                Tasks.put_nowait(item)
        elif ins_data['status'] in [INS_STATUS_INIT, INS_STATUS_CHECKING]:
            time.sleep(5)
            item = [self._check_worker_status, ins_name]
            Tasks.put_nowait(item)
        else:
            self._delete_ins(ins_name)

    def _check_dead_worker(self, delay):
        while True:
            time.sleep(delay['checking_time'])
            LOG.debug('Checking dead worker...')
            for ins in self.finished_ins_list:
                current = datetime.now()
                end = ins['finished_at']
                interval = delay['aging_time']
                if (current - end) > timedelta(seconds=interval):
                    item = [self._destroy_ins, ins]
                    Tasks.put_nowait(item)

    def put_faas(self, faas_input):
        LOG.debug('Updating FaaS info, input: %(input)s', {'input': faas_input})
        try:
            if not self._check_faasinfo(faas_input):
                raise exception.FaaSInfoInvalid()
            fc = FaasConfig(FUN_LIST)
            fc.load_and_save_faas(faas_input, self.faas, FAAS_CONFIG_PATH)
        except Exception as e:
            LOG.error('Updating FaaS info failed, error_info: %(error)s', {'error': e})
            raise exception.FaaSInfoInvalid()

    def _check_faasinfo(self, faas_input):
        return True
