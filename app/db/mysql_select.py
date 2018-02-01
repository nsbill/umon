# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/app/db')

from mysql.connector import MySQLConnection, Error
from mysql_db_conf import read_db_config
#from django.shortcuts import render

def iter_row(cursor, size=10):
    while True:
        rows = cursor.fetchmany(size)
        if not rows:
            break
        for row in rows:
            yield row

def query_with_bills():
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT b.uid, b.deposit FROM bills b where b.deposit < t.day_fee LIMIT 1000;")

        all = {}
        a = []
        for row in iter_row(cursor, 10):
            print(row)
            UidDepositDict = dict(zip(['uid', 'deposit'], row)) 
            all = a.append(UidDepositDict)
    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return a

    if __name__ == '__main__':
        query_with_bills()

def query_with_users():
    '''
    Выборка онлайн пользователей с депозитом ниже снятия за день,
    но больше депозита чем установленный кредит
    и с условием что не гостевой доступ.
    =================================================================================================
    | UID | Тариф ID | Статус | NG | NAS_ID | IP,Депозит | Оплата в день | Кредит | гостевой доступ |
    =================================================================================================

    MySQL query;
    ====================================================================================================
    SELECT d.uid, d.tp_id, d.status, d.connect_info, d.nas_id, d.framed_ip_address, b.deposit, t.day_fee, u.credit, d.guest
    FROM dv_calls d
    LEFT JOIN bills b ON (d.uid = b.uid)
    LEFT JOIN tarif_plans t ON (d.tp_id = t.id)
    LEFT JOIN users u ON (d.uid=u.uid)
    WHERE (b.deposit < t.day_fee) AND ((-u.credit) > b.deposit) AND d.guest=0
    LIMIT 5000
    ====================================================================================================
    '''
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT d.uid, d.tp_id, d.status, d.connect_info, d.nas_id, d.framed_ip_address, b.deposit, t.day_fee, u.credit, d.guest\
                        FROM dv_calls d\
                        LEFT JOIN bills b ON (d.uid = b.uid)\
                        LEFT JOIN tarif_plans t ON (d.tp_id = t.id)\
                        LEFT JOIN users u ON (d.uid=u.uid)\
                        WHERE (b.deposit < t.day_fee) AND ((-u.credit) > b.deposit) AND d.guest=0\
                        LIMIT 5000;")
        all = {}
        a = []
        for row in iter_row(cursor, 10):
            UidDepositDict = dict(zip(['uid','tp_id','status','connect_info','nas_id','framed_ip_address', 'deposit', 'day_fee', 'credit', 'guest'], row)) 
            all = a.append(UidDepositDict)
    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return a

    if __name__ == '__main__':
        query_with_users()

def update_with_user(uid): # uid = userUID
    '''
    Обновить статус в мониторинге
    0 - Не гость, 1 - Гость
    '''
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute('UPDATE dv_calls SET guest=1 WHERE uid={uid};'.format(uid=str(uid)))

        all = {}
        for row in iter_row(cursor, 10):
            all = row
            print(all)
        return all
    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

    if __name__ == '__main__':
        update_with_user(uid)

