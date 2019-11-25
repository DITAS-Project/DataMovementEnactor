import json

sync_backend = 'ftp'
dal_default_port = 50055
keycloak_url = 'https://153.92.30.56:58080/auth/realms/288/protocol/openid-connect/token'
#TODO implement refresh token
keycloak_settings = {
    'username': 'bogdan',
    'password': '',
    'refresh_token': '',
    'client_id': 'vdc_client',
    'grant_type': 'refresh_token'
}
shared_ftp_host = '178.22.69.180'
shared_ftp_user = 'ditas'
shared_ftp_pass = 'GhQ096%mF4YF'
shared_volume_system_path = 'move/'

dry_run = True

# Logging config
log_conf = {
    'version': 1,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'NOTSET',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'NOTSET',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 5000000,
            'backupCount': 10,
            'filename': 'dme.main.log',
            'formatter': 'standard'
        }
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'NOTSET',
            'propagate': True
        },
    }
}

### HTTP clients config
max_retries = 3
backoff_factor = 3

#TODO complete endpoint generation
#DE endpoint
de_endpoint = ''

#DS4M endpoint
ds4m_endpoint = ''


class Blueprint:

    def __init__(self, vdc_id):
        self.file_path = '/var/ditas/vdm/DS4M/blueprints/{}.json'.format(vdc_id)

        with open(self.file_path, 'r') as blueprint_cont:
            try:
                self.blueprint = json.load(blueprint_cont)
            except Exception as e:
                raise Exception('Could not load JSON content from blueprint file: {}'.format(e))

    def get_blueprint_id(self):

        return self.blueprint['id']

    def get_source_dal_id(self, dal_ip):
        for id in self.blueprint['INTERNAL_STRUCTURE']['DAL_Images'].items():
            if id[1]['original_ip'] == dal_ip:
                return id[0]


