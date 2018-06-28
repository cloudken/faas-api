
import os
import testtools

from cloudframe.common.config import HostConfig


class TestHostConfigServers(testtools.TestCase):
    def setUp(self):
        super(TestHostConfigServers, self).setUp()

    def test_host_config(self):
        # input
        config_file = 'host.conf'
        fo = open(config_file, 'w')
        fo.write("[default]\n")
        fo.write("registry = 10.62.99.232:5000\n")
        fo.write("min_port = 30000\n")
        fo.write("max_port = 32000\n")
        fo.write("host_num = 2\n")
        fo.write("\n")
        fo.write("[host1]\n")
        fo.write("host_ip = 192.168.1.1 \n")
        fo.write("ansible_user = cloud\n")
        fo.write("ansible_ssh_pass = cloud\n")
        fo.write("ansible_become_pass = cloud\n")
        fo.write("\n")
        fo.write("[host2]\n")
        fo.write("host_ip = 192.168.1.2 \n")
        fo.flush()
        fo.close()

        # testing
        hc = HostConfig(config_file)
        result = hc.get_host_info()
        os.remove(config_file)

        # output
        hosts = result[0]
        host_global = result[1]
        self.assertEqual(2, len(hosts))
        self.assertEqual('10.62.99.232:5000', host_global['registry'])
        self.assertEqual('192.168.1.1', hosts[0]['host_ip'])
        self.assertEqual('192.168.1.1 ansible_user=cloud ansible_ssh_pass=cloud ansible_become_pass=cloud', hosts[0]['host_par'])
        self.assertEqual('192.168.1.2', hosts[1]['host_ip'])
        self.assertEqual('192.168.1.2', hosts[1]['host_par'])
