#!/usr/bin/env python 3.5
# -*- coding: utf-8 -*-
# @Time    : 2018/10/15 19:37
# @Author  : wkend
# @File    : models.py
# @Software: PyCharm


# 定义Role模型
from app import db
from werkzeug.security import generate_password_hash,check_password_hash


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # 建立关系，第一个参数代表关系的另一端是哪个模型，backref向User模型中添加一个role属性
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name



class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    # 添加到User模型中的列role.id被定义为外键，就是这个外键建立了联系,lazy参数取消自助执行查询
    role_id = db.Column(db.Integer,db.ForeignKey('role.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        """
        将原始密码作为输入，以字符串形式返回密码的散列值，输出值可保存在数据库中
        :param password:密码
        :return:
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        """
        从数据库中取出密码的散列值和用户输入的密码，核对密码
        :param password:
        :return: boolean
        """
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return '<User %r>' % self.username