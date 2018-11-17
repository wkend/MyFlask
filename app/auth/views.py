from  flask import render_template,redirect,request,url_for,flash
from flask_login import login_user,logout_user,login_required
from . import auth
from ..models import User
from .forms import LoginForm, ChangeEmailForm,RegisterationForm,ChangePasswordForm
from app import db
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
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next =url_for('main.index')
            return redirect(next)
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
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('register successfully!')
        # 注册完成，跳转到登录页面
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)

@auth.route('/change-password',methods=['GET','POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verfy_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template('auth/change_password.html',form=form)

@auth.route('/change_email',methods=['GET','POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        new_email = form.email.data
        token = current_user.generate_email_change_token(new_email)
        return redirect(url_for('main.index'))
    else:
        flash('Invalid email or password.')
    return render_template('auth/change_email.html',form=form)


@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('Your email address has been updated.')
    else:
        flash('Invalid request.')
    return redirect(url_for('main.index'))




# @auth.route('/confirm/<token>')
# @login_required
# def confirm(token):
#     """确认用户的账户"""
#     if current_user.confirmed:  # 判断已经登录的用户是否已经确认过
#         return redirect(url_for('main.index'))
#     if current_user.confirm(token):
#         flash('You have confirmed your account. Thanks!')
#     else:
#         flash('The confirmation link is invalid or has expired!')
#     return redirect(url_for('main.index'))

# @auth.before_app_request
# def before_request():
#     if current_user.is_authenticated:
#         current_user.ping()
#         if not current_user.confirmed and request.endpoint[:5] != 'auth.':
#             return redirect(url_for('auth.unconfirmed'))



# @auth.before_app_request    # 使用该修饰器以在蓝本中使用针对全局请求的钩子
# def before_request():
#     if current_user.is_authenticated:
#         current_user.ping() # 更新已登录用户的访问时间
#         if not current_user.confirmed and request.endpoint[:5] != 'auth.'and request.endpoint != 'static':
#             return redirect(url_for('auth.unconfirmed'))


# @auth.route('/unconfirmed')
# def unconfirmed():
#     if current_user.is_anonymous or current_user.confirmed:
#         return redirect(url_for('main.index'))
#     return render_template('auth/unconfirmed.html')

