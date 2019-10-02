from flask import Flask
from flask import render_template
import pymongo

import datetime
import json
#from mongo_settings import MONGO_KEY


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    #db.init_app(app)
    MONGO_KEY = app.config.get("MONGO_KEY")
    client = pymongo.MongoClient(MONGO_KEY)
    db = client.testdb
    #cursor = db.content.find({})

    @app.route('/')
    def index():
        #print(list(cursor))
        title = "RD"
        '''
        with open('siteapp/content.json','r') as f:
            posts_list = json.loads(f.read())
        '''
        cursor = db.content.find({}).sort('_id', pymongo.DESCENDING).limit(20)
        posts_list = list(cursor)
        #print(posts_list)
        return render_template('index.html',page_title=title, 
                posts_list=posts_list)

    return app


