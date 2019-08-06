#!/usr/bin/env python3

from multiprocessing import Process

import connexion
from check_database import dme_agent
from swagger_server import encoder


def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    p = Process(target=dme_agent)
    app.add_api('swagger.yaml', arguments={'title': 'Data Movement Enactor'})
    p.start()
    app.run(port=8888, use_reloader=False)
    p.join()


if __name__ == '__main__':
    main()
