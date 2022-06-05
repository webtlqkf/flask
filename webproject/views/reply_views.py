from datetime import datetime
from flask import Blueprint, url_for, request,g
from werkzeug.utils import redirect
from ..forms import *

from webproject import db
from webproject.models import *
from webproject.views.auth_views import login_required


bp = Blueprint('reply', __name__, url_prefix='/reply')

@bp.route('/create/<int:post_id>', methods = ('POST',))
@login_required
def create(post_id):
    form = ReplyForm()
    post = Post.query.get_or_404(post_id)
    content = request.form['content']
    reply = Reply(content=content, create_date=datetime.now(),user=g.user)
    post.reply_set.append(reply)
    db.session.commit()

    return redirect(url_for('post.detail',post_id=post_id))