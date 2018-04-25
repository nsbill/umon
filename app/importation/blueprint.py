from app import db
from flask import Blueprint
from flask import render_template
from datetime import datetime
import sys
import time
sys.path.insert(0, '/app/db')
sys.path.insert(0, '/app/importation')
from impfunc import sort_list_text, sort_list_num, select_street, select_build, select_flat, select_sbf, insert_sbf
from abills_select import query_streetsbuildflat

from mysql_select import query_with_allusers, query_with_user, query_with_users_uid, query_with_tarifs, query_with_tarif_tpid, query_with_groups, query_with_group_gid, query_with_user_uid
import subprocess
from models import Users, Address, Networks, Groups, Tarifs, UsersPI, SortStreet, SortBuild, SortFlat, SelectAdressUid

imp = Blueprint('importation',__name__, template_folder='templates')

@imp.route('/')
def index():
    ''' Import Abills '''
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
    insert_sbf(sort_streets,list_streets,'street')          # добаляем в базу PostgreSQL новые улицы
    insert_sbf(sort_builds,list_builds,'build')             # добаляем в базу PostgreSQL новые дома
    insert_sbf(sort_flats,list_flats,'flat')                # добаляем в базу PostgreSQL новые кв
    return render_template('imp/index.html', import_data=(list_streets,list_builds,list_flats))



#
#
#def InSortListNum(args):
#    '''Сортируем по возр. и убираем дубликаты'''
#    list_num = list(set(args))
#    list_num.sort()
#    return list_num
#
#def InSortListText(args):
#    '''Сортируем по возр., перевод в верхний регистр каждое слово и убираем дубликаты'''
#    list_text = list(set({ i.title() for i in set(args)}))
#    list_text.sort()
#    return list_text

#@users.route('/')
#def index():
#    ''' Выборка всех пользователей из базы PostgreSQL '''
#    UsersALL =[ i for i in db.session.query(Users,Address,Networks,UsersPI)
#                                            .filter(Users.uid == Address.uid,
#                                                    Users.uid == Networks.uid,#
#                                                    Users.uid == UsersPI.uid).all()]
#    return render_template('users/index.html', UsersALL=UsersALL)
#
#@users.route('/user/<uid>')
#def user(uid):
#    ''' Выборка данных о пользователе по UID '''
#    def upd_user(*args):
#        print(*args)
#        us = args[1][0]
#        adr = args[1][1]
#        netw = args[1][2]
#        userpi =args[1][3]
#        db.session.query(Users).filter(Users.uid == args[0]).update(us)
#        db.session.query(Address).filter(Address.uid == args[0]).update(adr)
#        db.session.query(Networks).filter(Networks.uid == args[0]).update(netw)
#        db.session.query(UsersPI).filter(UsersPI.uid == args[0]).update(userpi)
#        db.session.commit()

