from flask import render_template, redirect, url_for
from . import main
from datetime import datetime
from .forms import PostForm
from ..models import Post
from .. import db

@main.route('/')
def index():
    # form = PostForm()

    return render_template('index.html', current_time=datetime.utcnow())

@main.route('/posts', methods=['GET', 'POST'])
def post_new():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template('post_edit.html', forms=form)