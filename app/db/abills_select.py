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
    '''Выборка улиц, домов, кв'''
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute('SELECT up.address_street, up.address_build, up.address_flat FROM users_pi up LIMIT 10000');

        all = {}
        a = []
        for row in iter_row(cursor, 10):
            UidDepositDict = dict(zip(['street','build', 'flat' ], (row[0],str_build_num(row[1]),str_build_num(row[2]))))
            all = a.append(UidDepositDict)

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
            UidDepositDict = dict(zip(['gid','name', 'descr' ], row)) 
            all = a.append(UidDepositDict)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return a

    if __name__ == '__main__':
        query_with_groups()

