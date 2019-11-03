from flask import Flask
from flask import render_template, current_app, flash, redirect, url_for
from flask_login import LoginManager, login_required, current_user

from app.db import db
from app.posts.views import blueprint as posts_blueprint
from app.user.views import blueprint as user_blueprint
from app.admin.views import blueprint as admin_blueprint
from app.user.models import User

from mongoengine import connect

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    connect(db='testdb',host=app.config.get("MONGO_URI")) 
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    app.register_blueprint(posts_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.objects.get(id=user_id)
    
    return app


