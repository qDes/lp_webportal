from flask import render_template, Blueprint, current_app, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app.user.models import User
from app.user.forms import LoginForm, RegistrationForm
from app.utils import get_redirect_target

blueprint = Blueprint("user", __name__, url_prefix='/users')

@blueprint.route("/login")
def login():
    
    if current_user.is_authenticated:
        return redirect(get_redirect_target())#redirect(url_for("posts.index"))
        
    title = "Authentication"
    login_form = LoginForm()
    return render_template("user/login.html",page_title=title, form=login_form)

@blueprint.route("/process-login", methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects.get(username=form.username.data)
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('You are logged in')
            return redirect(url_for('posts.index'))
        else:
            flash('Wrong username or password')
            return redirect(get_redirect_target())#url_for('posts.index'))

@blueprint.route("/logout")
def logout():
    logout_user()
    flash("Logout")
    return redirect(url_for('posts.index'))

@blueprint.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
    form = RegistrationForm()
    title = "Registration"
    return render_template('user/registration.html', page_title=title, form=form)


@blueprint.route('/process-reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, role='user')
        new_user.set_password(form.password.data)
        new_user.save()
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('user.login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash("Error in field {}: {}".format(getattr(form,field).label.text, error))

        return redirect(url_for('user.register'))
