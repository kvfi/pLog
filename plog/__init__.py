from flask import Flask
from flask_login import LoginManager
from flask_mongoengine import MongoEngine

from config import Config
from plog.api import UsersApi

app = Flask(__name__)
app.config.from_object(Config)

db = MongoEngine(app)

lmanager = LoginManager()
lmanager.init_app(app)
lmanager.login_view = 'login'

api.add_resource(UsersApi, '/users', endpoint='users')

from plog import routes
