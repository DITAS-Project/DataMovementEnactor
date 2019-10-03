import connexion
import six
import logging
import logging.config


from swagger_server.models.req_body import ReqBody  # noqa: E501
from swagger_server.models.start_dm import StartDM  # noqa: E501
from swagger_server import util

from movement_enactor.dme_orchestrator import DMOrchestrator
from config import conf


logging.config.dictConfig(conf.log_conf)
LOG = logging.getLogger(__name__)


def finish_movement():  # noqa: E501
    """finish_movement

    Communication between DMEs. Indicates completed transfer between clusters. Relays finish call to DAL # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def init_movement(body):  # noqa: E501
    """Initialize data movement for destination using transformation

     # noqa: E501

    :param body: DME JSON schema sent by the DS4M
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = ReqBody.from_dict(connexion.request.get_json())  # noqa: E501

    sql_queries = []
    for d in body.data_sources:
        for db in d.database:
            for tb in db['tables']:
                columns = []
                if not tb['columns']:
                    columns.append('*')
                else:
                    for column in tb['columns']:
                        columns.append(column['column_id'])
                sql_queries.append('SELECT {} FROM {}'.format(','.join(columns), tb['table_id']))

    dmo = DMOrchestrator(source=body.movements_enaction[0]['from'], destination=body.movements_enaction[0]['to'],
                         query_list=sql_queries)
    LOG.debug('Sending queries to the DAL. Source: {}. destination: {}, queries: {}'.format(
        body.movements_enaction[0]['from'], body.movements_enaction[0]['to'], sql_queries))
    dmo.send_queries_to_dal()

    return 'Initialized data movement', 200


def start_movement(body):  # noqa: E501
    """Communication between DMEs. Signals the other DME to prepare for movement

     # noqa: E501

    :param body: Target path for creation
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = StartDM.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
