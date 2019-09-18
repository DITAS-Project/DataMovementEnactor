import grpc

from service_proto_buffers import dal_pb2_grpc
import service_proto_buffers.DalMessageProperties_pb2 as DalMessageProperties__pb2
from service_proto_buffers.dal_pb2 import StartDataMovementRequest

from data_sync.sync import DataSync


class DALClient:

    def __init__(self, address, port, destination):
        self.address = address
        self.port = port
        self.destination = destination
        self.dal_msg_properties = None
        self.path = None
        self.channel = grpc.insecure_channel('{}:{}'.format(address, port))
        self.stub = dal_pb2_grpc.DataMovementServiceStub(self.channel)

    def generate_dal_message_properties(self, purpose, requesterId, authorization, token):
        authorization = authorization + " " + token
        self.dal_msg_properties = DalMessageProperties__pb2.DalMessageProperties(purpose=purpose,
                                                                                 requesterId=requesterId,
                                                                                 authorization=authorization)

    def process_start_movement_async_response(self, future):
        ds = DataSync()
        ds.sync_data(source_path=self.path, destination_host=self.destination, destination_path=self.path)
        print('Response received: {}'.format(future.result()))

    def create_start_data_movement_request(self, query, sharedVolumePath, sourcePrivacyProperties=None,
                                           destinationPrivacyProperties=None):
        self.path = sharedVolumePath
        request = StartDataMovementRequest(query=query, sharedVolumePath=sharedVolumePath,
                                           dalMessageProperties=self.dal_msg_properties,
                                           sourcePrivacyProperties=sourcePrivacyProperties,
                                           destinationPrivacyProperties=destinationPrivacyProperties)
        return request

    def send_start_data_movement(self, request, async=True):
        try:
            if async:
                call_future = self.stub.startDataMovement.future(request)
                call_future.add_done_callback(self.process_start_movement_async_response)
            else:
                self.stub.startDataMovement(request)
        except Exception as e:
            raise Exception('Error sending StartDataMovement gRPC call {}'.format(e))
