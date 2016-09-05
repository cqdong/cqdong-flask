from . import db
from datetime import datetime
from flask import Request
from flask_login import UserMixin
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_mptt.mixins import BaseNestedSets

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    body = db.Column(db.Text)
    create_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    published_date = db.Column(db.DateTime)
    abstract = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comment = db.relationship('Comment', backref='post', lazy='dynamic')

    def body_abstract(self, cut_length=500):
        judge = None
        cut_date = []
        html_tag_date = []
        html_tag_date_cache = None
        html_tag = ''

        for i in self.body:
            if i == '<':
                judge = True
            if i == '>':
                html_tag_date += i
                cut_date += html_tag_date
                html_tag_date_cache = html_tag_date
                html_tag_date = []
                judge = False
                continue

            if judge:
                html_tag_date += i
            else:
                cut_date += i
                cut_length -= 1

            if cut_length == 0:
                if not html_tag_date_cache or html_tag_date_cache[1] == '/':
                    break
                for j in html_tag_date_cache[1:]:
                    if j == ' ' or j == '>':
                        break
                    html_tag += j
                if html_tag:
                    html_tag = '</%s>'%html_tag
                break

        cut_date = ''.join(cut_date)+html_tag
        self.abstract = cut_date

    def __repr__(self):
        return 'title:%r'%self.title

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    post = db.relationship('Post', backref='user', lazy='dynamic')
    test_id = db.Column(db.Integer, db.ForeignKey('testmptts.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

class Comment(db.Model, BaseNestedSets):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)
    url = db.Column(db.String(64))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def __repr__(self):
        return 'comment_name {}'.format(self.username)

class TestMptt(db.Model, BaseNestedSets):
    __tablename__ = 'testmptts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    items = db.relationship('User', backref='item', lazy='dynamic')

    def __repr__(self):
        return '<testmptt> {}'.format(self.name)