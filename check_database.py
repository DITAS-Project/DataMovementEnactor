import time
import redis
import MySQLdb

from dal_client import DALClient


class DME:

    def __init__(self, db_user, db_pass, db_name, db_host, db_port, redis_host, redis_port):
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_name = db_name
        self.db_host = db_host
        self.db_port = db_port
        self.redis_host = redis_host
        self.redis_port = redis_port

    def connect_to_data_source(self):
        try:
            db = MySQLdb.connect(user=self.db_user, passwd=self.db_pass,
                                 db=self.db_name, host=self.db_host, port=self.db_port)
        except MySQLdb.Error as e:
            raise e

        db.autocommit(True)

        return db.cursor()

    def connect_to_redis(self):

        r = redis.StrictRedis(host=self.redis_host, port=self.redis_port, charset="utf-8", decode_responses=True)

        return r

    def compile_sql_query(self, operation, table_name, insert_order, values, where_cond=None):
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

    def agent_loop(self):
        cursor = self.connect_to_data_source()
        cursor.execute('show tables')
        tables = cursor.fetchall()

        sym_data_table = False
        table_names = []

        for table in tables:
            if not table[0].startswith('sym'):
                table_names.append(table[0])
            elif table[0] == 'sym_data':
                sym_data_table = True

        if not sym_data_table:
            raise Exception('sym_data table not found in database')
        dal = DALClient(address='localhost', port=50051)
        red = self.connect_to_redis()
        last_id = 0
        while True:
            target = red.get('active_movement')
            if target:
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
                            raise Exception('pk_data data does not match primary key number')
                        elif len(pk_data) > 1:
                            zipped = zip(primary_keys, pk_data)
                            where_values = []
                            for i in zipped:
                                where_values.append('{} = {}'.format(i[0], i[1]))
                            where_cond = 'AND'.join(x for x in where_values)
                        elif len(pk_data) == 1:
                            where_cond = '{} = {}'.format(primary_keys[0], pk_data[0])

                    sql_query = self.compile_sql_query(operation=result[2], table_name=result[1],
                                                       insert_order=table_cols, values=result[3], where_cond=where_cond)
                    print(sql_query)

                    dal.send_start_data_movement(query=sql_query, path='/test')

                time.sleep(1)
