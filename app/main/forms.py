from flask_wtf import Form
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import Required, DataRequired, Email, Length, url, InputRequired
from flask_pagedown.fields import PageDownField

class PostForm(Form):
    title = StringField('Title', validators=[InputRequired()])
    body = PageDownField("What's on your mind?", validators=[InputRequired()])
    submit = SubmitField('Submit')

class CommentForm(Form):
    username = StringField('Username', validators=[InputRequired(), Length(1,64)])
    email = StringField('Email', validators=[InputRequired(), Email(), Length(1,64)])
    url = StringField('Url', validators=[url()])
    body = TextAreaField('Your comment.', validators=[InputRequired()])
    submit = SubmitField('Submit')

class ReplyCommentForm(Form):
    reply_username = StringField('Username', validators=[InputRequired(), Length(1,64)])
    reply_email = StringField('Email', validators=[InputRequired(), Email(), Length(1,64)])
    reply_url = StringField('Url', validators=[url()])
    reply_body = TextAreaField('Your comment.', validators=[InputRequired()])
    reply_parent = IntegerField('Parent')
    reply_submit = SubmitField('Submit')
