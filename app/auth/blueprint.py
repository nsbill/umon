from flask import Blueprint
from flask import render_template

auth = Blueprint('auth',__name__, template_folder='templates')
@auth.route('/')
def index():
    return render_template('auth/index.html')
