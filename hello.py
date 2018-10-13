#!/usr/bin/env python 3.5
# -*- coding: utf-8 -*-
# @Time    : 2018/10/10 22:29
# @Author  : wkend
# @File    : hello.py
# @Software: PyCharm
import os
from datetime import datetime

import flask
from flask import render_template,flash,session,redirect,url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
# Flask-Script是一个Flask扩展，为flask程序添加了一个命令行解释器
from flask_script import Manager
from flask_script import Shell
from flask_mail import Mail,Message
from flask_sqlalchemy import SQLAlchemy
from threading import Thread

# 定义表单类
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import  DataRequired







class NameForm(FlaskForm):
    """
    使用Flask-WTF时，每个Web表单都由一个继承自Form的类表示。这个类定义表单中的
    一组字段，每个字段都用对象表示。字段对象可附属一个或对个验证函数，验证函数用来
    验证用户提交的注入值是否符合要求。
    """
    # StringField类表示属性为 type="text" 的 <input> 元素
    # validators指定一个验证函数的列表，DataRequired确保提交的字段不为空
    name = StringField('What is your name?',validators=[DataRequired()])
    # SubmitField类表示属性为 type="submit" 的<input> 元素
    submit = SubmitField('Submit')


app = flask.Flask(__name__)
# flask-wtf用于处理web表单的扩展，
# app.config字典可以用来存储框架、扩展和程序设计本身的配置变量
# SECRET_KEY配置变量是通用秘钥
app.config['SECRET_KEY'] = 'hard to guess string'
manager = Manager(app)  # 专为flask开发的扩展都暴露在flask.ext命名空间中
bootstrap = Bootstrap(app)  # 初始化Bootstrap 是客户端框架对象
moment = Moment(app)  # 引入 moment.js,渲染本地日期和时间


# 配置数据库
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

# 创建迁移仓库
from flask_migrate import Migrate,MigrateCommand
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

# 使用Flask-Mail提供电子邮件支持
import os
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
# Flask-Mail

mail = Mail(app)
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')



# methods参数告诉flask在url映射中把这个视图函数注册为GET，POST请求的处理程序
# 如果没指定，则认为注册为GET请求的处理函数
@app.route('/',methods=['GET','POST'])
def index_page():
    """
    利用模板来对请求进行初始化响应
    在视图函数中处理表单
    重定向和用户会话
    :return:
    """
    # 把current_time模板进行渲染
    # render_template('index.html', current_time=datetime.utcnow())
    """
    form = NameForm()
    if form.validate_on_submit():  # 判断用户输入的数据是否能被所有用户所接受，若能，则返回true
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.name:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data  # 获取name值,并保存在会话中
        # 使用url_for生成路由，保证 URL 和定义的路由兼容，而且修改路由名字后依然可用，
        # url_for() 函数的第一个且唯一必须指定的参数是端点名，即路由的内部名字。默认情
        # 况下，路由的端点是相应视图函数的名字
        return redirect(url_for('index_page'))
    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'))
    """

    # 在视图函数中操作数据库
    form = NameForm()
    if form.validate_on_submit():
        # 利用过滤器进行数据库符查询
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)    #向数据库中添加数据
            session['know'] = False
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'],'New User','mail/new_user', user=user)
        else:
            session['know'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index_page'))
    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'),know=session.get('know',False))

# 为shell命令添加一个上下文，为shell命令注册一个回调函数
def make_shell_context():
    """
    我们可以做些配置，让 Flask-Script的shell命令自动导入特定的对象
    该函数注册了程序，数据库实例以及模型，因此这些数据能直接导入shell
    :return:
    """
    return dict(app=app,db=db,User=User,Role=Role)
manager.add_command("shell",Shell(make_context=make_shell_context))


@app.errorhandler(404)
def page_not_found(e):
    """
    自定义错误页面,404错误
    :return:
    """
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    """
    500错误页面
    :return:
    """
    return render_template('500.html'), 500


@app.route('/cookie')
def cookie_page():
    """
    在响应对象上设置cookies
    :return:一个Response对象
    """
    response = flask.make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', 42)
    return response


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


"""
@app.route('/user/<id>')
def get_user(id):
    '''
    用于处理错误，比如请求的用户不存在
    :param id: 请求的用户id
    :return:
    '''
    user = load_user(id)
    if not user:
        abort(404)  # abort不会把控制权交给调用它的函数，而是抛出异常把控制权交给web服务器
    return '<h1>Hello, %s</h1>',% user.name
"""

"""
@app.route('/')
def bad_page():
    '''
    利用重定向来处理错误的路径请求
    :return:
    '''
    # return '<h1>Bad request</h1>',400   # 该视图函数返回一个400状态码
    # return flask.redirect('/index.html')  # 用于处理重定向
"""

"""通过定义类来定义模型"""

# 定义Role模型
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    # 建立关系，第一个参数代表关系的另一端是哪个模型，backref向User模型中添加一个role属性
    users = db.relationship('User',backref='role',lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    # 添加到User模型中的列role.id被定义为外键，就是这个外键建立了联系,lazy参数取消自助执行查询
    role_id = db.Column(db.Integer,db.ForeignKey('role.id'))

    def __repr__(self):
        return '<User %r>' % self.username


# 异步发送电子邮件
def send_asyc_email(app,msg):
    with app.app_comtext():
        mail.send(msg)


# 邮件主题前缀
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
# 发件人地址
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <flasky@example.com>'

def send_email(to,subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,
                  sender=app.config['FLASKY_MAIL_SENDER'],recipients=[to])
    msg.body = render_template(template+'.txt',**kwargs)
    msg.html = render_template(template+'.html',**kwargs)
    t = Thread(target=send_asyc_email,args=[app,msg])
    t.start()
    return t




if __name__ == '__main__':
    manager.run()
