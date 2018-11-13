#!/usr/bin/env python 3.5
# -*- coding: utf-8 -*-
# @Time    : 2018/10/15 19:37
# @Author  : wkend
# @File    : models.py
# @Software: PyCharm


# 定义Role模型
from datetime import datetime

from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin,AnonymousUserMixin


# 定义权限常亮
class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80
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

    def __repr__(self):
        return '<Role %r>' % self.name


    @staticmethod
    def insert_roles():
        """
        通过角色名查找现有角色，然后再进行更新，只有当数据库中没有某个角色时才会创建角色
        :return:
        """
        roles = {
            'User':(Permission.FOLLOW|Permission.COMMENT|Permission.WRITE_ARTICLES,True),
            'Moderate':(Permission.FOLLOW|Permission.COMMENT|Permission.WRITE_ARTICLES|Permission.MODERATE_COMMENTS,False),
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


    def can(self,permissions):
        return self.role is not None and (self.role.permissions & permissions) == permissions


    def is_administrator(self):
        return self.can(Permission.ADMINISTER)


    # def generate_confirmation_token(self,expiration=3600):
    #     """
    #     生成一个令牌，有效期为一个小时
    #     :param expiration:秘钥
    #     :return:令牌字符串
    #     """
    #     s = Serializer(current_app.config['SECRET_KEY'],expiration)
    #     # dumps为指定的数据生成一个加密签名，然后再对数据和密码进行格式化
    #     return s.dumps({'confirm':self.id})


    # def confirm(self,token):
    #     """
    #     验证令牌,还检查令牌中的用户是否和存储在current_user中的已经登录的用户匹配
    #     :param token: 待验证的token
    #     :return: 验证结果
    #     """
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         # loads检验签名和过期时间，如果通过，会返回原始数据，否则抛出异常
    #         data = s.loads(token)
    #     except:
    #         return False
    #     if data.get('confirm') != self.id:
    #         return False
    #     self.confirmed = True
    #     db.session.add(self)
    #     return True

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