from flask import Blueprint
from flask import render_template,request,redirect
from datetime import datetime
import sys
sys.path.insert(0, '/app/users')
from users_impfunc import search, litters_street, all_users, users_info, user_info, user_data, select_address, upd_user, user_online, users_online, search_user, search_cid, count_street_online

from flask_security import login_required
users = Blueprint('clients',__name__, template_folder='templates')

@users.route('/all', methods=['GET'])
@login_required
def index():
    ''' Выборка всех пользователей из базы PostgreSQL '''
    page = request.args.get('page')
    All_Users = all_users(page=page)
    UsersALL = [ user for user in All_Users.items ]
    if All_Users.page <= All_Users.pages:
        page_next = All_Users.page + 10
    else:
        page_next = All_Users.page - 10
    return render_template('users/index.html', UsersALL=UsersALL, pages=All_Users, page_next=page_next)


@users.route('/error', methods=['GET'])
def error():
    '''Выдавать страницу ошибки 404'''
    return render_template('users/error.html')

@users.route('/user/<uid>', methods=['GET'])
@login_required
def user(uid):
    ''' Выборка данных о пользователе по UID '''
    UserInfo = user_info(uid)
    UserOnLine = user_online(uid)
    return render_template('users/userinfo.html', UserInfo=UserInfo, UserOnLine=UserOnLine, DateTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@count_street_online
@litters_street
@search
@users.route('/adr/search', methods=['GET','POST'])
@login_required
def search_street():
    if request.method == 'POST':
        result = request.form
#        print(result.values())
        street_id = [ i for i in result.values()]
#        print(street_id)
        return redirect('users/adr/street_id/'+street_id[0])
    else:
        result = []
    liststreet = litters_street(search_street)
    def i():
        return i
    count_street = count_street_online(i)
    return render_template('users/search.html', ListSearch=liststreet[1][0], ListStreetLetters=liststreet[0].items(), DateTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), Count_Street=count_street)

@litters_street
@count_street_online
@search
@users.route('/adr/street_id/<street_id>', methods=['GET'])
@login_required
def street_id_users(street_id):
    def lstr():
        ''' Фун-ция для декоратора litters_street '''
        return lstr
    liststreet = litters_street(lstr)   # Cписок улиц и словарь улиц по заглавной букве
    users_data = users_info(street_id)  # Словарь пользователей выбранных по улице
    uon = users_online()                # Словарь онлайн пользователей с данными подключения
    online = []                         # Создаем список онлайн пользователей по uid 
    for item in users_data:
        for i in uon:
            if item.uid == i.get('uid'):
                for a in item.address_id:
                    i['street'] = a.street
                    i['building'] = a.building
                    i['flat'] = a.flat
                online.append( i )
    def i():
        return i
    count_street = count_street_online(i)
    count_street_online_users = []
    for i in count_street:
        if int(street_id) == i[0][1]:
            count_street_online_users.append(i)
    return render_template('users/street_users.html', StreetUsers=street_id_users, ListSearch=liststreet[1][0], ListStreetLetters=liststreet[0].items(), Users=users_data,UsersOnline=online, Count_Street=count_street_online_users)

@litters_street
@search
@users.route('search', methods=['GET'])
@login_required
def searchuser():
    '''Поиск универсальный'''
    search = request.args.get('search')
    if search:
        query = search_user(search)
    else:
        query = []
    liststreet = litters_street(search_street)
    return render_template('users/search_user.html',Users=query,ListSearch=liststreet[1][0], ListStreetLetters=liststreet[0].items())

@litters_street
@search
@users.route('cid', methods=['GET'])
@login_required
def searchcid():
    '''Поиск МАС адресса '''
    search = request.args.get('cid')
    if search:
        query = search_cid(search)
    else:
        query = []
    liststreet = litters_street(search_street)
    return render_template('users/search_cid.html', Users=query,ListSearch=liststreet[1][0], ListStreetLetters=liststreet[0].items())
