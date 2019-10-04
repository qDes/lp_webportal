from flask import render_template, Blueprint, current_app
from flask_pymongo import DESCENDING
from app.db import mongo

blueprint = Blueprint("posts", __name__)

@blueprint.route('/')
def index():
    title = "RD"
    client = mongo.cx
    db = client.testdb
    cursor = db.content.find({}).sort('_id', DESCENDING).limit(20)
    posts_list = list(cursor)
    return render_template('posts/index.html',page_title=title,
            posts_list=posts_list)
