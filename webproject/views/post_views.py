from flask import Blueprint, render_template, request, url_for

from webproject.models import *

bp = Blueprint('post', __name__, url_prefix='/post')

@bp.route('/list')
def _list():
    page = request.args.get('page', type=int, default=1)
    post_list = Post.query.order_by(Post.create_date.desc())
    post_list = post_list.paginate(page, per_page=10)
    return render_template('post/post_list.html', post_list=post_list)


@bp.route('/detail/<int:post_id>')
def detail(post_id):
    post = Post.query.get_or_404(post_id)
    book = BookInfo.query.get(post.book_info_id)
    return render_template('post/post_detail.html', post=post, book=book)
