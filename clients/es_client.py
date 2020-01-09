from elasticsearch import Elasticsearch
from conf import config
import logging


LOG = logging.getLogger()


class ElasticClient:

    def __init__(self, es_api=None, **kwargs):
        self.es_api = es_api if es_api else config.elastisearch_url
        if config.elasticsearch_authenticate:
            self.es = Elasticsearch(self.es_api, http_auth=(config.elasticsearch_user,
                                                            config.elasticsearch_password), **kwargs)
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

    def write_db_updates_to_es(self):
        if not self.es.indices.exists(config.db_update_es_index):
            self.es.indices.create(index=config.db_update_es_index)
            LOG.debug('Created index: {}'.format(config.db_update_es_index))

