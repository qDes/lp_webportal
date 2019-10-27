from flask import Blueprint, render_template

from app.user.decorators import admin_required
from app.posts.models import Comment, Post

blueprint = Blueprint('admin',__name__, url_prefix = '/admin')

@blueprint.route('/')
@admin_required
def admin_index():
    title = "ADMIN"
    posts_list = Post.objects.order_by('-posted').limit(5)
    comments_list = Comment.objects.order_by('-created').limit(10)
    return render_template('admin/index.html', page_title=title, 
            posts_list=posts_list, comments_list=comments_list)
