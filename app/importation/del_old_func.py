#def sort_street(args):
#    '''Список отсортированных улиц'''
#    if type(args) == dict:
#        i = [ street['street']for street in args  ]
#        street = sort_list_text(i)
#        street.sort()
#        return street
#
#def sort_build(args):
#    '''Список отсортированных домов'''
#    if type(args) == dict:
#        build = [ item['build'] for item in args  ]
#        build = list(set(build))
#        build.sort()
#        return build
#
#def sort_flat(args):
#    '''Список отсортированных квартир'''
#    if type(args) == dict:
#        flat = [ item['flat'] for item in args  ]
#        flat = list(set(flat))
#        flat.sort()
#        return flat

#                if args in ",".join(list_street):
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
  
