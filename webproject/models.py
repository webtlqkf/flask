from webproject import db

class School(db.Model): # 학교이름 모음
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200),nullable=False)

class Department(db.Model): # 학과 모음
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

class BookInfo(db.Model): # 책 정보
    __tablename__ = 'bookinfo'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200),nullable=False) #책이름
    author = db.Column(db.String(200),nullable=False) #저자
    school = db.Column(db.String(200),nullable=False) #학교
    department = db.Column(db.String(200),nullable=False) #학과
    price = db.Column(db.Integer, nullable=True, server_default='1')


class Post(db.Model): #판매페이지
    id = db.Column(db.Integer, primary_key=True)

    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(),nullable=False)
    isparcel = db.Column(db.Boolean(), nullable=True,sevrer_default='True')  # True: 택배, False: 직거래
    create_date = db.Column(db.DateTime(), nullable=False)
    img_path = db.Column(db.String(), nullable=True, server_default='1')  # 요거는 나중에 추가해보자

    book_info_id = db.Column(db.Integer, db.ForeignKey('bookinfo.id', ondelete='CASCADE'))
    book = db.relationship('BookInfo', backref=db.backref('post_set'))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True, server_default='1')
    user = db.relationship('User', backref=db.backref('post_set'))



class Reply(db.Model): #댓글
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'))
    post = db.relationship('Post',backref=db.backref('reply_set')) # Post.reply_set 하면 답글에 접근 가능
    content = db.Column(db.Text(),nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True, server_default='1')
    user = db.relationship('User', backref=db.backref('reply_set'))


class User(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
