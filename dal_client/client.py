import grpc

from service_proto_buffers import dal_pb2_grpc
import service_proto_buffers.DalMessageProperties_pb2 as DalMessageProperties__pb2
from service_proto_buffers.dal_pb2 import StartDataMovementRequest

from data_sync.sync import DataSync


class DALMessageProperties:

    def __init__(self, purpose, requesterId, authorization, token):
        self.purpose = purpose
        self.requesterId = requesterId
        self.authorization = authorization + " " + token

    def generate(self):
        return DalMessageProperties__pb2.DalMessageProperties(purpose=self.purpose, requesterId=self.requesterId,
                                                              authorization=self.authorization)


class DALClient:

    def __init__(self, address, port, destination, dal_msg_properties, async=True):
        self.address = address
        self.port = port
        self.async = async
        self.destination = destination
        self.dal_msg_properties = dal_msg_properties
        self.path = None
        self.channel = grpc.insecure_channel('{}:{}'.format(address, port))
        self.stub = dal_pb2_grpc.DataMovementServiceStub(self.channel)

    def process_start_movement_async_response(self, future):
        DataSync.sync_data(source_path=self.path, destination_path='{}:{}'.format(self.destination, self.path))
        print('Response received: {}'.format(future.result()))

    def create_start_data_movement_request(self, query, sharedVolumePath, sourcePrivacyProperties=None,
                                           destinationPrivacyProperties=None):
        self.path = sharedVolumePath
        request = StartDataMovementRequest(query=query, sharedVolumePath=sharedVolumePath,
                                           dalMesssageProperties=self.dal_msg_properties,
                                           sourcePrivacyProperties=sourcePrivacyProperties,
                                           destinationPrivacyProperties=destinationPrivacyProperties)
        return request

    def send_start_data_movement(self, request):
        try:
            if self.async:
                call_future = self.stub.startDataMovement.future(request)
                call_future.add_done_callback(self.process_start_movement_async_response)
            else:
                self.stub.startDataMovement(request)
        except Exception as e:
            raise Exception('Error sending StartDataMovement gRPC call {}'.format(e))
