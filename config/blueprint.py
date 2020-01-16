import json
import logging

LOG = logging.getLogger()


class Blueprint:

    def __init__(self, vdc_id=None):
        if vdc_id:
            self.file_path = '/var/ditas/vdm/DS4M/blueprints/{}.json'.format(vdc_id)

            with open(self.file_path, 'r') as blueprint_cont:
                try:
                    self.blueprint = json.load(blueprint_cont)
                except Exception as e:
                    LOG.exception('Could not load JSON content from concrete blueprint file: {}'.format(e))

       # self.abstract_blueprint_file_path = '/var/ditas/blueprint.json'

       # with open(self.abstract_blueprint_file_path, 'r') as abs_blueprint_cont:
       #         try:
       #             self.abs_blueprint = json.load(abs_blueprint_cont)
       #         except Exception as e:
       #             LOG.exception('Could not load JSON content from abstract blueprint file: {}'.format(e))

    def get_concrete_blueprint_id(self):

        return self.blueprint['_id']

    def get_source_dal_id(self, dal_ip):
        for id in self.blueprint['INTERNAL_STRUCTURE']['DAL_Images'].items():
            if id[1]['original_ip'] == dal_ip:
                return id[0]
