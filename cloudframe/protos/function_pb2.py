# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: function.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='function.proto',
  package='FunctionData',
  syntax='proto3',
  serialized_pb=_b('\n\x0e\x66unction.proto\x12\x0c\x46unctionData\"n\n\x0f\x46unctionRequest\x12\x0b\n\x03opr\x18\x01 \x01(\t\x12\x0e\n\x06tenant\x18\x02 \x01(\t\x12\x0f\n\x07version\x18\x03 \x01(\t\x12\x10\n\x08resource\x18\x04 \x01(\t\x12\x0e\n\x06res_id\x18\x05 \x01(\t\x12\x0b\n\x03req\x18\x06 \x01(\t\"1\n\rFunctionReply\x12\x13\n\x0breturn_code\x18\x01 \x01(\t\x12\x0b\n\x03\x61\x63k\x18\x02 \x01(\t2O\n\x07Greeter\x12\x44\n\x04\x43\x61ll\x12\x1d.FunctionData.FunctionRequest\x1a\x1b.FunctionData.FunctionReply\"\x00\x62\x06proto3')
)




_FUNCTIONREQUEST = _descriptor.Descriptor(
  name='FunctionRequest',
  full_name='FunctionData.FunctionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='opr', full_name='FunctionData.FunctionRequest.opr', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='tenant', full_name='FunctionData.FunctionRequest.tenant', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='version', full_name='FunctionData.FunctionRequest.version', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='resource', full_name='FunctionData.FunctionRequest.resource', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='res_id', full_name='FunctionData.FunctionRequest.res_id', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='req', full_name='FunctionData.FunctionRequest.req', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=32,
  serialized_end=142,
)


_FUNCTIONREPLY = _descriptor.Descriptor(
  name='FunctionReply',
  full_name='FunctionData.FunctionReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='return_code', full_name='FunctionData.FunctionReply.return_code', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ack', full_name='FunctionData.FunctionReply.ack', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=144,
  serialized_end=193,
)

DESCRIPTOR.message_types_by_name['FunctionRequest'] = _FUNCTIONREQUEST
DESCRIPTOR.message_types_by_name['FunctionReply'] = _FUNCTIONREPLY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

FunctionRequest = _reflection.GeneratedProtocolMessageType('FunctionRequest', (_message.Message,), dict(
  DESCRIPTOR = _FUNCTIONREQUEST,
  __module__ = 'function_pb2'
  # @@protoc_insertion_point(class_scope:FunctionData.FunctionRequest)
  ))
_sym_db.RegisterMessage(FunctionRequest)

FunctionReply = _reflection.GeneratedProtocolMessageType('FunctionReply', (_message.Message,), dict(
  DESCRIPTOR = _FUNCTIONREPLY,
  __module__ = 'function_pb2'
  # @@protoc_insertion_point(class_scope:FunctionData.FunctionReply)
  ))
_sym_db.RegisterMessage(FunctionReply)



_GREETER = _descriptor.ServiceDescriptor(
  name='Greeter',
  full_name='FunctionData.Greeter',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=195,
  serialized_end=274,
  methods=[
  _descriptor.MethodDescriptor(
    name='Call',
    full_name='FunctionData.Greeter.Call',
    index=0,
    containing_service=None,
    input_type=_FUNCTIONREQUEST,
    output_type=_FUNCTIONREPLY,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_GREETER)

DESCRIPTOR.services_by_name['Greeter'] = _GREETER

try:
  # THESE ELEMENTS WILL BE DEPRECATED.
  # Please use the generated *_pb2_grpc.py files instead.
  import grpc
  from grpc.beta import implementations as beta_implementations
  from grpc.beta import interfaces as beta_interfaces
  from grpc.framework.common import cardinality
  from grpc.framework.interfaces.face import utilities as face_utilities


  class GreeterStub(object):
    # missing associated documentation comment in .proto file
    pass

    def __init__(self, channel):
      """Constructor.

      Args:
        channel: A grpc.Channel.
      """
      self.Call = channel.unary_unary(
          '/FunctionData.Greeter/Call',
          request_serializer=FunctionRequest.SerializeToString,
          response_deserializer=FunctionReply.FromString,
          )


  class GreeterServicer(object):
    # missing associated documentation comment in .proto file
    pass

    def Call(self, request, context):
      # missing associated documentation comment in .proto file
      pass
      context.set_code(grpc.StatusCode.UNIMPLEMENTED)
      context.set_details('Method not implemented!')
      raise NotImplementedError('Method not implemented!')


  def add_GreeterServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'Call': grpc.unary_unary_rpc_method_handler(
            servicer.Call,
            request_deserializer=FunctionRequest.FromString,
            response_serializer=FunctionReply.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'FunctionData.Greeter', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


  class BetaGreeterServicer(object):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This class was generated
    only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0."""
    # missing associated documentation comment in .proto file
    pass
    def Call(self, request, context):
      # missing associated documentation comment in .proto file
      pass
      context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)


  class BetaGreeterStub(object):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This class was generated
    only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0."""
    # missing associated documentation comment in .proto file
    pass
    def Call(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
      # missing associated documentation comment in .proto file
      pass
      raise NotImplementedError()
    Call.future = None


  def beta_create_Greeter_server(servicer, pool=None, pool_size=None, default_timeout=None, maximum_timeout=None):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This function was
    generated only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0"""
    request_deserializers = {
      ('FunctionData.Greeter', 'Call'): FunctionRequest.FromString,
    }
    response_serializers = {
      ('FunctionData.Greeter', 'Call'): FunctionReply.SerializeToString,
    }
    method_implementations = {
      ('FunctionData.Greeter', 'Call'): face_utilities.unary_unary_inline(servicer.Call),
    }
    server_options = beta_implementations.server_options(request_deserializers=request_deserializers, response_serializers=response_serializers, thread_pool=pool, thread_pool_size=pool_size, default_timeout=default_timeout, maximum_timeout=maximum_timeout)
    return beta_implementations.server(method_implementations, options=server_options)


  def beta_create_Greeter_stub(channel, host=None, metadata_transformer=None, pool=None, pool_size=None):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This function was
    generated only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0"""
    request_serializers = {
      ('FunctionData.Greeter', 'Call'): FunctionRequest.SerializeToString,
    }
    response_deserializers = {
      ('FunctionData.Greeter', 'Call'): FunctionReply.FromString,
    }
    cardinalities = {
      'Call': cardinality.Cardinality.UNARY_UNARY,
    }
    stub_options = beta_implementations.stub_options(host=host, metadata_transformer=metadata_transformer, request_serializers=request_serializers, response_deserializers=response_deserializers, thread_pool=pool, thread_pool_size=pool_size)
    return beta_implementations.dynamic_stub(channel, 'FunctionData.Greeter', cardinalities, options=stub_options)
except ImportError:
  pass
# @@protoc_insertion_point(module_scope)
