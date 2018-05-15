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
#            print(row)
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
            Dict = dict(zip(['uid','tp_id','status','connect_info','nas_id','framed_ip_address', 'deposit', 'day_fee', 'credit', 'guest'], row)) 
            all = a.append(Dict)
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
#            print(all)
        return all
    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

    if __name__ == '__main__':
        update_with_user(uid)

def query_with_allusers():
    pass
#def query_with_allusers():
#    try:
#        dbconfig = read_db_config()
#        conn = MySQLConnection(**dbconfig)
#        cursor = conn.cursor()
#        cursor.execute('SELECT u.id, u.uid, DATE_FORMAT(u.activate, "%Y-%m-%d"),\
#                        DATE_FORMAT(u.expire, "%Y-%m%-%d"), u.credit, u.reduction,\
#                        DATE_FORMAT(u.reduction_date, "%Y-%m-%d"),\
#                        DATE_FORMAT(u.registration, "%Y-%m-%d"),\
#                        (DECODE(u.password, "test12345678901234567890")),u.gid,u.disable,u.company_id,u.bill_id,\
#                        DATE_FORMAT(u.credit_date, "%Y-%m-%d"), u.deleted,\
#                        up.fio, up.phone, up.email, up.address_street, up.address_build, up.address_flat, up.comments,\
#                        up.contract_id, up.contract_date, up.pasport_num, up.pasport_date, up.pasport_grant,up._telbot,up._telbot_send,\
#                        up._vk,up._vk_send, d.tp_id, d.logins, INET_NTOA(d.ip), INET_NTOA(d.netmask), d.cid, d.disable, b.deposit\
#                        FROM users u \
#                        LEFT JOIN users_pi up USING(uid)\
#                        LEFT JOIN dv_main d USING(uid) \
#                        LEFT JOIN bills b USING(uid) \
#                        WHERE u.uid=up.uid\
#                        LIMIT 10000;')
#        all = {}
#        a = []
#        for row in iter_row(cursor, 10):
##            print(row)
#            Dict = dict(zip(['login','uid','activate','expire','credit','reduction','reduction_date','registration','password','gid','disable',\
#                                        'company_id','bill_id','credit_date','deleted','fio','phone', 'email',\
#                                        'street', 'build', 'flat', 'descr',\
#                                        'contract_id', 'contract_date', 'pasport_num', 'pasport_date', 'pasport_grant',\
#                                        'telegram','teleram_send','vk','vk_send','tpid', 'logins','ip','netmask','cid', 'status','deposit' ], row)) 
#            all = a.append(Dict)
#
#    except Error as e:
#        print(e)
#
#    finally:
#        cursor.close()
#        conn.close()
#        return a
#
#    if __name__ == '__main__':
#        query_with_allusers()


