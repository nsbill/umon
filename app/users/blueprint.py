from app import db
from flask import Blueprint
from flask import render_template
from datetime import datetime
import sys
sys.path.insert(0, '/app/db')

from mysql_select import query_with_allusers, query_with_user, query_with_users_uid, query_with_tarifs, query_with_tarif_tpid, query_with_groups, query_with_group_gid, query_with_user_uid
import subprocess
from models import Users, Address, Networks, Groups, Tarifs, UsersPI

users = Blueprint('users',__name__, template_folder='templates')
@users.route('/')
def index():
    ''' Выборка всех пользователей из базы PostgreSQL '''
    UsersALL =[ i for i in db.session.query(Users,Address,Networks,UsersPI)
                                            .filter(Users.uid == Address.uid,
                                                    Users.uid == Networks.uid,#
                                                    Users.uid == UsersPI.uid).all()]
    return render_template('users/index.html', UsersALL=UsersALL)

@users.route('/user/<uid>')
def user(uid):
    ''' Выборка данных о пользователе по UID '''
    def upd_user(*args):
        user = args[1][0]
        adr = args[1][1]
        netw = args[1][2]
        userpi =args[1][3]
        db.session.query(Users).filter(Users.uid == args[0]).update(user)
        db.session.query(Address).filter(Address.uid == args[0]).update(adr)
        db.session.query(Networks).filter(Networks.uid == args[0]).update(netw)
        db.session.query(UsersPI).filter(UsersPI.uid == args[0]).update(userpi)
        db.session.commit()

    ii = query_with_user_uid(uid)
    upd_user(uid, ii)
    UserInfo =[ i for i in db.session.query(Users,Address,Networks,UsersPI,Tarifs,Groups)
                                            .filter(Users.uid == uid,
                                                Address.uid == uid,
                                                Networks.uid == uid,
                                                UsersPI.uid == uid,
                                                Tarifs.tpid == Users.tarifs_id,
                                                Groups.gid == Users.groups_id).first()]
    return render_template('users/userinfo.html', UserInfo=UserInfo, DateTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@users.route('/addallusers')
def addallusers():
    ''' Перенос пользователей из базы Abills '''

    ltpid = [ i[0] for i in db.session.query(Tarifs.tpid) ] # выборка tpid из локальной базы PostgreSQL
    tarifs = query_with_tarifs()                            # выборка тарифных планов из базы Abills
    tp_id = [i['tpid'] for i in tarifs]                     # выборка tpid из базы Abills
    s = set(ltpid) ^ set(tp_id)                             # Сортировка и удаление существующих tpid
    print('-s-'*20)
    tarifs = [ query_with_tarif_tpid(tpid=i)[0] for i in s ]# выборка пользователей по tpid из базы Abills
    print(tarifs)
    for tarif in tarifs:
        tf =  Tarifs(tpid=tarif.get('tpid'),
                name=tarif.get('name'),
                day_fee=tarif.get('day_fee'),
                month_fee=tarif.get('month_fee'),
                active_day_fee=tarif.get('active_day_fee'),
                comments=tarif.get('comments'))
        db.session.add(tf)                                  # добавляем в базу PostgreSQL


    lgid = [ i[0] for i in db.session.query(Groups.gid) ]   # выборка gid из локальной базы PostgreSQL
    if lgid==[]:
        gr0 = Groups(gid=0, name='', descr='')              # группа 0
        db.session.add(gr0)
        db.session.commit()                                     # сохраняем в базу PostgreSQL

    g_id=[]
    for i in lgid:
        if i == 0:
            i = 0
        else:
            g_id.append(i)
    groups = query_with_groups()                            # выборка тарифных планов из базы Abills
    gr_id = [i['gid'] for i in groups]                      # выборка gid из базы Abills
    g = set(g_id) ^ set(gr_id)                              # Сортировка и удаление существующих gid
    g = list(g)
    groups = [ query_with_group_gid(gid=i)[0] for i in g ]  # выборка пользователей по gid из базы Abills
    for group in groups:
        gr = Groups(gid=group.get('gid'),
                name=group.get('name'),
                descr=group.get('descr'))
        db.session.add(gr)                                  # добавляем в базу PostgreSQL
    db.session.commit()                                     # сохраняем в базу PostgreSQL

    lusers_uid = [ i[0] for i in db.session.query(Users.uid) ]  # выборка uid из локальной базы PostgreSQL

    users_uid = query_with_users_uid()                      # выборка uid из базы Abills
    users_uid = [ i['uid'] for i in users_uid ]
    s = set(lusers_uid) ^ set(users_uid)                    # Сортировка и удаление существующих uid 
    users = [ query_with_user(uid=i)[0] for i in s ]        # выборка пользователей по uid из базы Abills
    d = [ [ i for i in u.items()] for u in users]           # проверка полей и удаление пустых полей
    w=[]
    for ii in d:
        k=[]
        for i in ii:
            if i[1]=='':
               True
            elif i[1] == None:
               True
            elif i[1] == 'NULL':
               True
            else:
               k.append(i)
        w.append(dict(k))
    u = []
    for user in w:
        print('--User--'*10)
        print(user)

        u.append(user)                              # для логирования и вывод в представление

        userdata = Users(uid=user.get('uid'),
                login=user.get('login'),
                password=user.get('password').decode('utf-8'),
                fio=user.get('fio').upper(),
                phone=user.get('phone'),
                descr=user.get('descr'),
                disable=user.get('disable'),
                delete=user.get('deleted'),
                tarifs_id=user.get('tarifs_id'),
                groups_id=user.get('groups_id'))
        db.session.add(userdata) # добаляем в базу PostgreSQL

        useraddr = Address(uid=user.get('uid'),
                address=user.get('address'),
                street=user.get('street').upper(),
                building=user.get('building'),
                flat=user.get('flat'))
        db.session.add(useraddr) # добавляем в базу PostgreSQL

        usernet = Networks(uid=user.get('uid'),
                ip=user.get('ip'),
                netmask=user.get('netmask'),
                cid=user.get('cid').upper())
        db.session.add(usernet) # добавляем в базу PostgreSQL

        userpi = UsersPI(uid=user.get('uid'),
              balance=user.get('deposit'),
              registration=user.get('registration'),
              activate=user.get('activate'),
              expire=user.get('expire'),
              bill_id=user.get('bill_id'),
              logins=user.get('logins'),
              reduction=user.get('reduction'),
              reduction_date=user.get('reduction_date'),
              credit=user.get('credit'),
              credit_date=user.get('credit_date'),
#              archive=user.get('archive'),
              archive=False,
              contract_id=user.get('contract_id'),
              contract_date=user.get('contract_date'),
              pasport_num=user.get('pasport_num'),
              pasport_date=user.get('pasport_date'),
              telegram=user.get('telegram'),
              telegram_send=user.get('telegram_send'),
              vk=user.get('vk'),
              vk_send=user.get('vk_send'),
              status=user.get('disable'),
              company_id=user.get('company_id'),
              email=user.get('email'))

        db.session.add(userpi) # добавляем в базу PostgreSQL

    db.session.commit() # сохраняем в базу PostgreSQL
    return render_template('users/index.html',users=u)
