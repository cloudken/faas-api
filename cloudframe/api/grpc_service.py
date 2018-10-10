
import logging
import os
from six.moves import http_client

from cloudframe.manager.manager import FunctionManager
from cloudframe.protos import worker_pb2
from cloudframe.protos import worker_pb2_grpc

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
    filename='/var/log/cloudframe/faas-manager.log',
    filemode='a')
LOG = logging.getLogger(__name__)
Manager = FunctionManager()
FAAS_DYING = 1033


class WorkerServicer(worker_pb2_grpc.GreeterServicer):

    def Call(self, request, context):
        try:
            LOG.debug('Worker call begin, domain %(domain)s, resource %(res)s, version %(ver)s, operation %(opr)s.',
                      {'domain': request.domain, 'res': request.resource, 'ver': request.version, 'opr': request.opr})
            domain = request.domain.encode('utf-8')
            version = request.version.encode('utf-8')
            resource = request.resource.encode('utf-8')
            opr = request.opr.encode('utf-8')
            wk_info = Manager.get_worker(domain, version, resource, opr)
            LOG.debug('Worker call end, name %(name)s, id %(id)s, host_ip %(host_ip)s, host_port %(host_port)s.',
                      {'name': wk_info['ins_name'], 'id': wk_info['id'], 'host_ip': wk_info['host_ip'], 'host_port': wk_info['host_port']})
            return worker_pb2.WorkerReply(
                name=wk_info['ins_name'],
                id=wk_info['id'],
                host_ip=wk_info['host_ip'],
                host_port=wk_info['host_port'],
                return_code=http_client.OK)
        except Exception as e:
            LOG.error('Worker Call failed, error_info: %(error)s', {'error': e})
            return worker_pb2.WorkerReply(return_code=http_client.INTERNAL_SERVER_ERROR)

    def SetStatus(self, request, context):
        try:
            LOG.debug('Worker SetStatus begin, name %(name)s, id %(id)s, status %(status)d.',
                      {'name': request.name, 'id': request.id, 'status': request.status})
            name = request.name.encode('utf-8')
            worker_id = request.id.encode('utf-8')
            if request.status == FAAS_DYING:
                Manager.set_worker_dying(name, worker_id)
                LOG.debug('Worker SetStatus end.')
                return worker_pb2.CommonReply(return_code=http_client.OK)
            else:
                LOG.error('Worker status %(status)d is illegal.', {'status': request.status})
                return worker_pb2.CommonReply(return_code=http_client.FORBIDDEN)
        except Exception as e:
            LOG.error('Worker SetStatus failed, error_info: %(error)s', {'error': e})
            return worker_pb2.CommonReply(return_code=http_client.INTERNAL_SERVER_ERROR)
