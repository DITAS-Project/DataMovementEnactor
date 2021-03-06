# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import service_proto_buffers.dal_pb2 as dal__pb2


class DataMovementServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.startDataMovement = channel.unary_unary(
        '/com.ditas.ehealth.DataMovementService/startDataMovement',
        request_serializer=dal__pb2.StartDataMovementRequest.SerializeToString,
        response_deserializer=dal__pb2.StartDataMovementReply.FromString,
        )
    self.finishDataMovement = channel.unary_unary(
        '/com.ditas.ehealth.DataMovementService/finishDataMovement',
        request_serializer=dal__pb2.FinishDataMovementRequest.SerializeToString,
        response_deserializer=dal__pb2.FinishDataMovementReply.FromString,
        )


class DataMovementServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def startDataMovement(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def finishDataMovement(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_DataMovementServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'startDataMovement': grpc.unary_unary_rpc_method_handler(
          servicer.startDataMovement,
          request_deserializer=dal__pb2.StartDataMovementRequest.FromString,
          response_serializer=dal__pb2.StartDataMovementReply.SerializeToString,
      ),
      'finishDataMovement': grpc.unary_unary_rpc_method_handler(
          servicer.finishDataMovement,
          request_deserializer=dal__pb2.FinishDataMovementRequest.FromString,
          response_serializer=dal__pb2.FinishDataMovementReply.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'com.ditas.ehealth.DataMovementService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
