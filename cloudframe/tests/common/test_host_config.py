
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
        hosts = hc.get_hosts()
        os.remove(config_file)

        # output
        self.assertEqual(2, len(hosts))
        self.assertEqual('192.168.1.1', hosts[0]['host_ip'])
        self.assertEqual('192.168.1.1 ansible_user=cloud ansible_ssh_pass=cloud ansible_become_pass=cloud', hosts[0]['host_par'])
        self.assertEqual('192.168.1.2', hosts[1]['host_ip'])
        self.assertEqual('192.168.1.2', hosts[1]['host_par'])
