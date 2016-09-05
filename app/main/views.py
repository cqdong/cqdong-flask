# coding:utf-8
from flask import render_template, redirect, url_for, request, current_app
from . import main
from datetime import datetime
from .forms import PostForm, CommentForm
from ..models import Post, Comment, TestMptt
from .. import db
from flask_login import login_required

@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter(Post.published_date.isnot(None)).order_by(Post.published_date.desc()).paginate(
        page, per_page=3, error_out=False
    )
    post = pagination.items
    return render_template('index.html', current_time=datetime.utcnow(), posts=post, pagination=pagination)


@main.route('/posts', methods=['GET', 'POST'])
@login_required
def post_new():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data)
        post.body_abstract()
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template('post_edit.html', forms=form)


@main.route('/posts/<int:id>', methods=['GET', 'POST'])
def post_detail(id):
    post = Post.query.get_or_404(id)
    testmptt = TestMptt.query.filter_by(parent_id=None)
    post_comment = Comment.query.filter_by(parent_id=None, post_id=post.id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(username=form.username.data, email=form.email.data, url=form.url.data, body=form.body.data, post_id=post.id, parent_id=int(form.parent.data))
        db.session.add(comment)
        return redirect(url_for('.post_detail', id=post.id))
    return render_template('post_detail.html', posts=post, comment_forms=form, testmptts=testmptt, comments=post_comment)


@main.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def post_edit(id):
    post = Post.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.body_abstract()
        return redirect(url_for('.post_detail', id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    return render_template('post_edit.html', forms=form)


@main.route('/posts/remove/<int:id>')
@login_required
def post_remove(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    return redirect(url_for('.index'))


@main.route('/drafts')
@login_required
def post_drafts_list():
    drafts = True
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter_by(published_date=None).order_by(Post.create_date.desc()).paginate(page, 3, False)
    post = pagination.items
    return render_template('post_drafts.html', posts=post, current_time=datetime.utcnow(), drafts=drafts, drafts_pagination=pagination)


@main.route('/posts/publish/<id>')
@login_required
def post_publish(id):
    post = Post.query.get_or_404(id)
    post.published_date = datetime.utcnow()
    return redirect(url_for('.index'))


@main.route('/comment/<int:id>', methods=['GET', 'POST'])
def post_comment(id):
    form = CommentForm()
    return render_template('auth/login.html', comment_forms=form)