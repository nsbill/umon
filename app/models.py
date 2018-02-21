from app import db
from datetime import datetime
from sqlalchemy.dialects import postgresql

class AdminUser(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    login = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100))
    create = db.Column(db.DateTime, default=datetime.now())
    email = db.Column(db.String(120))
    activ = db.Column(db.Boolean,default=False)

    def __init__(self, *args, **kwargs):
        super(AdminUser, self).__init__(*args, **kwargs)
    def __repr__(self):
        return '<User %r>' % self.login

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, unique=True, nullable=False)
    login = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(50))
    fio = db.Column(db.String(150))
    phone = db.Column(db.String(12), default='0')
    descr = db.Column(db.Text)
    disable = db.Column(db.Boolean, default=False)
    delete = db.Column(db.Boolean, default=False)
    address_id = db.relationship('Address', backref='users', lazy='dynamic')
    networks_id = db.relationship('Networks', backref='networks', lazy='dynamic')
    tarifs_id = db.Column(db.Integer, db.ForeignKey('tarifs.tpid'))
    groups_id = db.Column(db.Integer, db.ForeignKey('groups.gid'))
 #   groups_id = db.relationship('Groups', backref='groups', lazy='dynamic')
 #   tarifs_id = db.relationship('Tarifs', backref='tarifs', lazy='dynamic')
    users_pi = db.relationship('UsersPI', backref='userspi', lazy='dynamic')

#    def __init__(self,uid,login,password,fio,phone,descr,disable,delete,address_id):
#        self.uid = uid
#        self.login = login
#        self.password = password
#        self.fio = fio
#        self.phone = phone
#        self.descr = descr
#        self.disable = disable
#        self.delete = delete
#        self.address_id = address_id
#
#    def __repr__(self):
#        return '<login: %r>' % (self.login)

class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'), unique=True, nullable=False)
    address = db.Column(db.String(300),default='')
    street = db.Column(db.String(80),default='')
    building = db.Column(db.String(10),default='')
    flat = db.Column(db.String(10),default='')

#    def __init__(self,uid,address,street,building,flat):
#        self.uid = uid
#        self.address = address
#        self.street = street
#        self.building = building
#        self.flat = flat

class Networks(db.Model):
    __tablename__ = 'networks'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column('uid', db.Integer, db.ForeignKey('users.uid'), unique=True, nullable=False)
    ip = db.Column('ip', postgresql.INET)
    netmask = db.Column('netmask', postgresql.INET)
    cid = db.Column('cid', db.String(17))

class Groups(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
#    uid = db.Column('uid', db.Integer, db.ForeignKey('users.uid'), unique=True, nullable=False)
    gid = db.Column('gid', db.Integer, unique=True, nullable=False)
    name = db.Column('name', db.String(100))
    descr = db.Column('descr', db.String(200))

class Tarifs(db.Model):
    __tablename__ = 'tarifs'
    id = db.Column(db.Integer, primary_key=True)
#    uid = db.Column('uid', db.Integer, db.ForeignKey('users.uid'), unique=True, nullable=False)
    tpid = db.Column('tpid', db.Integer, unique=True, nullable=False)
    name = db.Column('name', db.String(100))
    day_fee = db.Column('day_fee', db.Float)
    month_fee = db.Column('month_fee', db.Float)
    active_day_fee = db.Column('active_day_fee', db.Float)
    comments = db.Column('comments', db.String(200))

#class Aaa(db.Model):
#    __tablename__ = 'aaa'
#    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column('name', db.String(100))
#    day_fee = db.Column('day_fee', db.Float)
#    activ_day_fee = db.Column('activ_day_fee', db.Float)
#    descr = db.Column('descr', db.String(200))

class UsersPI(db.Model):
    __tablename__ = 'userspi'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column('uid', db.Integer, db.ForeignKey('users.uid'), unique=True, nullable=False)
    balance = db.Column('balance', db.Float)
    registration = db.Column('registration', db.DateTime)
    reduction = db.Column('reduction', db.Float)
    reduction_date = db.Column('reduction_date', db.DateTime)
    credit = db.Column('credit', db.Float)
    credit_date = db.Column('credit_date', db.DateTime)
    archive = db.Column('archive', db.Boolean)
    contract_id = db.Column('contract_id', db.String(25))
    contract_date = db.Column('contract_date', db.DateTime)
    pasport_num = db.Column('pasport_num', db.String(25))
    pasport_date = db.Column('pasport_date', db.DateTime)
    telegram = db.Column(db.Integer, default=0)
    telegram_send = db.Column(db.Integer,default=0)
    vk = db.Column(db.Integer,default=0)
    vk_send = db.Column(db.Integer,default=0)


