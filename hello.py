#!/usr/bin/env python 3.5
# -*- coding: utf-8 -*-
# @Time    : 2018/10/10 22:29
# @Author  : wkend
# @File    : hello.py
# @Software: PyCharm
from datetime import datetime

import flask
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
# Flask-Script是一个Flask扩展，为flask程序添加了一个命令行解释器
from flask_script import Manager

# 定义表单类
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import  DataRequired


class NameForm(Form):
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


@app.route('/')
def index_page():
    """
    利用模板来对请求进行初始化响应
    :return:
    """
    # 把current_time模板进行渲染
    return render_template('index.html', current_time=datetime.utcnow())


@app.route('/')
def bad_page():
    """
    利用重定向来处理错误的路径请求
    :return:
    """
    # return '<h1>Bad request</h1>',400   # 该视图函数返回一个400状态码
    return flask.redirect('/index.html')  # 用于处理重定向


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

if __name__ == '__main__':
    app.run(debug=True)
