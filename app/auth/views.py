from  flask import render_template,redirect,request,url_for,flash
from flask_login import login_user,logout_user,login_required
from . import auth
from ..models import User
from .forms import LoginForm
from .forms import RegisterationForm
from app import db




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
        user = User(email=form.email.data,
                    username=form.username.data,
                    password_hash=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)




