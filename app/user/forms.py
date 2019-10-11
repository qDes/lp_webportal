from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from app.user.models import User

class LoginForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired()],render_kw={"class":"form-control"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"class":"form-control"})
    submit = SubmitField("Login", render_kw={"class":"btn btn-primary"})
    remember_me = BooleanField("Remember me", default="True", render_kw={"class":"form-check-input"})


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()],render_kw={"class":"form-control"})
    email = StringField('Электронная почта', validators=[DataRequired(), Email()],render_kw={"class":"form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(),EqualTo('password')], render_kw={"class": "form-control"})
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary"})
    remember_me = BooleanField('Запомнить меня', default=True, render_kw={"class": "form-check-input"})
    
    def validate_username(self, username):
        user_count = User.objects(username=username.data).count()
        if user_count > 0:
            raise ValidationError("Пользователь с таким именем уже существует")

    def validate_email(self, email):
        email_count = User.objects(email=email.data).count()
        if email_count > 0:
            raise ValidationError("Пользователь с такой почтой уже существует")
