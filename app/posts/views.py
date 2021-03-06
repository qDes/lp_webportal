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
    return render_template('posts/single_post.html',page_title=my_post.title,
            post=my_post,comment_form=form)

@blueprint.route('/posts/<string:post_id>/edit')
@login_required
def edit_post(post_id):
    page_title = 'Edit post:'
    post = Post.objects(id=post_id).get()
    form = PostAddForm()
    form.title.data = post.title
    form.url.data = " ".join(post.urls)
    form.tag.data = post.tag
    form.text.data = post.text
    return render_template("posts/edit_post.html",
            page_title=page_title,
            form=form,post_id=post_id)

@blueprint.route('/posts/<string:post_id>/edit_post_proc', methods=['POST'])
def edit_post_proc(post_id):
    form = PostAddForm()
    post = Post.objects(id=post_id).get()
    post.title = form.title.data
    post.tag = form.tag.data
    post.text = form.text.data
    post.urls = form.url.data.split()
    post.save()
    flash('Edited post')
    return redirect(url_for("posts.index"))

@blueprint.route('/posts/tag/<string:tag>')
def view_tag(tag):
    title = f"Tag: {tag}"
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    posts_list = Post.objects(tag=tag).paginate(page=page,per_page=10)
    pagination = Pagination(page=page,
            total = Post.objects(tag=tag).count(), css_framework='bootstrap4',
            search=search, record_name='posts')
    return render_template('posts/tag_page.html',page_title=title,
            posts_list=posts_list, pagination=pagination)

@blueprint.route('/posts/comment', methods=['POST'])
@login_required
def add_comment():
    form = CommentForm()
    if form.validate_on_submit():
        post=Post.objects(id=form.post_id.data).get()
        comment=Comment(text=form.comment_text.data,
                from_user=User.objects(id=current_user.id).get(),
                post=post)
        comment.save()
        Post.objects(id=form.post_id.data).update_one(push__comments=comment)
    return redirect(get_redirect_target())

@blueprint.route('/posts/delete_comment', methods=['POST'])
@login_required
def delete_comment():
    form = DeleteForm()
    id_ = form.id_.data
    comment = Comment.objects(id=id_).get()
    comment.delete()
    return redirect(get_redirect_target())

@blueprint.route('/posts/delete_post', methods=['POST'])
@login_required
def delete_post():
    form = DeleteForm()
    id_ = form.id_.data
    post = Post.objects(id=id_).get()
    post.delete()
    return redirect(url_for('posts.index'))


@blueprint.route('/posts/add_post')
@login_required
def add_post():
    form = PostAddForm()
    title = "Add post"
    return render_template("posts/add_post.html", page_title=title,
            form=form)

@blueprint.route('/posts/add_post_proc',methods=['POST'])
def add_post_proc():
    form = PostAddForm()
    #if form.validate_on_submit():
    user = User.objects(id=current_user.id).get()
    post = Post(title=form.title.data,
            tag=form.tag.data,
            text=form.text.data,
            urls=form.url.data.split(),
            user=user,
            )
    post.save()
    flash('Add post')
    return redirect(url_for("posts.index"))#redirect(get_redirect_target())
