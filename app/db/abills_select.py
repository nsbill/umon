# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/app/db')

from mysql.connector import MySQLConnection, Error
from mysql_db_conf import read_db_config
from dbfunc import str_build_num

def iter_row(cursor, size=10):
     while True:
         rows = cursor.fetchmany(size)
         if not rows:
             break
         for row in rows:
             yield row

def query_streetsbuildflat():
    '''Выборка улиц, домов, кв, uid'''
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute('SELECT up.address_street, up.address_build, up.address_flat, up.uid FROM users_pi up LIMIT 10000');

        all = {}
        a = []
        for row in iter_row(cursor, 10):
            Dict = dict(zip(['street','build', 'flat', 'uid'], (row[0],str_build_num(row[1]),str_build_num(row[2]),row[3])))
            all = a.append(Dict)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return a

    if __name__ == '__main__':
        query_streetsbuildflat()


def query_with_groups():
    '''Выборка групп'''
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute('SELECT g.gid, g.name, g.descr FROM groups g LIMIT 2000');

        all = {}
        a = []
        for row in iter_row(cursor, 10):
            Dict = dict(zip(['gid','name', 'descr' ], row)) 
            all = a.append(Dict)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return a

    if __name__ == '__main__':
        query_with_groups()

def query_with_dv_online_users():
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT d.uid, d.status, d.user_name, d.started, (SELECT SEC_TO_TIME(d.acct_session_time)), \
                     ((d.acct_input_octets + 4294967296 * acct_input_gigawords)), ((d.acct_output_octets + 4294967296 * acct_output_gigawords)), \
                     INET_NTOA(d.framed_ip_address), d.CID, d.CONNECT_INFO, d.tp_id, d.nas_id \
                    FROM dv_calls d LIMIT 2000")

#        all = {}
#        a = []
#        for row in iter_row(cursor, 10):
#            a.append(row)
#            all = row
#            # print(all)
        a = []
        for row in iter_row(cursor, 10):
           Dict = dict(zip(['uid','status','login','started','acct_session_time','acct_input_octets','acct_output_octets','ip','cid','info','tp_id','nas_id'], row ))
           a.append(Dict)
    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return a

        if __name__ == '__main__':
            query_with_dv_online_users()

def query_with_dv_online_user(uid):
    ''' Выборка онлайн пользователей по uid'''
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT d.uid, d.status, d.user_name, d.started, (SELECT SEC_TO_TIME(d.acct_session_time)), \
                     ((d.acct_input_octets + 4294967296 * acct_input_gigawords)), ((d.acct_output_octets + 4294967296 * acct_output_gigawords)), \
                     INET_NTOA(d.framed_ip_address), d.CID, d.CONNECT_INFO, d.tp_id, d.nas_id \
                    FROM dv_calls d \
                    WHERE d.uid = " + str(uid) + " limit 1")
        a = []
        for row in iter_row(cursor, 10):
           dict = dict(zip(['uid','status','login','started','acct_session_time','acct_input_octets','acct_output_octets','ip','cid','info','tp_id','nas_id'], row ))
           a.append(dict)
        a = a[0]
    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return a

    if __name__ == '__main__':
        query_with_dv_online_user(uid)
