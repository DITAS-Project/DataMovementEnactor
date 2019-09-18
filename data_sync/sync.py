import subprocess
import os.path
from shutil import which

from config import conf


class DataSync:

    def check_if_source_file_exists(self, source_path):
        if not os.path.exists(source_path):
            raise Exception('Target path does not exist')

    def is_backend_available(self, name):
        if which(name) is None:
            raise Exception('{} not installed'.format(name))

    def sync_data(self, source_path, destination_host, destination_path):
        if not conf.sync_backend:
            raise Exception('Sync backend is not defined')
        try:
            cls = sync_backends[conf.sync_backend]
            sync_method = getattr(cls(), 'sync_data')
            sync_method(source_path=source_path, destination_host=destination_host, destination_path=destination_path)
        except KeyError:
            raise Exception('Incorrect sync backend')

    def finish_data_movement(self, destination):
        pass


class RsyncData(DataSync):

    def sync_data(self, source_path, destination_host, destination_path):
        self.is_backend_available('rsync')
        self.check_if_source_file_exists(source_path)
        rsync_command = 'rsync -r -a {} {}:{}'.format(source_path, destination_host, destination_path)
        p = subprocess.Popen(rsync_command, shell=True)
        code = p.wait()
        if code == 0:
            print('Rsync success')
            self.finish_data_movement(destination=destination_path)


sync_backends = {
    'rsync': RsyncData
}