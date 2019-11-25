import grpc
import requests
import sys
import json
import logging

from service_proto_buffers import dal_pb2_grpc
import service_proto_buffers.DalMessageProperties_pb2 as DalMessageProperties__pb2
from service_proto_buffers.dal_pb2 import StartDataMovementRequest, FinishDataMovementRequest

import config.conf as conf

LOG = logging.getLogger()


class DALClient:

    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.dal_msg_properties = None
        self.path = None
        self.token = None
        self.query = None
        self.channel = grpc.insecure_channel('{}:{}'.format(address, port))
        self.stub = dal_pb2_grpc.DataMovementServiceStub(self.channel)

    def generate_access_token(self):
        #TODO implement refresh token
        try:
            r = requests.post(conf.keycloak_url, data=conf.keycloak_settings, verify=False)
        except requests.exceptions.RequestException as e:
            LOG.error('Could not connect to keycloak endpoint {}. Exception: {}'.format(conf.keycloak_url, e))
            sys.exit(1)
        try:
            json_resp = json.loads(r.text)
            self.token = json_resp['access_token']
        except KeyError:
            LOG.error('Could not fetch access token needed for DAL comm')
            sys.exit(1)
        return self.token

    def generate_dal_message_properties(self, purpose='read', requesterId='requester', authorization='Bearer'):
        self.generate_access_token()
        authorization = authorization + " " + self.token
        self.dal_msg_properties = DalMessageProperties__pb2.DalMessageProperties(purpose=purpose,
                                                                                 requesterId=requesterId,
                                                                                 authorization=authorization)
        return self.dal_msg_properties

    def process_start_movement_async_response(self, future):
        LOG.debug('Start movement callback initiated')
        #finish data movement for query
        LOG.debug('Response received: {}'.format(future.result()))

    def create_start_data_movement_request(self, query, sharedVolumePath, sourcePrivacyProperties=None,
                                           destinationPrivacyProperties=None):
        self.path = sharedVolumePath
        self.query = query
        request = StartDataMovementRequest(query=query, sharedVolumePath=sharedVolumePath,
                                           dalMessageProperties=self.dal_msg_properties,
                                           sourcePrivacyProperties=sourcePrivacyProperties,
                                           destinationPrivacyProperties=destinationPrivacyProperties)
        return request

    def create_finish_data_movement_request(self, query, sharedVolumePath, sourcePrivacyProperties=None,
                                            destinationPrivacyProperties=None):

        request = FinishDataMovementRequest(query=query, sharedVolumePath=sharedVolumePath,
                                            dalMessageProperties=self.dal_msg_properties,
                                            sourcePrivacyProperties=sourcePrivacyProperties,
                                            destinationPrivacyProperties=destinationPrivacyProperties)
        return request

    def send_start_data_movement(self, request, async=True):
        try:
            LOG.debug('Sending start data movement request: {}, async: {}'.format(request, async))
            if async:
                call_future = self.stub.startDataMovement.future(request)
                call_future.add_done_callback(self.process_start_movement_async_response)
            else:
                self.stub.startDataMovement(request)
        except Exception as e:
            raise Exception('Error sending StartDataMovement gRPC call {}'.format(e))

    def send_finish_data_movement(self, request):
        try:
            self.stub.finishDataMovement(request)
        except Exception as e:
            raise Exception('Error sending finishDataMovement gRPC call {}'.format(e))

