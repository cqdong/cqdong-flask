from . import db
from datetime import datetime
from flask import Request

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    # author_id = db.Column(db.Integer, db.ForeignKey(users.id))
    title = db.Column(db.String(128))
    body = db.Column(db.Text)
    create_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    published_date = db.Column(db.DateTime)

    def publish(self):
        self.publish_date = datetime.now()

    def __repr__(self):
        return 'title:%r'%self.title

# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), unique=True)
#     email = db.Column(db.String(64), unique=True, index=True)
#     possowrd = db.Column(db.String(128))
#     confirmed = db.Column(db.Boolean, default=False)
