from app import app
from app import db
from auth.blueprint import auth
from users.blueprint import users
from importation.blueprint import imp

import view

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(imp, url_prefix='/imp')


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', port=80, debug=True, use_reloader=True)
