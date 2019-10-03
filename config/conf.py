sync_backend = 'rsync'
dal_default_port = 50055
keycloak_url = 'https://153.92.30.56:58080/auth/realms/288/protocol/openid-connect/token'
keycloak_settings = {
    'username': 'bogdan',
    'password': '',
    'client_id': 'vdc_client',
    'grant_type': 'password'
}
shared_volume_system_path = '/home/cloudsigma/movement'


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
