from app import db
from flask import Blueprint
from flask import render_template
from datetime import datetime
import sys
import time
sys.path.insert(0, '/app/db')
sys.path.insert(0, '/app/importation')
from impfunc import sort_list_text, sort_list_num, select_street, select_build, select_flat, select_sbf, insert_sbf, mtm_sbf, all_adr
from abills_select import query_streetsbuildflat

from mysql_select import query_with_allusers, query_with_user, query_with_users_uid, query_with_tarifs, query_with_tarif_tpid, query_with_groups, query_with_group_gid, query_with_user_uid
import subprocess
from models import Users, Address, Networks, Groups, Tarifs, UsersPI, SortStreet, SortBuild, SortFlat, SelectAdressUid

imp = Blueprint('importation',__name__, template_folder='templates')

@imp.route('/')
def index():
    ''' Import Abills Address Users'''
    street_build_flat = query_streetsbuildflat()    # выборка с базы abills всех ул. домов кв.
    streets = SortStreet.query.all()                # выборка улиц из базы PostgreSQL
    builds = SortBuild.query.all()                  # выборка домов из базы PostgreSQL
    flats = SortFlat.query.all()                    # выборка квартир из базы PostgreSQL
    list_streets = select_street(streets)           # сортировка улиц
    list_builds = select_build(builds)              # cортировка домов
    list_flats = select_flat(flats)                 # сортировка квартир
    sort_streets = select_sbf(street_build_flat,'street')   # выборка только улиц
    sort_builds = select_sbf(street_build_flat,'build')     # выборка только дома
    sort_flats = select_sbf(street_build_flat,'flat')       # выборка только кв
    insert_sbf(sort_streets,list_streets,'street')          # добавляем в базу PostgreSQL новые улицы
    insert_sbf(sort_builds,list_builds,'build')             # добавляем в базу PostgreSQL новые дома
    insert_sbf(sort_flats,list_flats,'flat')                # добавляем в базу PostgreSQL новые кв
    return render_template('imp/index.html', import_data=(sort_streets,sort_builds,sort_flats))

@imp.route('/mtm_sbf')
def manytomany_sbf():
    ''' Добавляем ManyToMany в street_build, build_flat '''
    street_build_flat = query_streetsbuildflat()    # выборка с базы abills всех ул. домов кв.
    mtm_sb = SortStreet.query.all()                 # выборка с базы PostgreSQL улиц
    mtm_bf = SortBuild.query.all()                  # выборка с бызы PostgreSQL домов
    mtm_sbf(street_build_flat,mtm_sb,mtm_bf)        # добавляем ManyToMany street,build,flat
    info = 'Done Many-To-Many Streets,Builds,Flats' # информационная запись об завершение
    return render_template('imp/index.html', import_data=info)

@imp.route('/all_adr')
def select_address():
    ''' Выборка с всех записей с таб. address '''
    street_build_flat = query_streetsbuildflat()    # выборка с базы abills всех ул. домов кв.
    info = all_adr(street_build_flat)
    return render_template('imp/index.html', import_data=info)

@imp.route('/addusers')
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
        user[1].update(uid=i)                                   # обновление адрес пользователя из базы Abills
        db.session.bulk_insert_mappings(Address,[user[1]])
        user[2].update(uid=i)                                   # обновление сетевые настройки польз. из базы Abills
        db.session.bulk_insert_mappings(Networks,[user[2]])
        user[3].update(uid=i)                                   # обновление информац о пользателе из базы Abills
        db.session.bulk_insert_mappings(UsersPI,[user[3]])
        db.session.commit()                                     # записать выбранные данные в базу PostgreSQL
    return render_template('imp/addusers.html',Tarifs='Все тарифы добавлены',Groups='Все группы добавлены',Users='Все пользователи добавлены')
