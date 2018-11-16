#!/usr/bin/env python 3.5
# -*- coding: utf-8 -*-
# @Time    : 2018/10/15 19:37
# @Author  : wkend
# @File    : models.py
# @Software: PyCharm


# 定义Role模型
import hashlib
from datetime import datetime

from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app,request
from flask_login import UserMixin,AnonymousUserMixin


# 定义权限常量
class Permission:
    FOLLOW = 0x01   # 关注其他用户的权限
    COMMENT = 0x02  # 发表评论的权限
    WRITE = 0x04    # 写原创文章的权限
    MODERATE_COMMENTS = 0x08    # 查处他人发表的不当权限
    ADMINISTER = 0x80   # 管理员权限
    ADMIN = 0x10



class Role(db.Model):
    """
    SQLAlchemy 会使用一个默认名字，但默认的表名没有遵守使用复数形式进行命名的约定，
    所以最好由我们自己来指定表名
    """
    __tablename__ = 'roles' # 指定表名
    id = db.Column(db.Integer, primary_key=True)    # 指定主键
    name = db.Column(db.String(64), unique=True)    # 不允许出现重复的值
    password_hash = db.Column(db.String(128))   # 变长字符串
    default = db.Column(db.Boolean,default=False)
    permissions = db.Column(db.Integer)
    # 建立关系，第一个参数代表关系的另一端是哪个模型，backref向User模型中添加一个role属性,lazy参数取消自助执行查询
    users = db.relationship('User', backref='role', lazy='dynamic')

    def has_permission(self, perm):
        return self.permissions and perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name


    @staticmethod
    def insert_roles():
        """
        通过角色名查找现有角色，然后再进行更新，只有当数据库
        有某个角色时才会创建角色
        """
        roles = {
            'User':(Permission.FOLLOW|
                    Permission.COMMENT|
                    Permission.WRITE,True),
            'Moderate':(Permission.FOLLOW|
                        Permission.COMMENT|
                        Permission.WRITE|
                        Permission.MODERATE_COMMENTS,False),
            'Administrator':(0xff,False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions= roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class User(UserMixin, db.Model):
    __tablename__ = 'users' # 指定表名
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(),default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(),default=datetime.utcnow)
    # 添加到User模型中的列role.id被定义为外键，就是这个外键建立了联系,参数 'roles.id' 表
    # 明，这列的值是 roles 表中行的 id 值。
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    avatar_hash = db.Column(db.String(32))
    posts = db.relationship('Post',backref='author',lazy='dynamic')
    # # 确认用户账户
    # confirmed = db.Column(db.Boolean,default=False)

    def __init__(self,**kwargs):
        """定义默认的用户角色"""
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = self.gravatar_hash()

    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def can(self,perm):
        return self.role is not None and self.role.has_permission(perm)


    def is_administrator(self):
        return self.can(Permission.ADMINISTER)


    def gravatar(self,size=100,default='identicon',rating='g'):
        """用户头像"""
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating
        )


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


    def ping(self):
        """刷新用户的最后访问时间"""
        self.last_seen = datetime.utcnow()
        db.session.add(self)


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


class AnonymousUser(AnonymousUserMixin):
    def can(self,permissions):
        return False


    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


class Post(db.Model):
    """定义文章模型"""
    __tablename__ = 'posts' # 表名
    id = db.Column(db.Integer,primary_key=True) # id号
    body = db.Column(db.Text)   # 正文
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow) # 时间戳
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))
