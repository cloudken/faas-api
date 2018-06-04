
from flask import abort
from flask import Flask
from flask import jsonify
from flask import make_response
from flask import request
import logging
from six.moves import http_client
from werkzeug.contrib.fixers import ProxyFix

from cloudframe.common.utils import get_resource
from cloudframe.common.utils import generate_uuid
from cloudframe.manager.manager import FunctionManager

LOG = logging.getLogger(__name__)
app = Flask(__name__)
Manager = FunctionManager()


@app.route('/<domain_name>/<ver>/tenants/<tenant_id>/<res_name>',
           methods=['GET'])
def get_list(domain_name=None, ver=None, tenant_id=None, res_name=None):
    try:
        results = Manager.function_call(domain_name, ver, tenant_id, res_name, 'get')
        return make_response(jsonify(results[1]), results[0])
    except Exception as e:
        return make_response(jsonify({'error': e.message}),
                             http_client.INTERNAL_SERVER_ERROR)


@app.route('/<domain_name>/<ver>/tenants/<tenant_id>/<res_name>/<uuid>',
           methods=['GET'])
def get_detail(domain_name=None, ver=None, tenant_id=None,
               res_name=None, uuid=None):
    try:
        results = Manager.function_call(domain_name, ver, tenant_id, res_name, 'get', res_id=uuid)
        return make_response(jsonify(results[1]), results[0])
    except Exception as e:
        return make_response(jsonify({'error': e.message}),
                             http_client.INTERNAL_SERVER_ERROR)


@app.route('/<domain_name>/<ver>/tenants/<tenant_id>/<res_name>',
           methods=['POST'])
def post(domain_name=None, ver=None, tenant_id=None, res_name=None):
    try:
        uuid = generate_uuid()
        results = Manager.function_call(domain_name, ver, tenant_id, res_name, 'post', req=request.json, res_id=uuid)
        return make_response(jsonify(results[1]), results[0])
    except Exception as e:
        return make_response(jsonify({'error': e.message}),
                             http_client.INTERNAL_SERVER_ERROR)


@app.route('/<domain_name>/<ver>/tenants/<tenant_id>/<res_name>/<uuid>',
           methods=['PUT'])
def put(domain_name=None, ver=None, tenant_id=None,
        res_name=None, uuid=None):
    if not request.json:
        abort(http_client.BAD_REQUEST)
    try:
        results = Manager.function_call(domain_name, ver, tenant_id, res_name, 'put', req=request.json, res_id=uuid)
        return make_response(jsonify(results[1]), results[0])
    except Exception as e:
        return make_response(jsonify({'error': e.message}),
                             http_client.INTERNAL_SERVER_ERROR)


@app.route('/<domain_name>/<ver>/tenants/<tenant_id>/<res_name>/<uuid>',
           methods=['DELETE'])
def delete(domain_name=None, ver=None, tenant_id=None,
           res_name=None, uuid=None):
    try:
        results = Manager.function_call(domain_name, ver, tenant_id, res_name, 'delete', res_id=uuid)
        return make_response(jsonify(results[1]), results[0])
    except Exception as e:
        return make_response(jsonify({'error': e.message}),
                             http_client.INTERNAL_SERVER_ERROR)


app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
    app.run()
