from flask import Blueprint, render_template, request, url_for, Flask, redirect, g, session
from werkzeug.utils import secure_filename
from webproject.models import *
from ..forms import *
from datetime import datetime
import os
from webproject.views.auth_views import login_required

bp = Blueprint('mypage', __name__, url_prefix='/mypage')

@bp.route('/list')
@login_required
def _list():
    user_id=session.get('user_id')
    post_list = Post.query.filter(Post.user_id==user_id).order_by(Post.create_date.desc())
    reply_list = Reply.query.filter(Reply.user_id==user_id).order_by(Reply.create_date.desc())
    return render_template('mypage/mypage_list.html', post_list=post_list, reply_list=reply_list)

@bp.route('/reply/<int:reply_id>')
def reply(reply_id):
    reply=Reply.query.get(reply_id)
    return render_template('mypage/mypage_reply.html', reply=reply)

@bp.route('/create/<int:reply_id>', methods = ('POST',))
def create(reply_id):
    reply = Reply.query.get_or_404(reply_id)
    content = request.form['content']
    re_reply = Re_reply(content=content, create_date=datetime.now(),user=g.user)
    reply.re_reply_set.append(re_reply)
    db.session.commit()
    return redirect(url_for('mypage.reply',reply_id=reply.id))

@bp.route('/post/all')
def post_all():
    user_id=session.get('user_id')
    page = request.args.get('page', type=int, default=1)
    post_list = Post.query.filter(Post.user_id == user_id).order_by(Post.create_date.desc())
    post_list = post_list.paginate(page, per_page=10)
    return render_template('mypage/mypage_post_all.html',post_list=post_list)

@bp.route('/reply/all')
def reply_all():
    user_id=session.get('user_id')
    page = request.args.get('page', type=int, default=1)
    reply_list = Reply.query.filter(Reply.user_id == user_id).order_by(Reply.create_date.desc())
    reply_list = reply_list.paginate(page, per_page=10)
    return render_template('mypage/mypage_reply_all.html',reply_list=reply_list)
