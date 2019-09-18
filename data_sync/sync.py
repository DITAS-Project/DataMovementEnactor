import subprocess
from config import conf
from shutil import which


class DataSync:

    def is_backend_available(self, name):
        if which(name) is None:
            raise Exception('{} not installed'.format(name))

    def sync_data(self, source_path, destination_path):
        if not conf.sync_backend:
            raise Exception('Sync backend is not defined')
        cls = conf.sync_backend
        sync_method = getattr(cls, 'sync_data')
        sync_method()


class RsyncData(DataSync):

    def sync_data(self, source_path, destination_path):
        self.is_backend_available('rsync')
        rsync_command = 'rsync -r -a {} {}'.format(source_path, destination_path)
        p = subprocess.Popen(rsync_command, shell=True)
        code = p.wait()
        if code == 0:
            print('Rsync success')