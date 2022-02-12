from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config['SECRET_KEY'] = 'f64b7c4f8a22f916a5a3ca7c00627310'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mw.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.user_login'
login_manager.login_message_category = 'info'
admin = Admin(app)


from website.users.routes import users
from website.applications.routes import apps
from website.reports.routes import reports
from website.instances.routes import instances
from website.sop.routes import sops
from website.main.routes import main

app.register_blueprint(users)
app.register_blueprint(apps)
app.register_blueprint(reports)
app.register_blueprint(instances)
app.register_blueprint(sops)
app.register_blueprint(main)