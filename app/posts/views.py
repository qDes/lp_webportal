from flask import render_template, Blueprint, current_app

from app.posts.models import Post

blueprint = Blueprint("posts", __name__)

@blueprint.route('/')
def index():
    title = "RD"
    posts_list = list(Post.objects.order_by('-posted').limit(5))
    return render_template('posts/index.html',page_title=title,
            posts_list=posts_list)
