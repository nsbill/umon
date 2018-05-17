from flask import Blueprint
from flask import render_template,request,redirect
from datetime import datetime
import sys
sys.path.insert(0, '/app/users')
from users_impfunc import search, litters_street, all_users, users_info, user_info, user_data, select_address, upd_user, user_online, users_online

users = Blueprint('users',__name__, template_folder='templates')


@users.route('/', methods=['GET'])
def index():
    ''' Выборка всех пользователей из базы PostgreSQL '''
    UsersALL = all_users()
    return render_template('users/index.html', UsersALL=UsersALL)

@users.route('/user/<uid>', methods=['GET'])
def user(uid):
    ''' Выборка данных о пользователе по UID '''
    UserInfo = user_info(uid)
    return render_template('users/userinfo.html', UserInfo=UserInfo, DateTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@litters_street
@search
@users.route('/adr/search', methods=['GET','POST'])
def search_street():
    if request.method == 'POST':
        result = request.form
        print(result.values())
        street_id = [ i for i in result.values()]
        print(street_id)
        return redirect('users/adr/street_id/'+street_id[0])
    else:
        result = []
    liststreet = litters_street(search_street)
    return render_template('users/search.html', ListSearch=liststreet[1][0], ListStreetLetters=liststreet[0].items(), DateTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@litters_street
@search
@users.route('/adr/street_id/<street_id>', methods=['GET'])
def street_id_users(street_id):
    def lstr():
        ''' Фун-ция для декоратора litters_street '''
        return lstr
    liststreet = litters_street(lstr)   # Cписок улиц и словарь улиц по заглавной букве
    users_data = users_info(street_id)
#    users_online = [ user_online(item.uid) for item in users_data ]
    uon = users_online()
    online = [] # Список онлайн пользователей по uid 
    for item in users_data:
        for i in uon:
            if item.uid == i.get('uid'):
                for a in item.address_id:
                    i['street'] = a.street
                    i['building'] = a.building
                    i['flat'] = a.flat
                online.append( i )
    return render_template('users/street_users.html', StreetUsers=street_id_users, ListSearch=liststreet[1][0], ListStreetLetters=liststreet[0].items(), Users=users_data,UsersOnline=online)