def query_with_user(uid):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute('SELECT u.id, u.uid, u.activate,\
                        u.expire, u.credit, u.reduction,\
                        u.reduction_date,u.registration,\
                        (DECODE(u.password, "test12345678901234567890")),u.gid,u.disable,u.company_id,u.bill_id,\
                        u.credit_date, u.deleted,\
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
            Dict = dict(zip(['login','uid','activate','expire','credit','reduction','reduction_date','registration','password','groups_id','disable',\
                                        'company_id','bill_id','credit_date','deleted','fio','phone', 'email',\
                                        'street', 'building', 'flat', 'descr',\
                                        'contract_id', 'contract_date', 'pasport_num', 'pasport_date', 'pasport_grant',\
                                        'telegram','telegram_send','vk','vk_send','tpid', 'logins','ip','netmask','cid', 'status','deposit' ], row)) 

            all = a.append(Dict)

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
        cursor.execute('SELECT u.uid FROM users u LIMIT 10000');

        all = {}
        a = []
        for row in iter_row(cursor, 10):
#            print(row)
            Dict = dict(zip(['uid'], row)) 
            all = a.append(Dict)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return a
 
    if __name__ == '__main__':
        query_with_users_uid()

def query_with_tarifs():
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute('SELECT t.id, t.name, t.day_fee, t.active_day_fee, t.month_fee, t.comments FROM tarif_plans t LIMIT 2000');

        all = {}
        a = []
        for row in iter_row(cursor, 10):
#            print(row)
            Dict = dict(zip(['tpid','name', 'day_fee', 'month_fee', 'active_day_fee', 'comments' ], row)) 
            all = a.append(Dict)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return a

    if __name__ == '__main__':
        query_with_tarifs()

def query_with_tarif_tpid(tpid):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute('SELECT t.id, t.name, t.day_fee, t.active_day_fee, t.month_fee, t.comments FROM tarif_plans t\
                        WHERE t.id={tpid}\
                        LIMIT 1;'.format(tpid=str(tpid)))

        all = {}
        a = []
        for row in iter_row(cursor, 10):
#            print(row)
            Dict = dict(zip(['tpid','name', 'day_fee', 'month_fee', 'active_day_fee', 'comments' ], row)) 
            all = a.append(Dict)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return a

    if __name__ == '__main__':
        query_with_tarif_tpid(tpid)

def query_with_groups():
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute('SELECT g.gid, g.name, g.descr FROM groups g LIMIT 2000');

        all = {}
        a = []
        for row in iter_row(cursor, 10):
#            print('=GROUP_ID=*'*10)
#            print(row)
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

def query_with_group_gid(gid):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute('SELECT g.gid, g.name, g.descr FROM groups g \
                        WHERE g.gid={gid}\
                        LIMIT 1;'.format(gid=str(gid)))

        all = {}
        a = []
        for row in iter_row(cursor, 10):
#            print(row)
            Dict = dict(zip(['gid','name', 'descr' ], row)) 
            all = a.append(Dict)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return a

    if __name__ == '__main__':
        query_with_group_gid(gid)

def query_with_user_uid(uid):
    ''' Обновление данных пользователя в локальной базе '''
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute('SELECT u.uid, u.id,(DECODE(u.password, "test12345678901234567890")),\
                        up.fio, up.phone, up.comments, u.disable, u.deleted, d.tp_id,u.gid,\
                        up.address_street, up.address_build, up.address_flat,\
                        INET_NTOA(d.ip), INET_NTOA(d.netmask), d.cid,\
                        d.logins,u.bill_id, b.deposit, u.registration, u.activate,\
                        u.reduction, u.reduction_date,u.credit,u.credit_date,up.contract_id,\
                        up.contract_date, up.pasport_num, up.pasport_date, up.pasport_grant,up._telbot, up._telbot_send,\
                        up._vk, up._vk_send, u.expire, d.disable, u.company_id, up.email\
                        FROM users u\
                        LEFT JOIN users_pi up USING(uid)\
                        LEFT JOIN dv_main d USING(uid) \
                        LEFT JOIN bills b USING(uid) \
                        WHERE u.uid=up.uid and u.uid={uid}\
                        LIMIT 1;'.format(uid=str(uid)))
        rows = cursor.fetchmany()
        item = []
        for i in rows[0]:                            # Декодируем в UTF8 bytearray
            if type(i) == bytearray:
                item.append(i.decode('utf-8'))
            else:
                item.append(i)
        User = []  # создаем список и добавлям словари UserDict, UserAdrDict, UserNetwDict, UserPIDict
        UserDict = dict(zip(['uid','login','password','fio','phone','descr','disable','delete','tarifs_id','groups_id'],item[:10]))
        User.append(UserDict)
        UserAdrDict = dict(zip(['street', 'building', 'flat'],item[10:13]))
        User.append(UserAdrDict)
        UserNetwDict = dict(zip(['ip','netmask','cid'],item[13:16]))
        User.append(UserNetwDict)

        UserPIDict = dict(zip(['logins','bill_id','balance','registration','activate','reduction','reduction_date',\
                               'credit','credit_date','contract_id','contract_date', 'pasport_num', 'pasport_date', 'pasport_grant',\
                               'telegram','telegram_send','vk','vk_send','expire','status','company_id', 'email'],item[16:]))
        User.append(UserPIDict)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return User

    if __name__ == '__main__':
        query_with_user_uid(uid)

def query_with_dv_calls():
    ''' Выборка пользователей Online '''
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute('SELECT dv.status,dv.user_name,dv.started,dv.acct_session_id,\
                        dv.acct_session_time,dv.acct_input_octets,dv.acct_output_octets,\
                        dv.framed_ip_address,dv.lupdated,dv.CID,dv.CONNECT_INFO,dv.tp_id,\
                        dv.nas_id,dv.uid,dv.guest\
                        FROM dv_calls dv LIMIT 10000;')
        all = {}
        dv = []
        for row in iter_row(cursor, 10):
           DvCallsDict = dict(zip(['status','username','started','acct_session_id','acct_session_time',\
                            'acct_input_octets','acct_output_octets','framed_ip_address','lupdated',\
                            'cid','connect_info','tpid','nas_id','uid','guest'],row))
           all = dv.append(DvCallsDict)
    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return dv

    if __name__ == '__main__':
        query_with_dv_calls()
