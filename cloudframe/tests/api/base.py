
import testtools

from cloudframe.api import flask_app as my_app


class ApiTestCase(testtools.TestCase):
    my_app.app.config['Testing'] = True
    app = my_app.app.test_client()

    def setUp(self):
        super(ApiTestCase, self).setUp()
