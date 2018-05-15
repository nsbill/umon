from app import db
from models import SortStreet, SortBuild, SortFlat, Address, SelectAdressUid
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
            street = [ item['street']for item in args ]
            street = sort_list_text(street)
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

def mtm_sbf(args=None,mtm_sb=None,mtm_bf=None):
    '''Добавить в ManyToMany street and build'''
    if args is not None:
        if type(args) != list:
            return []
        all_sbf = [ sbf for sbf in args if type(sbf) == dict ]
        streets = [ item['street'] for item in all_sbf ]
        builds = [ item['build'] for item in all_sbf ]
        for i in all_sbf:
            for street in set(streets):
                if street == i['street']:
                    build = i['build']
                    s_mtm = db.session.query(SortStreet).filter(SortStreet.name == street.title()).first()
                    b_mtm = db.session.query(SortBuild).filter(SortBuild.number_build == build[0]).filter(SortBuild.pref_build == build[1]).first()
#                    s_mtm = SortStreet.query.filter_by(name=street.title()).first()
#                    b_mtm = SortBuild.query.filter_by(number_build=build[0]).filter_by(pref_build=build[1]).first()
                    addstrbuild = b_mtm in s_mtm.building
                    if addstrbuild == False:
                        b_mtm.streetbuild.append(s_mtm)
                        db.session.commit()
                        db.session.close()
            for build in set(builds):
                if build  == i['build']:
                    build = i['build']
                    flat = i['flat']
                    b_mtm = db.session.query(SortBuild).filter(SortBuild.number_build == build[0]).filter(SortBuild.pref_build == build[1]).first()
                    f_mtm = db.session.query(SortFlat).filter(SortFlat.number_flat == flat[0]).filter(SortFlat.pref_flat == flat[1]).first()
#                    b_mtm = SortBuild.query.filter_by(number_build=build[0]).first()
#                    f_mtm = SortFlat.query.filter_by(number_flat=flat[0]).filter_by(pref_flat=flat[1]).first()

                    addbuildflat = f_mtm in b_mtm.flat
                    if addbuildflat == False:
                        f_mtm.buildflat.append(b_mtm)
                        db.session.commit()
                        db.session.close()

def all_adr(args):
    '''  Выборка с всех записей с таб. address '''
    list_all_uid_address = [ item.uid for item in Address.query.all()]          # Список uid из таб. address
    list_all_uid_adr = [ item.uid for item in SelectAdressUid.query.all()]      # Список uid из таб. adr_uid
    all_adr = select_sbf(args)
    list_adr = []
    for item in all_adr:
        street = SortStreet.query.filter_by(name=item['street'].title()).first()
        build = SortBuild.query.filter_by(number_build=item['build'][0]).filter_by(pref_build=item['build'][1]).first()
        flat =  SortFlat.query.filter_by(number_flat=item['flat'][0]).filter_by(pref_flat=item['flat'][1]).first()
        uid = item['uid']
        if uid not in list_all_uid_adr:
            if uid in list_all_uid_address:
                db.session.add(SelectAdressUid(uid=item['uid'],street_id=street.street_id,build_id=build.build_id,flat_id=flat.flat_id))
                db.session.commit()
        list_adr.append([[street.street_id,item['street']],[build.build_id,item['build']],[flat.flat_id,['flat_id']]])
    return list_adr

def adr_uid():
    pass

