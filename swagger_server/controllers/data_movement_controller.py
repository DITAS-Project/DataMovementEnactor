import connexion
import six

from swagger_server.models.req_body import ReqBody  # noqa: E501
from swagger_server.models.start_dm import StartDM  # noqa: E501
from swagger_server import util


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

    print(body.movements_enaction[0], body.movements_enaction[0]['to'])

    return 'do some magic!'


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
