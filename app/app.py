from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_security import SQLAlchemyUserDatastore
from flask_security import Security

app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

#--- ADMIN ---
from models import AdminUser,AdminRole,Users,Address,SelectAdressUid,SortStreet,SortBuild,SortFlat,Networks,Groups,Tarifs,UsersPI,DvCalls
admin = Admin(app)
admin.add_view(ModelView(AdminUser, db.session))
admin.add_view(ModelView(AdminRole, db.session))
admin.add_view(ModelView(Users, db.session))
admin.add_view(ModelView(Address, db.session))
#admin.add_view(ModelView(SelectAdressUid, db.session))
admin.add_view(ModelView(SortStreet, db.session))
admin.add_view(ModelView(SortBuild, db.session))
admin.add_view(ModelView(SortFlat, db.session))
admin.add_view(ModelView(Networks, db.session))
admin.add_view(ModelView(Groups, db.session))
admin.add_view(ModelView(Tarifs, db.session))
admin.add_view(ModelView(UsersPI, db.session))
admin.add_view(ModelView(DvCalls, db.session))

#--- Admin Flask Security ---

user_datastore = SQLAlchemyUserDatastore(db, AdminUser,AdminRole)
security = Security(app, user_datastore)
