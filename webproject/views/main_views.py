from flask import Blueprint, url_for, render_template
from werkzeug.utils import redirect
bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/') #인덱스페이지
def index():
    return render_template('index/index.html')

@bp.route('/test')
def test():
    return 'test1'

@bp.route('/post')
def post():
    return redirect(url_for('post._list'))











