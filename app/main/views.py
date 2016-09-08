# coding:utf-8
from flask import render_template, redirect, url_for, request, current_app, make_response
from . import main
from datetime import datetime
from .forms import PostForm, CommentForm, ReplyCommentForm
from ..models import Post, Comment, TestMptt
from .. import db
from flask_login import login_required
# from werkzeug import secure_filename
import random
import os

def gen_rnd_filename():
    filename_prefix = datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))

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
    comment_form = CommentForm()
    reply_comment_form = ReplyCommentForm()

    if reply_comment_form.validate_on_submit():
        reply_comment = Comment(username=reply_comment_form.reply_username.data, email=reply_comment_form.reply_email.data,
                          url=reply_comment_form.reply_url.data, body=reply_comment_form.reply_body.data, post_id=post.id,
                          parent_id=reply_comment_form.reply_parent.data)
        db.session.add(reply_comment)
        db.session.commit()
        return redirect(url_for('.post_detail', id=post.id))

    if comment_form.validate_on_submit():
        comment = Comment(username=comment_form.username.data, email=comment_form.email.data,
                          url=comment_form.url.data, body=comment_form.body.data, post_id=post.id,)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('.post_detail', id=post.id))

    return render_template('post_detail.html', posts=post, comment_forms=comment_form,
                           reply_comment_forms=reply_comment_form, testmptts=testmptt, comments=post_comment)


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

@main.route('/ckupload/', methods=['OPTIONS', 'POST'])
def ckupload():
    error = ''
    url = ''
    callback = request.args.get("CKEditorFuncNum")
    if request.method == 'POST'and 'upload' in request.files:
        file = request.files['upload']
        if file:
            fname, fext = os.path.splitext(file.filename)
            rnd_name = '%s%s' % (gen_rnd_filename(), fext)

            filepath = os.path.join(current_app.static_folder, 'upload', rnd_name)

        # 检查路径是否存在，不存在则创建
            dirname = os.path.dirname(filepath)
            if not os.path.exists(dirname):
                try:
                    os.makedirs(dirname)
                except:
                    error = 'ERROR_CREATE_DIR'
            elif not os.access(dirname, os.W_OK):
                error = 'ERROR_DIR_NOT_WRITEABLE'

            if not error:
                file.save(filepath)
                url = url_for('static', filename='%s/%s' % ('upload', rnd_name))
    else:
        error = 'post error'

    res = """<script type="text/javascript">
             window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
            </script>""" %(callback, url, error)

    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response

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

