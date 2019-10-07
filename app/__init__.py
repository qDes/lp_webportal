from flask import Flask
from flask import render_template, current_app
import datetime
import json

from app.db import db
from app.posts.views import blueprint as posts_blueprint
from app.user.views import blueprint as user_blueprint

from mongoengine import connect

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    connect(db='testdb',host=app.config.get("MONGO_URI")) 
    app.register_blueprint(posts_blueprint)
    app.register_blueprint(user_blueprint)
    return app


