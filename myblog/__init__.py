from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '12c65ff986cfb670141e121a406c9f60'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'admin.login'
login_manager.login_message_category = 'info'

from myblog.admin.routes import admin
from myblog.blogs.routes import blogs
from myblog.main.routes import main

app.register_blueprint(admin)
app.register_blueprint(blogs)
app.register_blueprint(main)