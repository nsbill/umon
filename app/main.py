from app import app
from app import db
from auth.blueprint import auth
from users.blueprint import users

import view

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(users, url_prefix='/users')

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', port=80)
