from flask import Flask
from flask import render_template, current_app
import datetime
import json

from app.db import mongo
from app.posts.views import blueprint as posts_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    mongo.init_app(app)
    
    app.register_blueprint(posts_blueprint)
    
    return app


