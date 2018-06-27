
import ConfigParser
import os
import yaml


class HostConfig(object):
    def __init__(self, filename):
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

    def get_hosts(self):
        num = self._get_hostnum()
        hosts = []
        for index in range(num):
            hosts.append(self._get_hostinfo(index + 1))
        return hosts


class FaasConfig(object):
    def __init__(self, fun_list):
        self.fun_list = fun_list

    def get_faas_from_path(self, path, faas):
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
        return self.get_faas(faas_input, faas)

    def get_faas(self, faas_input, faas):
        for resource in faas_input['resources']:
            key = faas_input['domain'] + '_' + resource['name'] + '_' + resource['version']
            for fun in resource['functions']:
                if fun['name'] in self.fun_list:
                    fun_key = key + '_' + fun['name']
                    faas[fun_key] = faas_input['image_name']
