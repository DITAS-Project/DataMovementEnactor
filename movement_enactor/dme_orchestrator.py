import uuid
import re
import os
import logging

from dal_client.client import DALClient
from config import conf

LOG = logging.getLogger()


class DMOrchestrator(object):

    def __init__(self, source, destination, query_list, database=None):
        self.source = source
        self.destination = destination
        self.database = database
        self.query_list = query_list

    def generate_shared_volume_path(self):
        directory_name = uuid.uuid4().hex
        path = conf.shared_volume_system_path + directory_name
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def prepare_filename(self, query):
        stripped_query = re.sub(r'\W+', '', query)
        filename = stripped_query + '.parquet'
        return filename

    def connect_to_dal(self):
        dal = DALClient(address=self.source, port=conf.dal_default_port, destination=self.destination)
        LOG.debug('Connected to DAL at: {}'.format(self.source))
        dal.generate_dal_message_properties()
        return dal

    def send_queries_to_dal(self):
        dal = self.connect_to_dal()
        path = self.generate_shared_volume_path()
        LOG.debug('Generated filepath: {}'.format(path))
        for query in self.query_list:
            fname = self.prepare_filename(query)
            fpath = path + '/' + fname
            request = dal.create_start_data_movement_request(query=query, sharedVolumePath=fpath)
            dal.send_start_data_movement(request)


