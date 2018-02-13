form app import db
form datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    login = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(100))
    create = db.Column(db.DateTime, default=datetime.now())
    email = db.Column(db.String(120))
    activ = db.Column(db.Boolean,default=False)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
#        self.
