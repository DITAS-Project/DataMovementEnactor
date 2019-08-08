#!/usr/bin/env python3

from multiprocessing import Process

import connexion
from check_database import DME
from swagger_server import encoder


def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    dme_instance = DME(db_user='symmetricds', db_pass='', db_name='hospital', db_host='127.0.0.1', db_port=5601,
                       redis_host='localhost', redis_port=6379)
    p = Process(target=dme_instance.agent_loop())
    app.add_api('swagger.yaml', arguments={'title': 'Data Movement Enactor'})
    p.start()
    app.run(port=8888, use_reloader=False)
    p.join()


if __name__ == '__main__':
    main()
