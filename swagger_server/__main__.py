#!/usr/bin/env python3
import threading

import connexion

from swagger_server import encoder
from movement_enactor.dme_monitor import DMEsymmetricds


def main():
    dmm = DMEsymmetricds()
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Data Movement Enactor'}, pythonic_params=True)
    t1 = threading.Thread(target=dmm.check_for_updates, args=[])
    t1.start()
    app.run(port=8111)


if __name__ == '__main__':
    main()
