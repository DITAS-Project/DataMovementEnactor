import grpc
import requests
import sys
import json
import logging

from service_proto_buffers import dal_pb2_grpc
import service_proto_buffers.DalMessageProperties_pb2 as DalMessageProperties__pb2
from service_proto_buffers.dal_pb2 import StartDataMovementRequest, FinishDataMovementRequest
from clients.redis_client import RedisClient

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
        try:
            r = requests.post(conf.keycloak_url, data=conf.keycloak_settings, verify=False)
        except requests.exceptions.RequestException as e:
            LOG.error('Could not connect to keycloak endpoint {}. Exception: {}'.format(conf.keycloak_url, e))
        try:
            json_resp = json.loads(r.text)
            self.token = json_resp['access_token']
        except KeyError:
            LOG.error('Could not fetch access token needed for DAL comm')
        return self.token

    def generate_dal_message_properties(self, purpose='data_movement_public_cloud', requesterId='requester',
                                        authorization='Bearer'):
        self.generate_access_token()
        authorization = authorization + " " + self.token
        self.dal_msg_properties = DalMessageProperties__pb2.DalMessageProperties(purpose=purpose,
                                                                                 requesterId=requesterId,
                                                                                 authorization=authorization)
        return self.dal_msg_properties

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

    def process_start_movement_async_response(self, future):
        LOG.debug('Start movement callback initiated')
        r = RedisClient()
        target_dal = r.get('target_dal')
        if not target_dal:
            LOG.exception('ERROR data movement is starting with no target DAL in Redis')
        target_channel = grpc.insecure_channel('{}:{}'.format(target_dal, conf.dal_default_port))
        stub = dal_pb2_grpc.DataMovementServiceStub(target_channel)
        request = self.create_finish_data_movement_request(query=self.query, sharedVolumePath=self.path)
        self.send_finish_data_movement(request, stub=stub)
        LOG.debug('Response received: {}'.format(future.result()))

    def send_start_data_movement(self, request, async=True):
        try:
            LOG.debug('Sending start data movement request: {}, async: {}'.format(request, async))
            if async:
                call_future = self.stub.startDataMovement.future(request)
                call_future.add_done_callback(self.process_start_movement_async_response)
            else:
                self.stub.startDataMovement(request)
        except Exception as e:
            LOG.exception('Error sending StartDataMovement gRPC call {}'.format(e))

    def send_finish_data_movement(self, request, stub=None):
        try:
            if not stub:
                self.stub.finishDataMovement(request)
            else:
                stub.finishDataMovement(request)
        except Exception as e:
            LOG.exception('Error sending finishDataMovement gRPC call {}'.format(e))

