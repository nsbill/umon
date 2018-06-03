from app import db
import sys
sys.path.insert(0, '/app/db')
sys.path.insert(0, '/app/users')

from mysql_select import query_with_users_uid
from users_impfunc import upd_user

def uids_users():
    uids = query_with_users_uid()
    return uids

def update_uids_postgres():
    uids = uids_users()
    info = []
    for uid in uids:
        upd_user(uid['uid'])
        info.append('Update = '+ str(uid))
        print('Update=='+str(uid))
    return info

if __name__ == '__main__':
    update_uids_postgres()
