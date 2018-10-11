#!/usr/bin/env python 3.5
# -*- coding: utf-8 -*-
# @Time    : 2018/10/10 22:29
# @Author  : wkend
# @File    : hello.py
# @Software: PyCharm

from flask import Flask,request,make_response,redirect
from flask import abort

# Flask-Script是一个Flask扩展，为flask程序添加了一个命令行解释器
from flask_script import Manager
from flask import render_template
from flask_bootstrap import Bootstrap


app = Flask(__name__)
manager = Manager(app)  # 专为flask开发的扩展都暴露在flask.ext命名空间中
bootstrap = Bootstrap(app)  #初始化Bootstrap 是客户端框架对象

@app.route('/')
def index_page():
    '''
    利用模板来对请求进行初始化响应
    :return:
    '''
    return render_template('index.html')


@app.route('/')
def bad_page():
    '''
    利用重定向来处理错误的路径请求
    :return:
    '''
    #return '<h1>Bad request</h1>',400   # 该视图函数返回一个400状态码
    return redirect('/index.html')   # 用于处理重定向

@app.route('/cookie')
def cookie_page():
    '''
    在响应对象上设置cookies
    :return:一个Response对象
    '''
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer',42)
    return response

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)


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
    manager.run()