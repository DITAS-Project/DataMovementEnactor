import subprocess
import os.path
from shutil import which
import logging

from config import conf

LOG = logging.getLogger()


class DataSync:

    def check_if_source_file_exists(self, source_path):
        if not os.path.exists(source_path):
            raise Exception('Target path does not exist')

    def is_backend_available(self, name):
        if which(name) is None:
            raise Exception('{} not installed'.format(name))

    def sync_data(self, source_path, destination_host, destination_path, query):
        if not conf.sync_backend:
            raise Exception('Sync backend is not defined')
        try:
            cls = sync_backends[conf.sync_backend]
            sync_method = getattr(cls(), 'sync_data')
            sync_method(source_path=source_path, destination_host=destination_host, destination_path=destination_path)
        except KeyError:
            raise Exception('Incorrect sync backend')

    def finish_data_movement(self, query, path, destination):
        #TODO check circular import problem
        from dal_client.client import DALClient
        LOG.debug('Sync calling finish data movement with args, query: {}, path: {}, dest: {}'.format(query, path,
                                                                                                      destination))
        dal = DALClient(address=destination, port=conf.dal_default_port, destination=None)
        dal.generate_dal_message_properties()
        request = dal.create_finish_data_movement_request(query=query, sharedVolumePath=path)
        dal.send_finish_data_movement(request)

    def send_details_to_ds4m(self):
        #TODO contact DS4M with the destination where the data has moved
        pass


class RsyncData(DataSync):

    def sync_data(self, source_path, destination_host, destination_path, query):
        self.is_backend_available('rsync')
        self.check_if_source_file_exists(source_path)
        rsync_command = 'rsync -r -a {} {}:{}'.format(source_path, destination_host, destination_path)
        LOG.debug('Running rsync with rsync command: {}'.format(rsync_command))
        p = subprocess.Popen(rsync_command, shell=True)
        code = p.wait()
        if code == 0:
            LOG.debug('Rsync success, finishing data movement with args query: {}, path: {}, destination: {}'.format(
                query, destination_path, destination_host
            ))
            self.finish_data_movement(query=query, path=destination_path, destination=destination_host)


sync_backends = {
    'rsync': RsyncData
}