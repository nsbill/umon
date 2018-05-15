from flask import Blueprint
from flask import render_template
from datetime import datetime
import sys
sys.path.insert(0, '/app/users')
from users_impfunc import search, litters_street, all_users, users_info, user_info, user_data, select_address

users = Blueprint('users',__name__, template_folder='templates')


@users.route('/')
def index():
    ''' Выборка всех пользователей из базы PostgreSQL '''
    UsersALL = all_users()
    return render_template('users/index.html', UsersALL=UsersALL)

@users.route('/user/<uid>')
def user(uid):
    ''' Выборка данных о пользователе по UID '''
    UserInfo = user_info(uid)
    return render_template('users/userinfo.html', UserInfo=UserInfo, DateTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@litters_street
@search
@users.route('/adr/search')
def search_street():
    liststreet = litters_street(search_street)
    return render_template('users/search.html', ListSearch=liststreet[1], ListStreetLetters=liststreet[0].items(), DateTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@litters_street
@search
@users.route('/adr/street_id/<street_id>')
def street_id_users(street_id):
    def lstr():
        ''' Фун-ция для декоратора litters_street '''
        return lstr
    liststreet = litters_street(lstr)   # Cписок улиц и словарь улиц по заглавной букве
    users_data = users_info(street_id)
    return render_template('users/street_users.html', StreetUsers=street_id_users, ListSearch=liststreet[1], ListStreetLetters=liststreet[0].items(), Users=users_data)
