from flask import Blueprint, render_template, request, url_for, Flask, redirect, g, flash, session
from werkzeug.utils import secure_filename
from webproject.models import *
from ..forms import *
from datetime import datetime
import os
from webproject.views.auth_views import login_required



bp = Blueprint('post', __name__, url_prefix='/post')

@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    post_list = Post.query.order_by(Post.create_date.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        '''sub_query = db.session.query(Reply.post_id, Reply.content, User.username) \
            .join(User, Reply.user_id == User.id).subquery()
        post_list = post_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.post_id == Post.id) \
            .filter(Post.subject.ilike(search) |  # 질문제목
                    Post.content.ilike(search) |  # 질문내용
                    User.username.ilike(search) |  # 질문작성자
                    sub_query.c.content.ilike(search) |  # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    ) \
            .distinct()'''
        post_list = post_list.join(BookInfo).filter(
            BookInfo.name.ilike(search)|
            BookInfo.department.ilike(search)|
            BookInfo.author.ilike(search)|
            BookInfo.school.ilike(search)
        )
    post_list = post_list.paginate(page, per_page=10)
    return render_template('post/post_list.html', post_list=post_list, page=page, kw=kw)



'''    page = request.args.get('page', type=int, default=1)
    post_list = Post.query.order_by(Post.create_date.desc())
    post_list = post_list.paginate(page, per_page=10)
    return render_template('post/post_list.html', post_list=post_list)
'''

@bp.route('/detail/<int:post_id>')
def detail(post_id):
    post = Post.query.get_or_404(post_id)
    book = BookInfo.query.get(post.book_info_id)
    return render_template('post/post_detail.html', post=post, book=book)


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'PNG'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = '..\\finalproject\webproject\static\img'
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('post._list')) ## 이게 게시글 작성 페이지로 redirect 되어야 댐
    return render_template('/post/post_upload.html')

@bp.route('/create/' , methods=('GET','POST'))
@login_required
def create():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = '..\\finalproject\webproject\static\img'
    form = PostForm()
    if request.method == 'POST' and form.validate_on_submit():
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = '/static/img/'+filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        book = BookInfo(name=form.bookname.data, author=form.author.data, school=form.school.data,
                        department=form.department.data, price=form.price.data)
        post =Post(subject=form.subject.data, content=form.content.data, isparcel=form.isparcel.data,img_path=file_path, create_date=datetime.now(),book=book,user=g.user )
        db.session.add(post)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('main.index'))


    return render_template('post/post_form.html', form=form)

@bp.route('/delete/<int:post_id>')
@login_required
def delete(post_id):
    post=Post.query.get_or_404(post_id)
    user_id = session.get('user_id')
    post_list = Post.query.filter(Post.user_id == user_id).order_by(Post.create_date.desc())
    reply_list = Reply.query.filter(Reply.user_id == user_id).order_by(Reply.create_date.desc())

    if g.user != post.user:
        flash('삭제권한이 없습니다')
        return render_template('mypage/mypage_list.html', post_list=post_list, reply_list=reply_list)
    db.session.query(Reply).filter(Reply.post_id==post_id).delete(synchronize_session=False)
    db.session.delete(post)
    db.session.commit()
    post_list = Post.query.filter(Post.user_id == user_id).order_by(Post.create_date.desc())
    reply_list = Reply.query.filter(Reply.user_id == user_id).order_by(Reply.create_date.desc())
    return render_template('mypage/mypage_list.html', post_list=post_list, reply_list=reply_list)