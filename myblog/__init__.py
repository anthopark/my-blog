
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from myblog.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'admin.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # importing instances of the blueprints
    from myblog.main.routes import main
    from myblog.blogs.routes import blogs
    from myblog.admin.routes import admin
    from myblog.errors.handlers import errors
    
    app.register_blueprint(admin)
    app.register_blueprint(blogs)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
