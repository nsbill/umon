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

    def __init__(self,uid,login,password,fio,phone,descr,disable,delete,tarifs_id,groups_id):
        self.uid = uid
        self.login = login
        self.password = password
        self.fio = fio
        self.phone = phone
        self.descr = descr
        self.disable = disable
        self.delete = delete
        self.tarifs_id = tarifs_id
        self.groups_id = groups_id

    def __repr__(self):
        return '<UID: {}>,<Login: {}>,<Password: {}>,<FIO: {}>,<Phone:{}>'.format(self.uid, self.login, self.password, self.fio, self.phone )


class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'), unique=True, nullable=False)
    address = db.Column(db.String(300),default='')
    street = db.Column(db.String(80),default='')
    building = db.Column(db.String(10),default='')
    flat = db.Column(db.String(10),default='')

    def __init__(self,uid,address,street,building,flat):
        self.uid = uid
        self.address = address
        self.street = street
        self.building = building
        self.flat = flat
    def __repr__(self):
        return 'uid: {},street: {},build: {},flat: {}'.format(self.uid, self.street, self.building,self.flat)

class SelectAdressUid(db.Model):
    __tablename__='adr_uid'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'), unique=True, nullable=False)
    street_id = db.Column(db.Integer, db.ForeignKey('sortstreet.street_id'))
    build_id = db.Column(db.Integer, db.ForeignKey('sortbuild.build_id'))
    flat_id = db.Column(db.Integer, db.ForeignKey('sortflat.flat_id'))

street_build = db.Table('street_build',
        db.Column('street_id', db.Integer, db.ForeignKey('sortstreet.street_id')),
        db.Column('build_id', db.Integer, db.ForeignKey('sortbuild.build_id'))
        )

class SortStreet(db.Model):
    __tablename__='sortstreet'
    street_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    building = db.relationship('SortBuild', secondary=street_build, backref=db.backref('streetbuild', lazy = 'dynamic'))

build_flat = db.Table('build_flat',
        db.Column('build_id', db.Integer, db.ForeignKey('sortbuild.build_id')),
        db.Column('flat_id', db.Integer, db.ForeignKey('sortflat.flat_id'))
        )
class SortBuild(db.Model):
    __tablename__='sortbuild'
    build_id = db.Column(db.Integer, primary_key=True)
    number_build = db.Column(db.String(10))
    flat = db.relationship('SortFlat', secondary=build_flat, backref=db.backref('buildflat', lazy = 'dynamic'))

class SortFlat(db.Model):
    __tablename__='sortflat'
    flat_id = db.Column(db.Integer, primary_key=True)
    number_flat = db.Column(db.String(10))

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
#    uid = db.Column('uid', db.Integer, db.ForeignKey('users.uid'), unique=True, Gnullable=False)
    tpid = db.Column('tpid', db.Integer, unique=True, nullable=False)
    name = db.Column('name', db.String(100))
    day_fee = db.Column('day_fee', db.Float)
    month_fee = db.Column('month_fee', db.Float)
    active_day_fee = db.Column('active_day_fee', db.Float)
    comments = db.Column('comments', db.String(200))

class UsersPI(db.Model):
    __tablename__ = 'userspi'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column('uid', db.Integer, db.ForeignKey('users.uid'), unique=True, nullable=False)
    logins = db.Column('logins', db.Integer, default=0)
    bill_id = db.Column('bill_id', db.Integer, unique=True, nullable=False)
    balance = db.Column('balance', db.Float)
    registration = db.Column('registration', db.Date, default='2000-01-01')
    activate = db.Column('activate', db.Date, default='2000-01-01')
    expire = db.Column('expire', db.Date, default='2001-01-01')
    reduction = db.Column('reduction', db.Float)
    reduction_date = db.Column('reduction_date', db.DateTime, default='2000-01-01')
    credit = db.Column('credit', db.Float)
    credit_date = db.Column('credit_date', db.DateTime, default='2000-01-01')
    archive = db.Column('archive', db.Boolean,default=False)
    contract_id = db.Column('contract_id', db.String(25))
    contract_date = db.Column('contract_date', db.Date, default='2000-01-01')
    pasport_num = db.Column('pasport_num', db.String(25))
    pasport_date = db.Column('pasport_date', db.Date, default='2000-01-01')
    pasport_grant = db.Column('pasport_grant', db.String(200))
    telegram = db.Column('telegram', db.Integer, default=0)
    telegram_send = db.Column('telegram_send', db.Integer,default=0)
    vk = db.Column('vk', db.Integer,default=0)
    vk_send = db.Column('vk_send', db.Integer,default=0)
    status = db.Column('status', db.Integer)
    company_id = db.Column('company_id', db.Integer)
    email = db.Column('email', db.String(100))

class DvCalls(db.Model):
    __tablename__= 'dv_calls'
    id = db.Column(db.BigInteger, primary_key=True)
    status = db.Column('status', db.Integer)
    username = db.Column('username',db.String(32))
    started = db.Column('started', db.DateTime)
    acct_session_id = db.Column('acct_session_id', db.String(32))
    acct_session_time = db.Column('acct_session_time', db.Integer)
    acct_input_octets = db.Column('acct_input_octets', db.BigInteger)
    acct_output_octets = db.Column('acct_output_octets', db.BigInteger)
    framed_ip_address = db.Column('framed_ip_address', postgresql.INET)
    lupdated = db.Column('lupdated', db.Integer)
    cid = db.Column('cid', db.String(17))
    connect_info = db.Column('connect_info', db.String(35))
    tpid = db.Column('tpid', db.Integer)
    nas_id = db.Column('nas_id',db.Integer)
    uid = db.Column('uid', db.Integer)
    guest = db.Column('guest', db.Integer)
