#!/usr/bin/env python3
import threading

import connexion

from swagger_server import encoder
from movement_enactor.dme_monitor import DMEsymmetricds
from config import conf
from clients.redis_client import RedisClient


def main():
    dmm = DMEsymmetricds()
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Data Movement Enactor'}, pythonic_params=True)
    if conf.port:
        port = conf.port
    else:
        port = 30030
    r = RedisClient()
    # ensure this is empty at start
    r.redis.delete('moved_tables')
    t1 = threading.Thread(target=dmm.check_for_updates, args=[])
    t1.start()
    app.run(port=port)


if __name__ == '__main__':
    main()
