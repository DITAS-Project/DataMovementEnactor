from elasticsearch import Elasticsearch, RequestError
from config import conf

import logging


LOG = logging.getLogger()


class ElasticClient:

    def __init__(self, es_api=None, **kwargs):
        self.es_api = es_api if es_api else conf.elasticsearch_url
        if conf.elasticsearch_authenticate:
            self.es = Elasticsearch(self.es_api, http_auth=(conf.elasticsearch_user,
                                                            conf.elasticsearch_password), **kwargs)
        else:
            self.es = Elasticsearch(self.es_api, **kwargs)

    def ping(self):
        if not self.es.ping():
            LOG.exception('Cannot connect to ES at: {}'.format(self.es_api))

    def search(self, index_name, query, **kwargs):
        if not self.es.indices.exists(index_name):
            LOG.exception('Index {} does not exist'.format(index_name))
        res = self.es.search(index=index_name, body=query, **kwargs)
        return res

    def write_db_updates_to_index(self, body):
        if not self.es.indices.exists(conf.db_update_es_index):
            self.es.indices.create(index=conf.db_update_es_index, body=conf.db_update_es_settings)
            LOG.debug('Created index: {}'.format(conf.db_update_es_index))
        try:
            res = self.es.index(index=conf.db_update_es_index,
                                doc_type=list(conf.db_update_es_settings['mappings'].keys())[0], body=body)
        except RequestError as e:
            LOG.exception('Error adding to index: {}'.format(e))
        if not res['result'] == 'created':
            LOG.exception('Error adding: {} with body: {} to index: {}'.format(
                list(conf.db_update_es_settings['mappings'].keys())[0], body, conf.db_update_es_index))
        return res

    def get_latest_from_index(self, index):
        query = {
            "query": {
                "match_all": {}
                },
            "size": 1,
            "sort": [
                {
                    "Records.eventTime": {
                        "order": "desc"
                        }
                    }
                ]
            }
        res = self.es.search(index=index, body=query)

        return res['hits']['hits']
