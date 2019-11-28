
config = dict()
#with open('/etc/ditas/data_movement_enactor.json') as dme_conf_file:
#    dme_conf = json.load(dme_conf_file)


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
shared_ftp_pass = '***'
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

#Redis settings
redis_host = 'localhost'
redis_port = 6379

#SymmetricDS db settings
db_user = ''
db_pass = ''
db_host = ''
db_port = ''
db_name = ''



