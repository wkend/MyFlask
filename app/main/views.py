"""蓝本中定义的程序路由"""

from datetime import datetime

from flask import render_template, session, redirect, url_for, current_app, flash, abort
from .. import db
from ..models import User
from ..email import send_email
from . import main
from .forms import NameForm

"""在视图函数中操作数据库"""
@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()  # type: NameForm
    if form.validate_on_submit():   # 判断提交的实际是否能被所有验证函数所接受
        # old_name = session.get('name')  # 会话中存储的name为前一次在表单中提交的数据
        # if old_name is not None and old_name != form.name.data: # 将提交的数据与会话中的数据比较
        #     flash('Looks like you have changed your name!')
        # 利用过滤器进行数据库符查询
        user = User.query.filter_by(username=form.name.data).first()
        # session['name'] = form.name.data
        if user is None:
            # noinspection PyArgumentList
            user = User(username=form.name.data)
            db.session.add(user)  # 向数据库中添加数据
            db.session.commit()
            session['know'] = False
            if current_app.config['FLASKY_ADMIN']:
                 send_email(current_app.config['FLASKY_ADMIN'], 'New User',
                            'mail/new_user', user=user)
        else:
            session['know'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('.index'))
    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'),
                           know=session.get('know', False))

@main.route('/user/<username>')
def user(username):
    """资料页面的路由"""
    #  在数据库中查找该用户
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html',user=user)

