from app import db
from flask import Blueprint
from flask import render_template
from datetime import datetime
import sys
import time
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

@users.route('/addusers')
def addusers():
    ''' Перенос пользователей, тарифных планов, групп из базы Abills '''
#Tarifs
    ltpid = [ i[0] for i in db.session.query(Tarifs.tpid) ] # выборка tpid из локальной базы PostgreSQL
    tarifs = query_with_tarifs()                            # выборка тарифных планов из базы Abills
    tp_id = [i['tpid'] for i in tarifs]                     # выборка tpid из базы Abills
    s = set(ltpid) ^ set(tp_id)                             # Сортировка и удаление существующих tpid
    for i in s:                                             # выборка тариф по tpid из базы Abills
        db.session.close()                                  # закрыть сессии если сущ
        tp = query_with_tarif_tpid(i)                       # выборка tpid из бызы Abills 
        db.session.bulk_insert_mappings(Tarifs,[tp[0]])     # вставка в базу PostgreSQL
        db.session.commit()

    lgid = [ i[0] for i in db.session.query(Groups.gid) ]   # выборка gid из локальной базы PostgreSQL
    g0 = Groups.query.filter_by(gid=0).first()
    if g0 == None:
        gr0 = Groups(gid=0, name='', descr='')              # Добавляем группу 0
        db.session.add(gr0)
        db.session.commit()                                 # сохраняем в базу PostgreSQL
#Groups
    groups = query_with_groups()                            # выборка тарифных планов из базы Abills
    gr_id = [i['gid'] for i in groups]                      # выборка gid из базы Abills
    g = set(lgid) ^ set(gr_id)                              # Сортировка и удаление существующих gid
    for i in g:                                             # выборка тариф по tpid из базы Abills
        db.session.close()                                  # закрыть существующие сессии
        if i == 0:
            i = 'Уже существует'
        else:
            gr = query_with_group_gid(i)                        # выборка gid из бызы Abills 
            db.session.bulk_insert_mappings(Groups,[gr[0]])     # вставка в базу PostgreSQL
            db.session.commit()
#Users
    lusers_uid = [ i[0] for i in db.session.query(Users.uid) ]  # выборка uid из локальной базы PostgreSQL
    users_uid = query_with_users_uid()                          # выборка uid из базы Abills
    users_uid = [ i['uid'] for i in users_uid ]
    s = set(lusers_uid) ^ set(users_uid)                        # Сортировка и удаление существующих uid 
    for i in s:                                                 # добавление пользователя в PostgreSQL
        db.session.close()                                      # закрыть существующие сессии
        user = query_with_user_uid(uid=i)                       # выборка пользователя их базы Abills по uid
        db.session.bulk_insert_mappings(Users,[user[0]])        # создание сесси для добавления в PostgreSQL
        user[1].update(uid=i)                                   # выборка адрес пользователя из базы Abills
        db.session.bulk_insert_mappings(Address,[user[1]])
        user[2].update(uid=i)                                   # выборка сетевые настройки польз. из базы Abills
        db.session.bulk_insert_mappings(Networks,[user[2]])
        user[3].update(uid=i)                                   # выборка информац о пользателе из базы Abills
        db.session.bulk_insert_mappings(UsersPI,[user[3]])
        db.session.commit()                                     # записать выбранные данные в базу PostgreSQL
    return render_template('users/addusers.html',Tarifs='Все тарифы добавлены',Groups='Все группы добавлены',Users='Все пользователи добавлены')
