from flask import render_template, Blueprint, current_app, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app.user.models import User
from app.user.forms import LoginForm

blueprint = Blueprint("user", __name__, url_prefix='/users')

@blueprint.route("/login")
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for("posts.index"))
    
    title = "Authentication"
    login_form = LoginForm()
    return render_template("user/login.html",page_title=title, form=login_form)

@blueprint.route("/process-login", methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects.get(username=form.username.data)
        print('#'*100)
        print(dir(user))
        #print(user.check_password(123),user.check_password(123456))
        print('#'*100)
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('You are logged in')
            return redirect(url_for('posts.index'))

@blueprint.route("/logout")
def logout():
    logout_user()
    flash("Logout")
    return redirect(url_for("posts.index"))
