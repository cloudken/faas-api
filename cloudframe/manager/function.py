
from cloudframe.common.rpc import MyRPC
from cloudframe.driver.docker import Instance

Fun_list = ['get', 'post', 'put', 'delete']
Resources = {
    'dom1_res1_v1': {'get': 'image1', 'post': 'image1', 'put': 'image1', 'delete': 'image1'},
    'dom1_res2_v1': {'get': 'image2', 'post': 'image3', 'put': 'image3', 'delete': 'image3'},
    'dom1_res2_v2': {'get': None, 'post': 'image4', 'put': None, 'delete': None},
}

MAX_INS = 10
MIN_PORT = 1000
MAX_PORT = 5000


class FunctionInstances(object):
    def __init__(self):
        self.ins_list = {}
        self.port_idle_list = range(MIN_PORT, MAX_PORT, 1)
        self.port_busy_list = []
        self.driver = Instance()

    def _get_image(self, domain, version, res, opr, num):
        if num > MAX_INS:
            return None
        res_name = domain + '_' + res + '_' + version
        if res_name not in Resources.key():
            return None
        fun_name = str.lower(opr)
        if fun_name not in Fun_list:
            return None
        return Resources[res_name][fun_name]

    def _launch_ins(self, image_name, num):
        port = self.port_idle_list.pop(len(self.port_idle_list) - 1)
        self.port_busy_list.append(port)
        ins_name = image_name + '_' + num
        ins_data = self.driver.create(image_name, port)
        self.ins_list[ins_name] = ins_data
        return ins_data

    def _check_ins(self, ins_data):
        rpc = MyRPC(ins_data)
        try:
            rpc.call_heartbeat()
            return True
        except:
            return False

    def _delete_ins(self, ins_name):
        port = self.ins_list[ins_name]['host_port']
        self.port_busy_list.remove(port)
        self.port_idle_list.append(port)
        self.ins_list.pop(ins_name)

    def get(self, domain, version, res, opr, num):
        image_name = self._get_image(domain, version, res, opr, num)
        if image_name is None:
            return None
        ins_name = image_name + '_' + num
        if ins_name not in self.ins_list.key():
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
        if image_name is None:
            return None
        try:
            ins_data = self._launch_ins(image_name, num)
            return ins_data
        except:
            return None
