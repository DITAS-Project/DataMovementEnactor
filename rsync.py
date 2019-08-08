import subprocess


def rsync_data(source_path, destination_path):
    rsync_command = 'rsync -r -a {} {}'.format(source_path, destination_path)
    p = subprocess.Popen(rsync_command, shell=True)
    code = p.wait()
    if code == 0:
        print('Rsync success')


