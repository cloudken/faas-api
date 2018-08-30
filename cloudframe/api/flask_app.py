
from flask import abort
from flask import Flask
from flask import jsonify
from flask import make_response
from flask import request
import logging
import os
from six.moves import http_client
from werkzeug.contrib.fixers import ProxyFix

# from cloudframe.common.utils import generate_uuid
from cloudframe.common import exception
from cloudframe.manager.manager import FunctionManager


os.environ.setdefault('LOG_LEVEL', 'DEBUG')
loglevel_map = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARN': logging.WARN,
    'ERROR': logging.ERROR,
}
logging.basicConfig(
    level=loglevel_map[os.environ['LOG_LEVEL']],
    format='%(asctime)s.%(msecs)03d %(filename)s[line:%(lineno)d]'
           ' %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='/var/log/cloudframe/faas-api.log',
    filemode='a')
LOG = logging.getLogger(__name__)
app = Flask(__name__)
Manager = FunctionManager()


@app.route('/<domain_name>/<ver>/tenants/<tenant_id>/<res_name>',
           methods=['GET'])
def get_list(domain_name=None, ver=None, tenant_id=None, res_name=None):
    try:
        results = Manager.function_call(domain_name, ver, tenant_id, res_name, 'get')
        return make_response(results[1], results[0])
    except exception.CloudframeException as e:
        LOG.error('GET REST API[%(domain)s, %(ver)s, %(tenant_id)s, %(res)s] failed, error info: %(error)s',
                  {'domain': domain_name, 'ver': ver, 'tenant_id': tenant_id, 'res': res_name, 'error': e.message})
        return make_response(jsonify({'error': e.message}),
                             e.code)


@app.route('/<domain_name>/<ver>/tenants/<tenant_id>/<res_name>/<uuid>',
           methods=['GET'])
def get_detail(domain_name=None, ver=None, tenant_id=None,
               res_name=None, uuid=None):
    try:
        results = Manager.function_call(domain_name, ver, tenant_id, res_name, 'get', res_id=uuid)
        return make_response(results[1], results[0])
    except exception.CloudframeException as e:
        LOG.error('GET REST API[%(domain)s, %(ver)s, %(tenant_id)s, %(res)s, %(uuid)s] failed, error info: %(error)s',
                  {'domain': domain_name, 'ver': ver, 'tenant_id': tenant_id, 'res': res_name, 'uuid': uuid, 'error': e.message})
        return make_response(jsonify({'error': e.message}),
                             e.code)


@app.route('/<domain_name>/<ver>/tenants/<tenant_id>/<res_name>',
           methods=['POST'])
def post(domain_name=None, ver=None, tenant_id=None, res_name=None):
    try:
        # uuid = generate_uuid()
        results = Manager.function_call(domain_name, ver, tenant_id, res_name, 'post', request.json)
        return make_response(results[1], results[0])
    except exception.CloudframeException as e:
        LOG.error('POST REST API[%(domain)s, %(ver)s, %(tenant_id)s, %(res)s] failed, error info: %(error)s',
                  {'domain': domain_name, 'ver': ver, 'tenant_id': tenant_id, 'res': res_name, 'error': e.message})
        return make_response(jsonify({'error': e.message}),
                             e.code)


@app.route('/<domain_name>/<ver>/tenants/<tenant_id>/<res_name>/<uuid>',
           methods=['PUT'])
def put(domain_name=None, ver=None, tenant_id=None,
        res_name=None, uuid=None):
    if not request.json:
        abort(http_client.BAD_REQUEST)
    try:
        results = Manager.function_call(domain_name, ver, tenant_id, res_name, 'put', request.json, res_id=uuid)
        return make_response(results[1], results[0])
    except exception.CloudframeException as e:
        LOG.error('PUT REST API[%(domain)s, %(ver)s, %(tenant_id)s, %(res)s, %(uuid)s] failed, error info: %(error)s',
                  {'domain': domain_name, 'ver': ver, 'tenant_id': tenant_id, 'res': res_name, 'uuid': uuid, 'error': e.message})
        return make_response(jsonify({'error': e.message}),
                             e.code)


@app.route('/<domain_name>/<ver>/tenants/<tenant_id>/<res_name>/<uuid>',
           methods=['DELETE'])
def delete(domain_name=None, ver=None, tenant_id=None,
           res_name=None, uuid=None):
    try:
        results = Manager.function_call(domain_name, ver, tenant_id, res_name, 'delete', res_id=uuid)
        return make_response(results[1], results[0])
    except exception.CloudframeException as e:
        LOG.error('DELETE REST API[%(domain)s, %(ver)s, %(tenant_id)s, %(res)s, %(uuid)s] failed, error info: %(error)s',
                  {'domain': domain_name, 'ver': ver, 'tenant_id': tenant_id, 'res': res_name, 'uuid': uuid, 'error': e.message})
        return make_response(jsonify({'error': e.message}),
                             e.code)


@app.route('/serverless/<ver>/faas', methods=['PUT'])
def put_faas(ver=None):
    try:
        if not request.json:
            abort(http_client.BAD_REQUEST)
        req = request.json
        Manager.put_faasinfo(req)
        result = {'result': 'ok'}
        return make_response(jsonify(result), http_client.OK)
    except exception.CloudframeException as e:
        LOG.error('PUT FaaS failed, error info: %(error)s', {'error': e.message})
        return make_response(jsonify({'error': e.message}),
                             e.code)


app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
    app.run()
