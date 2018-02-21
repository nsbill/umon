from app import db
from flask import Blueprint
from flask import render_template
import sys
sys.path.insert(0, '/app/db')
from mysql_select import query_with_allusers, query_with_user, query_with_users_uid
import subprocess
from models import Users

users = Blueprint('users',__name__, template_folder='templates')
@users.route('/')
def index():
    users = Users.query.all()
    return render_template('users/index.html',users=users)

@users.route('/addallusers')
def addallusers():
    ''' Перенос пользователей из базы Abills '''
    lusers_uid = [ i[0] for i in db.session.query(Users.uid) ]  # выборка uid из локальной базы PostgreSQL

    users_uid = query_with_users_uid() # выборка uid из базы Abills
    users_uid = [ i['uid'] for i in users_uid ]
    s = set(lusers_uid) ^ set(users_uid) # Сортировка и удаление существующих uid 
    users = [ query_with_user(uid=i)[0] for i in s ]
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
        u.append(user) # для логирования и вывод в представление
    # создаем словарь с данными пользователя
        uu = Users(uid=user.get('uid'),
                login=user.get('login'),
                password=user.get('password').decode('utf-8'),
                fio=user.get('fio'),
                phone=user.get('phone'),
                descr=user.get('descr'),
                disable=user.get('disable'),
                delete=user.get('deleted'))
        db.session.add(uu) # добаляем в базу PostgreSQL
    db.session.commit() # сохраняем в базу PostgreSQL
    return render_template('users/index.html',users=u)
