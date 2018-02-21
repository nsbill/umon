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

def query_with_negbalance_users():
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
        query_with_negbalance_users()

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

def query_with_allusers():
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute('SELECT u.id, u.uid, DATE_FORMAT(u.activate, "%Y-%m-%d"),\
                        DATE_FORMAT(u.expire, "%Y-%m%-%d"), u.credit, u.reduction,\
                        DATE_FORMAT(u.reduction_date, "%Y-%m-%d"),\
                        DATE_FORMAT(u.registration, "%Y-%m-%d"),\
                        (DECODE(u.password, "test12345678901234567890")),u.gid,u.disable,u.company_id,u.bill_id,u.ext_bill_id,\
                        DATE_FORMAT(u.credit_date, "%Y-%m-%d"),u.domain_id, u.deleted,\
                        up.fio, up.phone, up.email, up.address_street, up.address_build, up.address_flat, up.comments,\
                        up.contract_id, up.contract_date, up.pasport_num, up.pasport_date, up.pasport_grant,up._telbot,up._telbot_send,\
                        up._vk,up._vk_send, d.tp_id, d.logins, INET_NTOA(d.ip), INET_NTOA(d.netmask), d.cid, d.disable, b.deposit\
                        FROM users u \
                        LEFT JOIN users_pi up USING(uid)\
                        LEFT JOIN dv_main d USING(uid) \
                        LEFT JOIN bills b USING(uid) \
                        WHERE u.uid=up.uid\
                        LIMIT 10;')
        all = {}
        a = []
        for row in iter_row(cursor, 10):
#            print(row)
            UidDepositDict = dict(zip(['login','uid','activate','expire','credit','reduction','reduction_date','registration','password','gid','disable',\
                                        'company_id','bill_id','ext_bill_id','credit_date','domain_id','deleted','fio','phone', 'email',\
                                        'address_street', 'address_build', 'address_flat', 'comments',\
                                        'contract_id', 'contract_date', 'pasport_num', 'pasport_date', 'pasport_grant',\
                                        '_telbot','_telbot_send','_vk','_vk_send','tp_id', 'logins','ip','netmask','cid', 'disable','deposit' ], row)) 
            all = a.append(UidDepositDict)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return a

    if __name__ == '__main__':
        query_with_allusers()


def query_with_user(uid):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute('SELECT u.id, u.uid, DATE_FORMAT(u.activate, "%Y-%m-%d"),\
                        DATE_FORMAT(u.expire, "%Y-%m%-%d"), u.credit, u.reduction,\
                        DATE_FORMAT(u.reduction_date, "%Y-%m-%d"),\
                        DATE_FORMAT(u.registration, "%Y-%m-%d"),\
                        (DECODE(u.password, "test12345678901234567890")),u.gid,u.disable,u.company_id,u.bill_id,u.ext_bill_id,\
                        DATE_FORMAT(u.credit_date, "%Y-%m-%d"),u.domain_id, u.deleted,\
                        up.fio, up.phone, up.email, up.address_street, up.address_build, up.address_flat, up.comments,\
                        up.contract_id, up.contract_date, up.pasport_num, up.pasport_date, up.pasport_grant,up._telbot,up._telbot_send,\
                        up._vk,up._vk_send, d.tp_id, d.logins, INET_NTOA(d.ip), INET_NTOA(d.netmask), d.cid, d.disable, b.deposit\
                        FROM users u \
                        LEFT JOIN users_pi up USING(uid)\
                        LEFT JOIN dv_main d USING(uid) \
                        LEFT JOIN bills b USING(uid) \
                        WHERE u.uid=up.uid and u.uid={uid}\
                        LIMIT 1;'.format(uid=str(uid)))
        all = {}
        a = []
        for row in iter_row(cursor, 10):
#            print(row)
            UidDepositDict = dict(zip(['login','uid','activate','expire','credit','reduction','reduction_date','registration','password','gid','disable',\
                                        'company_id','bill_id','ext_bill_id','credit_date','domain_id','deleted','fio','phone', 'email',\
                                        'address_street', 'address_build', 'address_flat', 'comments',\
                                        'contract_id', 'contract_date', 'pasport_num', 'pasport_date', 'pasport_grant',\
                                        '_telbot','_telbot_send','_vk','_vk_send','tp_id', 'logins','ip','netmask','cid', 'disable','deposit' ], row)) 
            all = a.append(UidDepositDict)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return a

    if __name__ == '__main__':
        query_with_user(uid)

def query_with_users_uid():
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute('SELECT u.uid FROM users u LIMIT 20');

        all = {}
        a = []
        for row in iter_row(cursor, 10):
#            print(row)
            UidDepositDict = dict(zip(['uid'], row)) 
            all = a.append(UidDepositDict)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return a

    if __name__ == '__main__':
        query_with_users_uid()
