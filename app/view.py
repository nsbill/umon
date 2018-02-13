from app import app
from flask import render_template

@app.route('/')
def index():
    name = 'Aleksandr'
    return render_template('index.html',name=name)
