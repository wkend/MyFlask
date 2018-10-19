from  flask import render_template,redirect,request,url_for,flash
from flask_login import login_user,logout_user,login_required
from . import auth
from ..models import User
from .forms import LoginForm
from .forms import RegisterationForm
from app import db
from ..email import send_email
from flask_login import current_user


@auth.route('/login',methods=['GET','POST'])
def login():
    """用户登录"""
    form = LoginForm()
    if form.validate_on_submit():
        # 用表单中填写的email从数据库中加载用户
        user = User.query.filter_by(email=form.email.data).first()
        # 验证表单数据，
        if user is not None and user.verify_password(form.password.data):
            # 尝试登入
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html',form=form)



@auth.route('/logout')
@login_required
def logout():
    """用户登出"""
    # 调用flask_login中的logout_user函数，删除并重设会话
    logout_user()
    # 回复一个flash消息
    flash('You have been logged out')
    # 重定向，返回首页
    return redirect(url_for('main.index'))



"""用户注册路由"""
@auth.route('/register',methods=['GET','POST'])
def register():
    """用户注册"""
    form = RegisterationForm()
    if form.validate_on_submit():
        # noinspection PyArgumentList
        user = User(email=form.email.data,
                    username=form.username.data,
                    password_hash=form.password.data)
        db.session.add(user)
        db.session.commit()
        # 在重定向之前，需要发送确认邮件
        token = user.generate_confirmation_token()
        send_email(user.email,'Confirm Your Account',
                   'auth/email/confirm',user=user,token=token)
        flash('A confirmation email has been send to you by email,,,')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html',form=form)



@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    """确认用户的账户"""
    if current_user.confirmed:  # 判断已经登录的用户是否已经确认过
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired!')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    """重新发送账户确认邮件"""
    token = current_user.generate_confirmation_token()
    send_email(current_user.eamil,'Confirm You Account',
               'auth/email/confirm',user=current_user,token=token)
    flash('A new confirmation email has been sent to you by email.')
    redirect(url_for('main.index'))


@auth.before_app_request    # 使用该修饰器以在蓝本中使用针对全局请求的钩子
def before_request():
    if current_user.is_authenticated and not current_user.confirmed and request.endpoint[:5] != 'auth.'and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')
