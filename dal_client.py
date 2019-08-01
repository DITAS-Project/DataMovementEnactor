import grpc
import dal_pb2_grpc

from dal_pb2 import StartDataMovementRequest, FinishDataMovementRequest


def start_data_movement(query, path):
    channel = grpc.insecure_channel('localhost:50051')
    stub = dal_pb2_grpc.DataMovementServiceStub(channel)

    request = StartDataMovementRequest(query=query, sharedVolumePath=path)
    try:
        stub.startDataMovement(request)
    except Exception as e:
        raise Exception('Error sending gRPC call {}'.format(e))


def finish_data_movement(path):
    channel = grpc.insecure_channel('localhost:50051')
    stub = dal_pb2_grpc.DataMovementServiceStub(channel)

    request = FinishDataMovementRequest(sharedVolumePath=path)
    try:
        stub.finishDataMovement(request)
    except Exception as e:
        raise Exception('Error sending gRPC call {}'.format(e))