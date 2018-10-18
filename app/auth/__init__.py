#!/usr/bin/env python 3.5
# -*- coding: utf-8 -*-
# @Time    : 2018/10/15 20:59
# @Author  : wkend
# @File    : __init__.py.py
# @Software: PyCharm



from flask import Blueprint

"""创建用户认证蓝本对象"""
auth = Blueprint('auth',__name__)


from . import views # 从views模块中引入路由