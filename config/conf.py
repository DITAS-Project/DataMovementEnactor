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

port = dme_conf.get('Port', None)
sync_backend = 'ftp'
dal_default_port = 30055
keycloak_url = 'https://153.92.30.225:58080/auth/realms/vdc_access/protocol/openid-connect/token'
keycloak_settings = {
    'username': 'bogdan',
    'refresh_token': 'eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIxNThjN2IxNi1mOWY0LTQ3NTUtYjEwZC0zMmFkY2ViNjE5MjQifQ.eyJqdGkiOiIyOGNkYTc5ZS02ODIxLTRmMDctOTdjMC01NzA5NzkzMmVjNmIiLCJleHAiOjE2MTExNDYwMDMsIm5iZiI6MCwiaWF0IjoxNTc5NjEwMDAzLCJpc3MiOiJodHRwczovLzE1My45Mi4zMC4yMjU6NTgwODAvYXV0aC9yZWFsbXMvdmRjX2FjY2VzcyIsImF1ZCI6Imh0dHBzOi8vMTUzLjkyLjMwLjIyNTo1ODA4MC9hdXRoL3JlYWxtcy92ZGNfYWNjZXNzIiwic3ViIjoiN2NkNzY2MWMtYThlOC00OWZhLTgyNjEtNjVmOGIwY2EzYjdiIiwidHlwIjoiUmVmcmVzaCIsImF6cCI6InZkY19jbGllbnQiLCJhdXRoX3RpbWUiOjAsInNlc3Npb25fc3RhdGUiOiJmOGUyZWJlYi1mZWI0LTRlYjEtYjM1Yy04OGE0ZTEwMDI1NmUiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZG9jdG9yIiwiZXh0ZXJuYWwtcmVzZWFyY2hlciIsInJlc2VhcmNoZXIiLCJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJwcm9maWxlIGVtYWlsIn0.Ar-TSftV_j7koSwQ4KF1gMdtjL-t6MZLH-tEYMxZh54',
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

#DE endpoint
de_endpoint = 'http://{}:50012'.format('localhost')

#DS4M endpoint
ds4m_endpoint = 'http://{}:30003'.format('localhost')

#Redis settings
redis_host = 'localhost'
redis_port = 30031

#SymmetricDS db settings
db_user = dme_conf.get('db_user', 'ditas')
db_pass = dme_conf.get('db_pass', None)
db_host = dme_conf.get('db_host', '104.36.16.223')
db_port = dme_conf.get('db_port', 3306)
db_name = dme_conf.get('db_name', 'ditas_dummy_example')

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
#DAL comm
asynchronous = True
