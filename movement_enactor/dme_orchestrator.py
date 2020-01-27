import uuid
import re
import os
import logging
import json

from clients.dal_client import DALClient
from clients.de_client import DEclient
from clients.ds4m_client import DS4Mclient
from clients.redis_client import RedisClient
from data_sync.sync import FTPsync
from config import conf
from config.blueprint import Blueprint

LOG = logging.getLogger()


class DMBase:

    def generate_shared_volume_path(self, ftp=True):
        directory_name = uuid.uuid4().hex
        path = conf.shared_volume_system_path + directory_name
        if not ftp and not os.path.exists(path):
            os.makedirs(path)
        return path

    def prepare_filename(self, query):
        stripped_query = re.sub(r'\W+', '', query)
        filename = stripped_query + '.parquet'
        return filename

    def connect_to_dal(self, dal_ip):
        dal = DALClient(address=dal_ip, port=conf.dal_default_port)
        LOG.debug('Connected to DAL at: {}'.format(dal_ip))
        dal.generate_dal_message_properties()
        return dal


class DMContOrchestrator(DMBase):

    def __init__(self, target_dal):
        self.target_dal = target_dal
        self.path = self.generate_shared_volume_path()

    def send_query_to_dal(self, query):
        filename = self.prepare_filename(query)
        path = self.path + '/' + filename
        dal = self.connect_to_dal(self.target_dal)
        request = dal.create_start_data_movement_request(query=query, sharedVolumePath=path)
        dal.send_start_data_movement(request)


class DMInitOrchestrator(DMBase):

    def __init__(self, source, dest_vdc_id, dest_infra_id, dal_original_ip, database=None):
        self.source = source
        self.dest_vdc_id = dest_vdc_id
        self.dest_infra_id = dest_infra_id
        self.dal_original_ip = dal_original_ip
        self.database = database
        self.blueprint = Blueprint(self.dest_vdc_id)
        self.blueprint_id = self.blueprint.get_concrete_blueprint_id()
        self.dal_id = self.blueprint.get_source_dal_id(self.dal_original_ip)
        self.dec = DEclient(endpoint=conf.de_endpoint)

    def create_target_dal(self):
        resp = self.dec.create_datasource(self.blueprint_id, self.dest_vdc_id, self.dest_infra_id, type='minio')
        response = self.dec.create_dal(self.blueprint_id, self.dest_vdc_id, self.dest_infra_id, self.dal_id)
        response_json = json.loads(response.text)
        new_dal_ip = response_json['Infrastructures'][self.dest_infra_id]['IP']
        r = RedisClient()
        r.set('target_dal', new_dal_ip)
        r.set('original_dal', self.dal_original_ip)
        return new_dal_ip

    def notify_ds4m_for_new_dal(self, dal_ip):
        ds4m_c = DS4Mclient(endpoint=conf.ds4m_endpoint)
        response = ds4m_c.notify_new_dal(dal_ip, self.dal_original_ip)
        return response

    def send_queries_to_dal(self, query_list, dal_ip):
        path = self.generate_shared_volume_path()
        ftp = FTPsync()
        ftp.create_ftp_structure(path)
        dal = self.connect_to_dal(dal_ip)
        LOG.debug('Generated filepath: {}'.format(path))
        LOG.debug('Starting data movement for queries: {}'.format(query_list))
        for query in query_list:
            fname = self.prepare_filename(query)
            fpath = path + '/' + fname
            request = dal.create_start_data_movement_request(query=query, sharedVolumePath=fpath)
            dal.send_start_data_movement(request)

    def finish_data_movement_for_queries(self, query_list, dal_ip):
        dal = self.connect_to_dal(dal_ip)
        LOG.debug('Finishing data movement for queries: {}'.format(query_list))
        for query in query_list:
            fname = self.prepare_filename(query)
            request = dal.create_finish_data_movement_request(query=query, sharedVolumePath=fname)
            dal.send_finish_data_movement(request)

    def initial_movement(self, query_list):
        self.send_queries_to_dal(query_list, self.dal_original_ip)
        new_dal_ip = self.create_target_dal()
        self.dec.move_dal(self.blueprint_id, self.dest_vdc_id, self.dest_infra_id, self.dal_id, new_dal_ip)
        self.notify_ds4m_for_new_dal(new_dal_ip)

