"""蓝本中定义的程序路由"""

from datetime import datetime

from flask import render_template, session, redirect, url_for, current_app, flash, abort
from flask_login import login_required, current_user

from .. import db
from ..models import User, Role, Permission, Post
from . import main
from .forms import EditProfileForm, PostForm, EditProfileAdminForm
from ..decorators import admin_required


"""在视图函数中操作数据库"""
@main.route('/', methods=['GET', 'POST'])
def index():
    """处理博客文章的首页路由"""
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(body=form.body.data,author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html',form=form,posts=posts)



@main.route('/user/<username>')
def user(username):
    """用户资料页面的路由"""
    #  在数据库中查找该用户
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html',user=user)


@main.route('/edit-profile',methods=['GET','POST'])
@login_required
def edit_profile():
    """普通用户资料编辑路由"""
    form = EditProfileForm()
    if form.validate_on_submit():   # 如果表单被提交，则更新表单中的各个字段
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user',username=current_user.username))
    # 未提交表单之前，各个字段都使用current_user中保存的值
    form.name.data = current_user.username
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',form=form)

@main.route('/edit-profile/<int:id>',methods=['GET','POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user',username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.role.data = user.role_id
    form.name.data = user.username
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html',form=form,user=user)




