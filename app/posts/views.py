from flask import abort, render_template, Blueprint, current_app, flash, redirect, request, url_for
from flask_login import login_required, current_user
from flask_paginate import Pagination, get_page_parameter

from app.posts.models import Post, Comment
from app.posts.forms import CommentForm, DeleteForm, PostAddForm
from app.user.models import User
from app.user.decorators import admin_required
from app.utils import get_redirect_target


blueprint = Blueprint("posts", __name__)

@blueprint.route('/')
def index():
    title = "Le Coq d'Esprit"
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    #posts_list = list(Post.objects.order_by('-posted'))
    posts_list = Post.objects.order_by('-posted').paginate(page=page,per_page=10)
    pagination = Pagination(page=page,
            total = Post.objects.count(),css_framework='bootstrap4',
            search=search, record_name='posts')
    return render_template('posts/index.html',page_title=title,
            posts_list=posts_list, pagination=pagination)

@blueprint.route('/posts/<string:post_id>')
def single_post(post_id):
    my_post =  Post.objects(id=post_id).get()
    if not my_post:
        abort(404)
    form = CommentForm(post_id=post_id)
    #del_form = DeleteForm()
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

@blueprint.route('/posts/delete_comment', methods=['POST'])
@admin_required
def delete_comment():
    form = DeleteForm()
    comment_id = form.comment_id.data
    #print('##'*100)
    comment = Comment.objects(id=comment_id).get()
    comment.delete()
    return redirect(get_redirect_target())

@blueprint.route('/posts/add_post')
@login_required
def add_post():
    form = PostAddForm()
    title = "Add post"
    return render_template("posts/add_post.html", page_title=title,
            form=form)

@blueprint.route('/posts/add_post_proc',methods=['POST'])
def add_post_proc():
    print(1)
    form = PostAddForm()
    print(2)
    #if form.validate_on_submit():
    print(current_user.id)
    print(3)
    post = Post(title=form.title.data,
            tag=form.tag.data,
            text=form.text.data,
            urls=[form.url.data],
            )
    print(post)
    post.save()
    print('4')
    flash('Add post')
    return redirect(url_for("posts.index"))#redirect(get_redirect_target())
