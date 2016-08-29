# coding:utf-8
from flask import render_template, redirect, url_for
from . import main
from datetime import datetime
from .forms import PostForm
from ..models import Post
from .. import db

@main.route('/')
def index():
    post = Post.query.order_by(Post.create_date.desc()).all()
    return render_template('index.html', current_time=datetime.utcnow(), posts=post)

@main.route('/posts', methods=['GET', 'POST'])
def post_new():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=u'%s'%form.body.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template('post_edit.html', forms=form)

@main.route('/posts/<int:id>')
def post_detail(id):
    post = Post.query.filter_by(id=id).first()
    return render_template('post_detail.html', posts=post)

@main.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def post_edit(id):
    post = Post.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        return redirect(url_for('.post_detail', id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    return render_template('post_edit.html', forms=form)

@main.route('/posts/remove/<int:id>')
def post_remove(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    return redirect(url_for('.index'))