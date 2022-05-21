from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class PostForm(FlaskForm):
    subject=StringField('제목',validators=[DataRequired('제목은 필수 입력 항목입니다')]) # <input type='text'>에 대응하는 자료형, (라벨,필드값 검증)
    content=TextAreaField('내용',validators=[DataRequired('내용은 필수 입력 항목입니다')]) # <textarea>에 대응하는 자료형

class ReplyForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수 입력 항목입니다')])

class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', [DataRequired(), Email()])

class UserLoginForm(FlaskForm):
    username=StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password=PasswordField('비밀번호', validators=[DataRequired()])