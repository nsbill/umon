from app import db
from models import SortStreet, SortBuild, SortFlat
import sys
sys.path.insert(0, '/app/db')


def select_street(args):
    '''создание списка улиц c таб. SortStreet  PostgreSQL '''
    streets = [ street.name for street in args ]
    streets.sort()
    return streets

def select_build(args):
    '''создание списка домов c таб. SortBuild  PostgreSQL '''
    builds = [ (build.number_build, build.pref_build) for build in args ]
    builds = list(set(builds))
    builds.sort()
    return builds

def select_flat(args):
    '''создание списка улиц c таб. SortFlat PostgreSQL '''
    flats = [ (flat.number_flat, flat.pref_flat) for flat in args ]
    flats = list(set(flats))
    flats.sort()
    return flats

def sort_list_num(args):
    '''Сортируем числа по возр. и убираем дубликаты'''
    list_num = list(set(args))
    list_num.sort()
    return list_num

def sort_list_text(args):
    '''Сортируем текст по возр., перевод в верхний регистр каждое слово и убираем дубликаты'''
    list_text = list(set({ i.title() for i in set(args) }))
    list_text.sort()
    return list_text

def select_sbf(args=None, item='None'):
    '''Вывод отсортированного списка
        - ул.дом.кв --> [{'street': 'Железнодорожный', 'build': (4, '0'), 'flat': (12, '0')}]
        - улицы --> ['Железнодорожный']
        - дом --> [(4, '0')]
        - кв --> [(12, '0')]
    '''
    if args is not None:
        if type(args) != list:
            return []
        all_sbf = [ sbf for sbf in args if type(sbf) == dict ]

        if item == 'street':
            i = [ item['street']for item in args ]
            street = sort_list_text(i)
            street.sort()
            return street

        if item == 'build':
            build = [ item['build'] for item in args ]
            build = list(set(build))
            build.sort()
            return build

        if item == 'flat':
            flat = [ item['flat'] for item in args ]
            flat = list(set(flat))
            flat.sort()
            return flat
    else:
        return []
    return all_sbf


def insert_sbf(db_abills_items, db_list_items, item=None):
    '''Добавляем в бызу PostgreSQL ул. дом кв'''
    list_items = set(db_abills_items) - set(db_list_items)
    if list_items is not None:
        if item == 'street':
            for street in list_items:                                                   # Добавляем не сущ. улиц в PostgreSQL
                db.session.close()
                db.session.add(SortStreet(name=street))
                db.session.commit()
        if item == 'build':
            for build in list_items:                                                    # Добавляем не сущ. дома в PostgreSQL
                db.session.close()
                db.session.add(SortBuild(number_build=build[0],pref_build=build[1]))
                db.session.commit()
        if item == 'flat':
            for flat in list_items:                                                     # Добавляем не сущ. квартиры в PostgreSQL
                db.session.close()
                db.session.add(SortFlat(number_flat=flat[0],pref_flat=flat[1]))
                db.session.commit()

def mtm_street(sbf):
    pass

#def adr_mtm(uid=None):
#    '''Добавляет manytomany ул. дом кв и в таб. adr_uid'''
#    if uid is not None:
#        db.session.close()
#        for i in uid:
#            adruid = select_address_uid(uid=i)
#            print('-=adruid=-'*7)
#            print(adruid)
#            street = adruid[0]
#            print(street)
#            build = adruid[1]
#            print(build)
#            flat = adruid[2]
#            print(flat)
#
#            add_adr_uid(st=street,bt=build,ft=flat,uid=i)            # добавляем в таб adr_uid 
#
#            addstrbuild = build in street.building
#            if addstrbuild == False:
#                build.streetbuild.append(street)
#                db.session.commit()
#
#            addbuildflat = flat in build.flat
#            if addbuildflat == False:
#                flat.buildflat.append(build)
#                db.session.commit()
#
