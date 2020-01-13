import os
import json
import logging

LOG = logging.getLogger()


vdc_shared_config = '/etc/ditas/data_movement_enactor.json'

config = {}
if os.path.isfile(vdc_shared_config):
    with open(vdc_shared_config) as dme_conf_file:
        dme_conf = json.load(dme_conf_file)
else:
    dme_conf = dict()


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
#ES config
elasticsearch_url = dme_conf.get('ElasticSearchURL', None)
elasticsearch_authenticate = dme_conf.get('elasticsearch_authenticate', False)
elasticsearch_user = dme_conf.get('elasticsearch_user', None)
elasticsearch_password = dme_conf.get('elasticsearch_password', None)
#FTP config
shared_ftp_host = dme_conf.get('ftp_host', '178.22.69.180')
shared_ftp_user = dme_conf.get('ftp_user', 'ditas')
shared_ftp_pass = dme_conf.get('ftp_pass', '**')
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
de_endpoint = 'http://{}:50012'.format('localhost')

#DS4M endpoint
ds4m_endpoint = 'http://{}:30003'.format('localhost')

#Redis settings
redis_host = 'localhost'
redis_port = 6379

#SymmetricDS db settings
db_user = dme_conf.get('db_user', None)
db_pass = dme_conf.get('db_pass', None)
db_host = dme_conf.get('db_host', None)
db_port = dme_conf.get('db_port', None)
db_name = dme_conf.get('db_name', None)

#DB update ES config
db_update_es_index = 'dme-db-updates'

db_update_es_settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
        },
    "mappings": {
        "db_update": {
            "dynamic": "strict",
            "properties": {
                "query": {
                    "type": "text"
                    },
                "target_dal": {
                    "type": "text"
                    },
                "timestamp": {
                    "type": "date"
                }
                }
            }
        }
    }

