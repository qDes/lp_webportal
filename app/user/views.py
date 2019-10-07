from flask import render_template, Blueprint, current_app, redirect, url_for
from flask_login import login_user, logout_user, current_user
from app.user.models import User
from app.user.forms import LoginForm

blueprint = Blueprint("user", __name__, url_prefix='/users')

@blueprint.route("/login")
def login():
    '''
    if current_user.is_authenticated:
        return redirect(url_for("posts.index"))
    '''
    title = "Auth."
    login_form = LoginForm()
    return render_template("user/login.html",page_title=title, form=login_form)

@blueprint.route("/process-login", methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username)
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Вы вошли на сайт')
            return redirect(url_for('news.index'))
