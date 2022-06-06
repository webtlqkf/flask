from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField, SelectField, IntegerField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, Email, InputRequired

class PostForm(FlaskForm):
    #post info
    subject=StringField('제목',validators=[DataRequired('제목은 필수 입력 항목입니다')]) # <input type='text'>에 대응하는 자료형, (라벨,필드값 검증)
    content=TextAreaField('내용',validators=[DataRequired('내용은 필수 입력 항목입니다')]) # <textarea>에 대응하는 자료형
    isparcel=SelectField('거래방식',choices=[('True', '택배'), ('False', '직거래')],validators=[InputRequired('거래방식을 선택해 주세요')],coerce=lambda x: x == 'True')
    #selectfield에서 True값을 반환할 때 html에서는 항상 string타입이기 때문에 이렇게 해야댐
    img = FileField('file')
    #book info
    bookname=StringField('책제목', validators=[DataRequired('책제목을 입력해 주세요')])
    author = StringField('저자',validators=[DataRequired('저자를 입력해 주세요')])
    school = StringField('학교', validators=[DataRequired('학교를 입력해 주세요')])
    department = StringField('학과',validators=[DataRequired('학과를 입력해 주세요')])
    price = IntegerField('가격', validators=[DataRequired('가격을 입력해 주세요')])


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
