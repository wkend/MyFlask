#!/usr/bin/env python 3.5
# -*- coding: utf-8 -*-
# @Time    : 2018/10/14 11:23
# @Author  : wkend
# @File    : test_basics.py.py
# @Software: PyCharm


"""
单元测试
使用python标准库中的unittest包编写。

"""
import unittest
from flask import current_app
from app import create_app,db


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        """
        测试前运行
        尝试创建一个尝试环境，类似于运行中的程序
        :return:
        """
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()


    def tearDown(self):
        """
        测试后运行
        :return:
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_app_exists(self):
        """
        确保程序实例存在
        :return:
        """
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        """
        确保程序在测试配置中运行
        :return:
        """
        self.assertTrue(current_app.config['TESTING'])
