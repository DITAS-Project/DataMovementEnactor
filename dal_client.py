import grpc
import dal_pb2_grpc

from dal_pb2 import StartDataMovementRequest, FinishDataMovementRequest


class DALClient:

    def __init__(self, address, port, async=True):
        self.port = port
        self.address = address
        self.channel = grpc.insecure_channel('{}:{}'.format(address, port))
        self.async = async
        self.stub = dal_pb2_grpc.DataMovementServiceStub(self.channel)

    def process_async_response(self, future):
        print('Response received: {}'.format(future.result()))

    def send_start_data_movement(self, query, path):
        request = StartDataMovementRequest(query=query, sharedVolumePath=path)
        try:
            if self.async:
                call_future = self.stub.startDataMovement.future(request)
                call_future.add_done_callback(self.process_async_response)
            else:
                self.stub.startDataMovement(request)
        except Exception as e:
            raise Exception('Error sending StartDataMovement gRPC call {}'.format(e))

    def send_finish_data_movement(self, path):
        request = FinishDataMovementRequest(sharedVolumePath=path)
        try:
            if self.async:
                call_future = self.stub.finishDataMovement.future(request)
                call_future.add_done_callback(self.process_async_response)
            else:
                self.stub.finishDataMovement(request)
        except Exception as e:
            raise Exception('Error sending FinishDataMovement gRPC call {}'.format(e))