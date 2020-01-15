import subprocess
import os.path
from ftplib import FTP
from shutil import which
from pathlib import Path
import logging

from config import conf

LOG = logging.getLogger()


class DataSync:

    def check_if_source_file_exists(self, source_path):
        if conf.dry_run:
            Path(source_path).touch()
        elif not os.path.exists(source_path):
            raise Exception('Target path does not exist: {}'.format(source_path))

    def is_backend_available(self, name):
        if which(name) is None:
            raise Exception('{} not installed'.format(name))

    def sync_data(self, source_path, destination_host, destination_path, query):
        if not conf.sync_backend:
            raise Exception('Sync backend is not defined')
        try:
            cls = sync_backends[conf.sync_backend]
            sync_method = getattr(cls(), 'sync_data')
            sync_method(source_path=source_path, destination_host=destination_host, destination_path=destination_path,
                        query=query)
        except KeyError:
            raise Exception('Incorrect sync backend')

    def prepare_path(self, path):
        return os.path.dirname(path) + '/'

    def finish_data_movement(self, query, path, destination):
        from clients.dal_client import DALClient
        LOG.debug('Sync calling finish data movement with args, query: {}, path: {}, dest: {}'.format(query, path,
                                                                                                      destination))
        dal = DALClient(address=destination, port=conf.dal_default_port)
        dal.generate_dal_message_properties()
        request = dal.create_finish_data_movement_request(query=query, sharedVolumePath=path)
        dal.send_finish_data_movement(request)


class RsyncData(DataSync):

    def sync_data(self, source_path, destination_host, destination_path, query):
        self.is_backend_available('rsync')
        self.check_if_source_file_exists(source_path)
        destination_path = self.prepare_path(destination_path)
        rsync_command = 'rsync -a {} {}:{}'.format(source_path, destination_host, destination_path)
        LOG.debug('Running rsync with rsync command: {}'.format(rsync_command))
        p = subprocess.Popen(rsync_command, shell=True)
        code = p.wait()
        if code == 0:
            LOG.debug('Rsync success, finishing data movement with args query: {}, path: {}, destination: {}'.format(
                query, destination_path, destination_host
            ))
            self.finish_data_movement(query=query, path=destination_path, destination=destination_host)


class FTPsync:

    def __init__(self, ftp_host=None, ftp_user=None, ftp_pass=None):
        self.ftp_host = ftp_host if ftp_host else conf.shared_ftp_host
        self.ftp_user = ftp_user if ftp_user else conf.shared_ftp_user
        self.ftp_pass = ftp_pass if ftp_pass else conf.shared_ftp_pass

    def create_ftp_structure(self, path):
        try:
            ftp = FTP(self.ftp_host, self.ftp_user, self.ftp_pass)
            ftp.mkd(path)
            return True
        except Exception as e:
            LOG.exception('Cannot created path on FTP host: {}, exception: {}'.format(conf.shared_ftp_host, e))
        return False


sync_backends = {
    'rsync': RsyncData,
    'ftp': FTPsync
}