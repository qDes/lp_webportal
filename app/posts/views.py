from flask import abort, render_template, Blueprint, current_app, redirect
from flask_login import login_required, current_user

from app.posts.models import Post, Comment
from app.posts.forms import CommentForm
from app.user.models import User
from app.utils import get_redirect_target
blueprint = Blueprint("posts", __name__)

@blueprint.route('/')
def index():
    title = "Web Portal"
    posts_list = list(Post.objects.order_by('-posted'))
    return render_template('posts/index.html',page_title=title,
            posts_list=posts_list)

@blueprint.route('/posts/<string:post_id>')
def single_post(post_id):
    my_post =  Post.objects(id=post_id).get()
    if not my_post:
        abort(404)
    form = CommentForm(post_id=post_id)
    return render_template('posts/single_post.html',page_title=my_post.title,
            post=my_post,comment_form=form)


@blueprint.route('/posts/comment', methods=['POST'])
@login_required
def add_comment():
    form = CommentForm()
    if form.validate_on_submit():
        #form.post_id.data
        comment=Comment(text=form.comment_text.data,
                from_user=User.objects(id=current_user.id).get())
        comment.save()
        Post.objects(id=form.post_id.data).update_one(push__comments=comment)
    return redirect(get_redirect_target())
