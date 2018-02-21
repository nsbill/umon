from app import db
from flask import Blueprint
from flask import render_template
import sys
sys.path.insert(0, '/app/db')
from mysql_select import query_with_allusers, query_with_user, query_with_users_uid, query_with_tarifs, query_with_groups
import subprocess
from models import Users, Address, Networks, Groups, Tarifs, UsersPI

users = Blueprint('users',__name__, template_folder='templates')
@users.route('/')
def index():
    users = Users.query.all()
    useraddr = Address.query.all()
#    for u in session.query(Users).all(): # выборка в словарь
#            print(u.__dict__)
    return render_template('users/index.html',users=users)

@users.route('/addallusers')
def addallusers():
    ''' Перенос пользователей из базы Abills '''

    tarifs = query_with_tarifs() # выборка тарифных планов
    for tarif in tarifs:
        tf =  Tarifs(tpid=tarif.get('tpid'),
                name=tarif.get('name'),
                day_fee=tarif.get('day_fee'),
                month_fee=tarif.get('month_fee'),
                active_day_fee=tarif.get('active_day_fee'),
                comments=tarif.get('comments'))
        db.session.add(tf) # добавляем в базу PostgreSQL

    groups = query_with_groups() # выборка тарифных планов
    for group in groups:
        gr = Groups(gid=group.get('gid'),
                name=group.get('name'),
                descr=group.get('descr'))
        db.session.add(gr) # добавляем в базу PostgreSQL
    gr0 = Groups(gid=99999, name='', descr='') # группа 0
    db.session.add(gr0)


    db.session.commit() # сохраняем в базу PostgreSQL

    lusers_uid = [ i[0] for i in db.session.query(Users.uid) ]  # выборка uid из локальной базы PostgreSQL

    users_uid = query_with_users_uid() # выборка uid из базы Abills
    users_uid = [ i['uid'] for i in users_uid ]
    s = set(lusers_uid) ^ set(users_uid) # Сортировка и удаление существующих uid 
    users = [ query_with_user(uid=i)[0] for i in s ] # выборка пользователей по uid из базы Abills
    d = [ [ i for i in u.items()] for u in users] # проверка полей и удаление пустых полей
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

        u.append(user) # для логирования и вывод в представление
    # создаем словарь с данными пользователя
        if user.get('gid') == 0:
            gid = 99999
        else:
            gid = user.get('gid')

        userdata = Users(uid=user.get('uid'),
                login=user.get('login'),
                password=user.get('password').decode('utf-8'),
                fio=user.get('fio'),
                phone=user.get('phone'),
                descr=user.get('descr'),
                disable=user.get('disable'),
                delete=user.get('deleted'),
                tarifs_id=user.get('tp_id'),
                groups_id=gid)
        db.session.add(userdata) # добаляем в базу PostgreSQL

        useraddr = Address(uid=user.get('uid'),
                address=user.get('address'),
                street=user.get('address_street'),
                building=user.get('address_build'),
                flat=user.get('address_flat'))
        db.session.add(useraddr) # добавляем в базу PostgreSQL

        usernet = Networks(uid=user.get('uid'),
                ip=user.get('ip'),
                netmask=user.get('netmask'),
                cid=user.get('cid'))
        db.session.add(usernet) # добавляем в базу PostgreSQL

        userpi = UsersPI(uid=user.get('uid'),
              balance=user.get('balance'),
              registration =user.get('registration'),
              reduction=user.get('reduction'),
              reduction_date=user.get('reduction_date'),
              credit=user.get('credit'),
              credit_date=user.get('credit_date'),
              archive=user.get('archive'),
              contract_id=user.get('contract_id'),
              contract_date=user.get('contract_date'),
              pasport_num=user.get('pasport_num'),
              pasport_date=user.get('pasport_date'),
              telegram=user.get('telegram'),
              telegram_send=user.get('telegram_send'),
              vk=user.get('vk'),
              vk_send=user.get('vk_send'))
        db.session.add(userpi) # добавляем в базу PostgreSQL

    db.session.commit() # сохраняем в базу PostgreSQL
    return render_template('users/index.html',users=u)
