#!/usr/bin/env python 3.5
# -*- coding: utf-8 -*-
# @Time    : 2018/10/15 20:50
# @Author  : wkend
# @File    : test_user_model.py
# @Software: PyCharm

"""密码散列化测试"""


import unittest
from app.models import User, Role, Permission, AnonymousUser


class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        # noinspection PyArgumentList
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

    # noinspection PyArgumentList
    def test_no_password_getter(self):
        u = User(password='cat')
        with self.assertRaises(AttributeError):
            u.password()


    def test_password_verrification(self):
        # noinspection PyArgumentList
        u = User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))


    def test_password_salts_are_random(self):
        # noinspection PyArgumentList
        u = User(password='cat')
        # noinspection PyArgumentList
        u2 = User(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)


    def test_roles_and_permissions(self):
        """角色或权限的单元测试"""
        Role.insert_roles()
        u = User(email='john@example.com',password='cat')
        self.assertTrue(u.can(Permission.MODERATE_COMMENTS))
        self.assertFalse(u.can(Permission.MODERATE_COMMENTS))


    def test_annoymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))