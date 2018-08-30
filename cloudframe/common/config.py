
try:
    import configparser as ConfigParser
except Exception:
    import ConfigParser

import os
import yaml


class HostConfig(object):
    def __init__(self, filename):
        if not os.path.exists(filename):
            raise Exception('File not exist.')
        self.filename = filename
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.filename)

    def _get_hostnum(self):
        return self.config.getint('default', 'host_num')

    def _get_hostinfo(self, host_id):
        host = 'host' + str(host_id)
        section = self.config.items(host)
        host_info = {}
        host_info['host_ip'] = self.config.get(host, 'host_ip')
        host_info['host_par'] = host_info['host_ip']
        for item in section:
            if item[0] != 'host_ip':
                host_info['host_par'] += ' ' + item[0] + '=' + item[1]
        return host_info

    def get_host_info(self):
        host_global = {}
        host_global['registry'] = self.config.get('default', 'registry')
        host_global['min_port'] = self.config.getint('default', 'min_port')
        host_global['max_port'] = self.config.getint('default', 'max_port')

        num = self._get_hostnum()
        hosts = []
        for index in range(num):
            hosts.append(self._get_hostinfo(index + 1))
        return hosts, host_global


class FaasConfig(object):
    def __init__(self, fun_list):
        self.fun_list = fun_list

    def get_faas_list(self, faas, path):
        if not os.path.exists(path):
            raise Exception('Path not exist.')
        for dirpath, dirnames, filenames in os.walk(path):
            dirnames = dirnames
            for name in filenames:
                filename = os.path.join(dirpath, name)
                ext = os.path.splitext(filename)[1]
                if ext == '.yaml':
                    self.get_faas_from_file(filename, faas)

    def get_faas_from_file(self, filename, faas):
        fo = open(filename, 'r')
        faas_input = yaml.load(fo)
        fo.close()
        self.get_faas(faas_input, faas)

    def get_faas(self, faas_input, faas):
        for resource in faas_input['resources']:
            key = faas_input['domain'] + '_' + resource['name'] + '_' + resource['version']
            for fun in resource['functions']:
                if fun['name'] in self.fun_list:
                    fun_key = key + '_' + fun['name']
                    faas[fun_key] = faas_input['image_name'] + ':' + faas_input['image_tag']

    def load_and_save_faas(self, faas_input, faas, path):
        self.get_faas(faas_input, faas)
        if not os.path.exists(path):
            os.makedirs(path)
        filename = faas_input['image_name'] + ':' + faas_input['image_tag'] + '.yaml'
        faas_file = path + '/' + filename
        fo = open(faas_file, 'w')
        yaml.safe_dump(faas_input, fo)
        fo.close()
