from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Configuration
from auth.blueprint import auth

app = Flask(__name__)
db = SQLAlchemy(app)


app.config.from_object(Configuration)
app.register_blueprint(auth, url_prefix='/auth')
