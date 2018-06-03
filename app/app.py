from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_security import SQLAlchemyUserDatastore, Security, current_user

from flask import redirect, url_for, request


app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

#--- ADMIN ---
from models import AdminUser,AdminRole,Users,Address,SelectAdressUid,SortStreet,SortBuild,SortFlat,Networks,Groups,Tarifs,UsersPI,DvCalls


class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('Admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect( url_for('security.login', next=request.url ))

class AdminView(AdminMixin, ModelView):
    pass

class HomeAdminView(AdminMixin, AdminIndexView):
    pass

admin = Admin(app, 'FlaskApp', url='/', index_view=HomeAdminView(name='Home'))
admin.add_view(AdminView(AdminUser, db.session))
admin.add_view(AdminView(AdminRole, db.session))
admin.add_view(AdminView(Users, db.session))
admin.add_view(AdminView(Address, db.session))
#admin.add_view(AdminView(SelectAdressUid, db.session))
admin.add_view(AdminView(SortStreet, db.session))
admin.add_view(AdminView(SortBuild, db.session))
admin.add_view(AdminView(SortFlat, db.session))
admin.add_view(AdminView(Networks, db.session))
admin.add_view(AdminView(Groups, db.session))
admin.add_view(AdminView(Tarifs, db.session))
admin.add_view(AdminView(UsersPI, db.session))
admin.add_view(AdminView(DvCalls, db.session))

#--- Admin Flask Security ---

user_datastore = SQLAlchemyUserDatastore(db, AdminUser,AdminRole)
security = Security(app, user_datastore)
