import time
import datetime
import logging

import MySQLdb
from movement_enactor.dme_orchestrator import DMContOrchestrator
from clients.redis_client import RedisClient
from clients.es_client import ElasticClient
from config import conf

LOG = logging.getLogger()


class DMEdatabase:

    def __init__(self, db_user=None, db_pass=None, db_name=None, db_host=None, db_port=None):
        self.db_user = db_user if db_user else conf.db_user
        self.db_pass = db_pass if db_pass else conf.db_pass
        self.db_name = db_name if db_name else conf.db_name
        self.db_host = db_host if db_host else conf.db_host
        self.db_port = db_port if db_port else conf.db_port
        self.es = ElasticClient()

    def connect_to_mysql_data_source(self):
        try:
            db = MySQLdb.connect(user=self.db_user, passwd=self.db_pass,
                                 db=self.db_name, host=self.db_host, port=self.db_port)
            db.autocommit(True)

            return db.cursor()
        except MySQLdb.Error as e:
            LOG.exception('Cannot connect to MySQL data source. Exception: {}'.format(e))


class DMEsymmetricds(DMEdatabase):

    def compile_sql_query_from_symmetricds(self, operation, table_name, insert_order, values, where_cond=None):
        type_map = {
            'I': 'INSERT INTO {table_name}({insert_order}) VALUES ({values})',
            'U': 'UPDATE {table_name} SET {set_values} WHERE {where_cond}',
            'D': 'DELETE FROM {table_name} WHERE {where_cond}'
        }

        if operation == 'I':
            query = type_map['I'].format(table_name=table_name,
                                         insert_order=','.join(insert_order), values=values)
        if operation == 'U':
            zipped = zip(insert_order, values.split(','))
            set_values = []
            for i in zipped:
                set_values.append('{} = {}'.format(i[0], i[1]))
            query = type_map['U'].format(table_name=table_name, set_values=','.join(set_values), where_cond=where_cond)

        if operation == 'D':
            query = type_map['D'].format(table_name=table_name, where_cond=where_cond)

        return query

    def add_query_to_elasitcsearch(self, query, target_dal):
        body = {
            "query": query,
            "target_dal": target_dal,
            "timestamp": datetime.datetime.now().isoformat()
        }
        self.es.write_db_updates_to_index(body=body)

    def check_for_updates(self):
        r = RedisClient()

        cursor = self.connect_to_mysql_data_source()
        cursor.execute('show tables')
        tables = cursor.fetchall()

        sym_data_table = False
        table_names = []

        for table in tables:
            if table[0] == 'sym_data':
                sym_data_table = True

        if not sym_data_table:
            LOG.exception('sym_data table not found in database. Current tables: {}'.format(tables))
        last_id = 0

        while True:
            moved_tables = r.get_list('moved_tables')
            target_dal = r.get('target_dal')

            dmo = DMContOrchestrator(target_dal)
            cursor.execute("SELECT * FROM sym_data WHERE data_id = (SELECT MAX(data_id) FROM sym_data)")
            result = cursor.fetchone()
            if result[1] in table_names and result[0] != last_id:
                last_id = result[0]
                cursor.execute("describe {}".format(result[1]))
                res = cursor.fetchall()
                table_cols = []
                primary_keys = []

                for r in res:
                    if r[3] != 'PRI':
                        table_cols.append(r[0])
                    else:
                        table_cols.insert(0, r[0])
                        primary_keys.append(r[0])

                where_cond = None
                if result[2] == 'U' or result[2] == 'D':
                    pk_data = result[4].split(',')
                    if len(pk_data) != len(primary_keys):
                        LOG.exception('pk_data data does not match primary key length')
                    elif len(pk_data) > 1:
                        zipped = zip(primary_keys, pk_data)
                        where_values = []
                        for i in zipped:
                            where_values.append('{} = {}'.format(i[0], i[1]))
                        where_cond = 'AND'.join(x for x in where_values)
                    elif len(pk_data) == 1:
                        where_cond = '{} = {}'.format(primary_keys[0], pk_data[0])

                sql_query = self.compile_sql_query_from_symmetricds(operation=result[2], table_name=result[1],
                                                                    insert_order=table_cols, values=result[3],
                                                                    where_cond=where_cond)
                if moved_tables and target_dal:
                    LOG.debug('Sending update query: {} to DAL'.format(sql_query))
                    dmo.send_query_to_dal(sql_query)
               
                self.add_query_to_elasitcsearch(sql_query, target_dal)
                time.sleep(5)
