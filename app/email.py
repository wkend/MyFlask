#!/usr/bin/env python 3.5
# -*- coding: utf-8 -*-
# @Time    : 2018/10/15 23:55
# @Author  : wkend
# @File    : email.py
# @Software: PyCharm

# 异步发送电子邮件
from threading import Thread

from flask import render_template
from flask_mail import Message

import app
from app import mail


def send_asyc_email(app, msg):
    with app.app_context():
        mail.send(msg)


# 邮件主题前缀
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
# 发件人地址
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <flasky@example.com>'


def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    t = Thread(target=send_asyc_email, args=[app, msg])
    t.start()
    return t
