#!/usr/bin/env python 3.5
# -*- coding: utf-8 -*-
# @Time    : 2018/10/15 19:37
# @Author  : wkend
# @File    : models.py
# @Software: PyCharm


# 定义Role模型
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager


class Role(db.Model):
    """
    SQLAlchemy 会使用一个默认名字，但默认的表名没有遵守使用复数形式进行命名的约定，
    所以最好由我们自己来指定表名
    """
    __tablename__ = 'roles' # 指定表名
    id = db.Column(db.Integer, primary_key=True)    # 指定主键
    name = db.Column(db.String(64), unique=True)    # 不允许出现重复的值
    password_hash = db.Column(db.String(128))   # 变长字符串
    # 建立关系，第一个参数代表关系的另一端是哪个模型，backref向User模型中添加一个role属性,lazy参数取消自助执行查询
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users' # 指定表名
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    # 添加到User模型中的列role.id被定义为外键，就是这个外键建立了联系,参数 'roles.id' 表
    # 明，这列的值是 roles 表中行的 id 值。
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """
        将原始密码作为输入，以字符串形式返回密码的散列值，输出值可保存在数据库中
        :param password:密码
        :return:
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        从数据库中取出密码的散列值和用户输入的密码，核对密码
        :param password:
        :return: boolean
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

@login_manager.user_loader
def load_user(user_id):
    """
    使用回调函数，使用指定的标识符加载用户，
    :param user_id:
    :return:
    """
    # 加载用户的回调函数接受以Unicode字符串形式表示的用户标识符，
    # 如果能找到用户，这个函数必须返回用户对象；否则返回None
    return User.query.get(int(user_id))


