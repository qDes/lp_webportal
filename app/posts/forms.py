from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired

class CommentForm(FlaskForm):
    post_id = HiddenField('Post ID',validators=[DataRequired()])
    comment_text = StringField('Comment text:', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Send', render_kw={"class": "btn btn-primary"})
