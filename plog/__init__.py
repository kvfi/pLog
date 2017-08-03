from os.path import join, dirname

from dotenv import load_dotenv
from flask import Flask, request, abort
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'


@app.before_request
def default_login_required():
    if not (current_user.is_authenticated or request.endpoint in ['login', 'static']):
        return abort(403)


from plog import routes, models
