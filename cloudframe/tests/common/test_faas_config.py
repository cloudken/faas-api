
import os
import shutil
import testtools
import yaml

from cloudframe.common.config import FaasConfig
from cloudframe.manager.function import FUN_LIST


class TestFaasConfigServers(testtools.TestCase):
    def setUp(self):
        super(TestFaasConfigServers, self).setUp()

    def test_faas_config(self):
        # input
        worker01_desc = {
            'image_name': 'abc',
            'image_tag': 'v1.0',
            'domain': 'dom1',
            'resources': [
                {
                    'name': 'res01',
                    'version': 'v1',
                    'functions': [
                        {'name': 'get'},
                        {'name': 'post'},
                        {'name': 'put'},
                        {'name': 'delete'}
                    ]
                },
                {
                    'name': 'res01',
                    'version': 'v2',
                    'functions': [
                        {'name': 'get'}
                    ]
                },
                {
                    'name': 'res02',
                    'version': 'v1',
                    'functions': [
                        {'name': 'get'},
                        {'name': 'post'},
                        {'name': 'delete'}
                    ]
                }
            ]
        }
        worker02_desc = {
            'image_name': 'def',
            'image_tag': 'v1.0',
            'domain': 'dom2',
            'resources': [
                {
                    'name': 'res_aa',
                    'version': 'v1',
                    'functions': [
                        {'name': 'get'},
                        {'name': 'post'},
                        {'name': 'put'},
                        {'name': 'delete'}
                    ]
                }
            ]
        }

        path = 'temp'
        if not os.path.exists(path):
            os.makedirs(path)
        fo = open('temp/worker01.yaml', 'w')
        yaml.dump(worker01_desc, fo)
        fo.close()
        fo = open('temp/worker02.yaml', 'w')
        yaml.dump(worker02_desc, fo)
        fo.close()

        # testing
        fc = FaasConfig(FUN_LIST)
        faas = {}
        fc.get_faas_list(faas, path)
        shutil.rmtree(path)

        # output
        self.assertEqual(12, len(faas))
        self.assertEqual('abc:v1.0', faas['dom1_res01_v1_get'])
        self.assertEqual('abc:v1.0', faas['dom1_res02_v1_post'])
        self.assertEqual('def:v1.0', faas['dom2_res_aa_v1_delete'])
