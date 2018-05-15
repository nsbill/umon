from app import db
from models import Users, Address, Networks, Groups, Tarifs, UsersPI, SortStreet, SortBuild, SortFlat, SelectAdressUid
import sys
import time
sys.path.insert(0, '/app/db')
sys.path.insert(0, '/app/users')

from mysql_select import query_with_allusers, query_with_user, query_with_users_uid, query_with_tarifs, query_with_tarif_tpid, query_with_groups, query_with_group_gid,query_with_user_uid

def all_users():
    ''' Выборка всех пользователей из базы PostgreSQL '''
    UsersALL =[ i for i in db.session.query(Users,Address,Networks,UsersPI)
		.filter(Users.uid == Address.uid,
			Users.uid == Networks.uid,
			Users.uid == UsersPI.uid).all()]
    return UsersALL

def user_data(uid):
    ''' Выборка пользователя с таб. users из PostgreSQL '''
    user = Users.query.filter_by(uid=uid).first()
    return user

def select_address(uid):
    ''' Выборка адреса пользователя'''
    a = SelectAdressUid.query.filter_by(uid=uid).first()
    s = SortStreet.query.filter_by(street_id=a.street_id).first()
    b = SortBuild.query.filter_by(build_id=a.build_id).first()
    f = SortFlat.query.filter_by(flat_id=a.flat_id).first()
    adr = [s.name,b.number_build,b.pref_build,f.number_flat,f.pref_flat]
    return adr

def users_info(street_id):
    street_id_users = SelectAdressUid.query.filter_by(street_id=street_id).all()     # Список улиц
    list_users_uid = [ i.uid for i in street_id_users  ]                              # Список UID
    adr_list = [[uid, select_address(uid)] for uid in list_users_uid]                # Список адрессов
    adr_list.sort(key=lambda i: i[1])                                                # Сортировка списка адрессов
    sort_adr_uid = [i[0] for i in adr_list]                                          # Список отсортированных адрессов для получения UID
    users = [ user_data(uid=uid) for uid in sort_adr_uid  ]                           # Список пользователей
    return users

def user_info(uid):
    ''' Выборка данных о пользователе по UID и обновлнение данных '''
    def upd_user(*args):
        us = args[1][0]
        adr = args[1][1]
        netw = args[1][2]
        userpi =args[1][3]
        db.session.query(Users).filter(Users.uid == args[0]).update(us)
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
    return UserInfo

def search(func):
    '''Поиск'''
    def allstreet():
        '''Выборка улиц, сортировка и вывод в список [заглавная буква, улица, street_id]'''
        all_st = SortStreet.query.all()
        allstreet = [ (street.name,street.street_id) for street in all_st] #   
        street = [ (i[0][0],i[0],i[1]) for i in allstreet if i[0] != '' ]
        street.sort()
        return street

    def street_letters(add = None):
        '''Функция для сортировки улиц по заглавной букве с выводом в словарь'''
        street_letters = {}
        litters = [ i[0] for i in add ] # выборка заглавных букв
        litters = list(set(litters))    # удаляем дубликаты и создваем список
        litters.sort()                  # сортировка списка
        for item in add:                # создание словаря улиц по каждой заглавной букве улицы
          for i in litters:
            if item[0] == i:
              street_letters.setdefault(item[0],[]).append((item[1],item[2]))
        return street_letters

    def allbuild():
        allbuild = SortBuild.query.all()
        return allbuild

    def allflat():
        allflat = SortFlat.query.all()
        return allflat

    all_street = allstreet()                              # получаем список всех улиц
    list_street_letters = street_letters(add=all_street)  # получаем словарь улиц
    return all_street, list_street_letters

def litters_street(func):
    ''' Список адрессов и словарь улиц по заглавной букве '''
    def list_street():
        ''' Cписок улиц'''
        streets = search(list_street)
        return streets
    liststreet = list_street()              # Список улиц
    list_streetletters = liststreet[1]      # Словарь улиц по заглавной букве 
    return list_streetletters, liststreet

