class Configuration(object):
    DEBUG=True
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_DATABASE_URI='postgresql://dbuser:dbuser2018@db/dbumon'
    SECRET_KEY='pgERrGbzIQSk6Tg4JvwjGJkgXKSS5uP7i9yY8NjsOvibKKOZ7T'
    ### Flask-Security
    SECURITY_PASSWORD_SALT='salt'
    SECURITY_PASSWORD_HASH='sha512_crypt'
