from flask_wtf import Form
from wtforms import StringField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import Required

class PostForm(Form):
    title = StringField('Title', validators=[Required()])
    body = TextAreaField("What's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')