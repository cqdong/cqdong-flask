from flask_wtf import Form
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import Required, Email, Length, URL

class PostForm(Form):
    title = StringField('Title', validators=[Required()])
    body = TextAreaField("What's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')

class CommentForm(Form):
    username = StringField('Username', validators=[Required(), Length(1,64)])
    email = StringField('Email', validators=[Required(), Email(), Length(1,64)])
    url = StringField('Url', validators=[URL()])
    body = TextAreaField('Your comment.', validators=[Required()])
    parent = IntegerField('Parent')
    submit = SubmitField('Submit')