#    ii = query_with_user_uid(uid)
#    upd_user(uid, ii)
#    UserInfo =[ i for i in db.session.query(Users,Address,Networks,UsersPI,Tarifs,Groups)
#                                            .filter(Users.uid == uid,
#                                                Address.uid == uid,
#                                                Networks.uid == uid,
#                                                UsersPI.uid == uid,
#                                                Tarifs.tpid == Users.tarifs_id,
#                                                Groups.gid == Users.groups_id).first()]
#    return render_template('users/userinfo.html', UserInfo=UserInfo, DateTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#
#def search(func):
#    '''Поиск'''
#    def allstreet():
#        '''Выборка улиц, сортировка и вывод в список [заглавная буква, улица, street_id]'''
#        all_st = SortStreet.query.all()
#        allstreet = [ (street.name,street.street_id) for street in all_st] #  
#        street = [ (i[0][0],i[0],i[1]) for i in allstreet if i[0] != '' ]
#        street.sort()
#        return street
#
#    def street_letters(add = None):
#        '''Функция для сортировки улиц по заглавной букве с выводом в словарь'''
#        street_letters = {}
#        litters = [ i[0] for i in add ] # выборка заглавных букв
#        litters = list(set(litters))    # удаляем дубликаты и создваем список
#        litters.sort()                  # сортировка списка
#        for item in add:                # создание словаря улиц по каждой заглавной букве улицы
#            for i in litters:
#                if item[0] == i:
#                    street_letters.setdefault(item[0],[]).append((item[1],item[2]))
#        return street_letters
#
#    def allbuild():
#        allbuild = SortBuild.query.all()
#        return allbuild
#
#    def allflat():
#        allflat = SortFlat.query.all()
#        return allflat
#
#    all_street = allstreet()                # получаем список всех улиц
#    list_street_letters = street_letters(add=all_street)  # получаем словарь улиц
#    return all_street, list_street_letters
#
#@search
#@users.route('/adr/search')
#def search_street():
#    def list_street():
#        street = search(list_street)
#        return street
#    liststreet = list_street()      # Список улиц
#    list_streetletters = liststreet[1]  # Осортированный словарь улиц по заглавной букве 
#    return render_template('users/search.html', ListSearch=liststreet[0], ListStreetLetters=list_streetletters.items(), DateTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#
#@search
#@users.route('/adr/street_id/<street_id>')
#def street_id_users(street_id):
#    def list_street():
#        street = search(list_street)
#        return street
#    liststreet = list_street()      # Список улиц
#    list_streetletters = liststreet[1]  # Осортированный словарь улиц по заглавной букве 
#    street_id_users = SelectAdressUid.query.filter_by(street_id=street_id).all()
#    list_users_uid = [ i.uid for i in street_id_users ]
#
#    def user(uid):
#        user = Users.query.filter_by(uid=uid).first()
#        return user
#
#    users = [ user(uid=uid) for uid in list_users_uid ]
#    print('--users--'*10)
#    user = users[0]
#    users_info = [ (user.login,user.fio,user.phone,
#                   [(i.balance, i.credit) for i in user.users_pi],
#                   [(i.street, i.building, i.flat) for i in user.address_id],) for user in users ]
#
#    def sort_users_info_street(user):
#        return user[4][0][1]
##    dict(zip(('login','fio','phone','balance','credit','street','building','flat'),
#    users_info.sort(key=sort_users_info_street)
#    print(users_info)
#
#    def selection_sort(ar):
#        length = len(ar)
#        for i in range(length):
#            x = i
#            for z in range(x + 1, length):
#                if ar[x] > ar[z]:
#                    x = z
#            ar[i], ar[x] = ar[x], ar[i]
#        return ar
#
##    sorted(users.items(), key=lambda item: item[1]) # Упорядочим элементы словаря по значениям.
##    s = [ i for i in users ]
##    print('s'*10)
##    print(s)
#    str_sort_num = [ number_build[4][0][1] for number_build in users_info ]
#    print(str_sort_num)
#    users_info = selection_sort(str_sort_num)
##    users_info = [selection_sort(i) for i in str_sort_num]
#    return render_template('users/street_users.html', UserInfo=users_info, StreetUsers=street_id_users, ListSearch=liststreet[0], ListStreetLetters=list_streetletters.items(), Users=users)
#
#
#
#
#@users.route('/adr/sortadr')
#def sort_adr():
#    def input_num(sort_num=None):
#        '''Отделить тип int и str в номере дома или квартиры
#           Пример: '100a' >>>  (100,'a')
#        '''
#        print('---=main=---'*7)
#        print(sort_num)
#        if sort_num is not None:
#            if sort_num[0] != '':
#                s = 0
#                sort_build_num = []
#                try:
#                  for i in sort_num[0]:
#                      int(i)
#                      s = s + 1
#                      print('---sort_num---'*7)
#                      print(sort_num)
#                  return (sort_num[0],'',)
#                except ValueError:
#                  sort_build_num.append((sort_num[0][:s], sort_num[0][s:]))
#                  print('---sort_build_num---'*7)
#                  print(sort_build_num)
#                  if sort_build_num[0][0] == '':
#                    return (0, sort_build_num[0][1])
#                  return sort_build_num[0]
#        isnot = (0, sort_num)
#        print('--isnot--'*8)
#        print(isnot)
#        return isnot
#
#    def select_address():
#        '''Выборка ул, дом, кв из таб. Address и добавление в таб. SortStreet, SortBuild, SortFlat
#            - стравниваем списки и удаляем дубликаты
#        '''
#        item_street = set([ i for i in db.session.query(Address.street)])            # Выборка всех улиц и убираем дубликаты улиц
#        item_build = set([ i for i in db.session.query(Address.building)])           # Выборка всех улиц и убираем дубликаты домов
#        item_flat = set([ i for i in db.session.query(Address.flat)])                # Выборка всех улиц и убираем дубликаты квартир
#        item_sort_street = set([i for i in db.session.query(SortStreet.name)])       # Выборка сортированных названий улиц 
#        item_sort_build = set([i for i in db.session.query(SortBuild.number_build)]) # Выборка сортированных номеров домов 
#        item_sort_flat = set([i for i in db.session.query(SortFlat.number_flat)])    # Выборка сортированных номеров квартир
#
#        list_street = set(item_street) - set(item_sort_street)                       # Создаем список улиц для добавление в SortStreet
#        list_build = set(item_build) - set(item_sort_build)                          # Создаем список улиц для добавление в SortBuild
#        list_flat = set(item_flat) - set(item_sort_flat)                             # Создаем список улиц для добавление в SortFlat
#        return list_street, list_build, list_flat
#
#    def add_adr(list_street=None, list_build=None, list_flat=None):
#        '''Добавление ул дом кв в таб. SortStreet, SortBuild, SortFlat '''
#        if list_street is not None:
#            for i in list_street:                                                                  # Добавляем не сущ. улицу
#                db.session.close()
#                db.session.add(SortStreet(name=i[0]))
#                db.session.commit()
#
#        if list_build is not None:
#            for i in list_build:                                                                  # Добавляем не сущ. дом
#                db.session.close()
#                build = input_num(i)
#                db.session.add(SortBuild(number_build=build[0],pref_build=build[1]))
#                db.session.commit()
#
#        if list_flat is not None:
#            for i in list_flat:                                                                  # Добавляем не сущ. кв. 
#                db.session.close()
#                flat = input_num(i)
#                db.session.add(SortFlat(number_flat=flat[0],pref_flat=flat[1]))
#                db.session.commit()
#
#    def select_adress_all():
#        '''Выборка всех  uid,street,building,flat из таб. Address '''
#        all_address = Address.query.all()
#        list_all_address = set([(i.uid,i.street,i.building,i.flat) for i in all_address])
#        uid = [i[0] for i in list_all_address]  # Выборка UID
#        return list_all_address, uid
#
#    def select_adr_all():
#        '''Выборка всех  uid,street,building,flat из таб. SelectAdressUid '''
#        adr_all = SelectAdressUid.query.all()
#        list_adr_all = set([(i.uid,i.street_id,i.build_id,i.flat_id) for i in adr_all])
#        uid = [i[0] for i in list_adr_all]  # Выборка UID
#        return list_adr_all, uid
#
#    def select_address_uid(uid=None):
#        '''Выборка из локальной базы PostgreSQL по uid с таб address'''
#        db.session.close()
#        if uid is not None:
#            a = Address.query.filter_by(uid=uid).all()
#            ab = [ (i.uid, i.street, i.building, i.flat) for i in a ]
#            print('--==ab==---'*7)
#            print(ab)
#            st = db.session.query(SortStreet).filter(SortStreet.name == ab[0][1]).first()
#            build_num = input_num([ab[0][2]])
#            flat_num = input_num([ab[0][3]])
#            print(build_num)
#            test = db.session.query(SortBuild).filter(SortBuild.number_build == build_num[0]).filter(SortBuild.pref_build == build_num[1]).first()
#            print('==test=='*7)
#            print(test)
#            ftest = db.session.query(SortFlat).filter(SortFlat.number_flat == flat_num[0]).filter(SortFlat.pref_flat == flat_num[1]).first()
#            print('==ftest=='*7)
#            print(ftest)
#            if build_num[0]:
#                bt = db.session.query(SortBuild).filter(SortBuild.number_build == build_num[0]).filter(SortBuild.pref_build == build_num[1]).first()
#            else:
#                bt = db.session.query(SortBuild).filter(SortBuild.number_build == 0).filter(SortBuild.pref_build == build_num[1]).first()
#
#            if flat_num[0]:
#                ft = db.session.query(SortFlat).filter(SortFlat.number_flat == flat_num[0]).filter(SortFlat.pref_flat == flat_num[1]).first()
#            else:
#                ft = db.session.query(SortFlat).filter(SortFlat.number_flat == 0).filter(SortFlat.pref_flat == flat_num[1]).first()
#
#            print('=bt='*8)
#            print(bt)
#            print('=ft='*8)
#            print(ft)
#        return st, bt, ft
#
#    def add_adr_uid(st,bt,ft,uid=None):
#        '''Добавить пользователя в теб. adr_uid'''
#        if uid is not None:
#            au = SelectAdressUid.query.filter_by(uid=uid).all()                 # Выборка из таб пользов.
#            if au == []:                                                  # Если отсутствует польз добавить.
#                db.session.add(SelectAdressUid(uid=uid,street_id=st.street_id,build_id=bt.build_id,flat_id=ft.flat_id))
#                db.session.commit()
#
#    def adr_mtm(uid=None):
#        '''Добавляет manytomany ул. дом кв и в таб. adr_uid'''
#        if uid is not None:
#            db.session.close()
#            for i in uid:
#                adruid = select_address_uid(uid=i)
#                print('-=adruid=-'*7)
#                print(adruid)
#                street = adruid[0]
#                print(street)
#                build = adruid[1]
#                print(build)
#                flat = adruid[2]
#                print(flat)
#
#                add_adr_uid(st=street,bt=build,ft=flat,uid=i)            # добавляем в таб adr_uid 
#
#                addstrbuild = build in street.building
#                if addstrbuild == False:
#                    build.streetbuild.append(street)
#                    db.session.commit()
#
#                addbuildflat = flat in build.flat
#                if addbuildflat == False:
#                    flat.buildflat.append(build)
#                    db.session.commit()
#
#    sort = select_address()             # выборка и сортировка
#    add_adr(list_street=sort[0],list_build=sort[1],list_flat=sort[2]) # доваление новых адресов
#
#    saa1 = select_adress_all()
#    print('---saa1==='*7)
#    print(saa1)
#    saa2 = select_adr_all()
#    print('---saa2==='*7)
#    print(saa2)
#    diff = set(saa1[1]) - set(saa2[1]) # сравнения и поиск новых учетных записей по UID
#    print('-==diff==-'*7)
#    print(diff)
#    adr_mtm(uid=tuple(diff))
#    return render_template('users/address.html', AddItemStreet=sort[0], AddItemBuild=sort[1], AddItemFlat=sort[2], DateTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#
#@users.route('/addusers')
#def addusers():
#    ''' Перенос пользователей, тарифных планов, групп из базы Abills '''
##Tarifs
#    ltpid = [ i[0] for i in db.session.query(Tarifs.tpid) ] # выборка tpid из локальной базы PostgreSQL
#    tarifs = query_with_tarifs()                            # выборка тарифных планов из базы Abills
#    tp_id = [i['tpid'] for i in tarifs]                     # выборка tpid из базы Abills
#    s = set(ltpid) ^ set(tp_id)                             # Сортировка и удаление существующих tpid
#    for i in s:                                             # выборка тариф по tpid из базы Abills
#        db.session.close()                                  # закрыть сессии если сущ
#        tp = query_with_tarif_tpid(i)                       # выборка tpid из бызы Abills 
#        db.session.bulk_insert_mappings(Tarifs,[tp[0]])     # вставка в базу PostgreSQL
#        db.session.commit()
#
#    lgid = [ i[0] for i in db.session.query(Groups.gid) ]   # выборка gid из локальной базы PostgreSQL
#    g0 = Groups.query.filter_by(gid=0).first()
#    if g0 == None:
#        gr0 = Groups(gid=0, name='', descr='')              # Добавляем группу 0
#        db.session.add(gr0)
#        db.session.commit()                                 # сохраняем в базу PostgreSQL
##Groups
#    groups = query_with_groups()                            # выборка тарифных планов из базы Abills
#    gr_id = [i['gid'] for i in groups]                      # выборка gid из базы Abills
#    g = set(lgid) ^ set(gr_id)                              # Сортировка и удаление существующих gid
#    for i in g:                                             # выборка тариф по tpid из базы Abills
#        db.session.close()                                  # закрыть существующие сессии
#        if i == 0:
#            i = 'Уже существует'
#        else:
#            gr = query_with_group_gid(i)                        # выборка gid из бызы Abills 
#            db.session.bulk_insert_mappings(Groups,[gr[0]])     # вставка в базу PostgreSQL
#            db.session.commit()
##Users
#    lusers_uid = [ i[0] for i in db.session.query(Users.uid) ]  # выборка uid из локальной базы PostgreSQL
#    users_uid = query_with_users_uid()                          # выборка uid из базы Abills
#    users_uid = [ i['uid'] for i in users_uid ]
#    s = set(lusers_uid) ^ set(users_uid)                        # Сортировка и удаление существующих uid 
#    for i in s:                                                 # добавление пользователя в PostgreSQL
#        db.session.close()                                      # закрыть существующие сессии
#        user = query_with_user_uid(uid=i)                       # выборка пользователя их базы Abills по uid
#        db.session.bulk_insert_mappings(Users,[user[0]])        # создание сесси для добавления в PostgreSQL
#        user[1].update(uid=i)                                   # обновление адрес пользователя из базы Abills
#        db.session.bulk_insert_mappings(Address,[user[1]])
#        user[2].update(uid=i)                                   # обновление сетевые настройки польз. из базы Abills
#        db.session.bulk_insert_mappings(Networks,[user[2]])
#        user[3].update(uid=i)                                   # обновление информац о пользателе из базы Abills
#        db.session.bulk_insert_mappings(UsersPI,[user[3]])
#        db.session.commit()                                     # записать выбранные данные в базу PostgreSQL
#    return render_template('users/addusers.html',Tarifs='Все тарифы добавлены',Groups='Все группы добавлены',Users='Все пользователи добавлены')
