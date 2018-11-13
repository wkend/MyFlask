# 异步发送电子邮件
from threading import Thread
from flask_mail import Message
from flask import current_app, render_template
from . import mail
import os


def send_asyc_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, recipients, template, **kwargs):
    """
    发送邮件
    :param subject: 邮件主题
    :param recipients: 收信人
    :param template: 邮件模板
    :param kwargs: 附加参数
    :return:
    """
    app = current_app._get_current_object()
    app.config['MAIL_DEBUG'] = True  # 开启debug，便于调试看信息
    app.config['MAIL_SUPPRESS_SEND'] = False  # 发送邮件，为True则不发送
    app.config['MAIL_SERVER'] = 'smtp.qq.com'  # 邮箱服务器
    app.config['MAIL_PORT'] = 465  # 端口
    app.config['MAIL_USE_SSL'] = True  # 重要，qq邮箱需要使用SSL
    app.config['MAIL_USE_TLS'] = False  # 不需要使用TLS
    app.config['MAIL_USERNAME'] = 'wkend@qq.com'  # 填邮箱

    app.config['MAIL_PASSWORD'] = '1394059601xxw'  # 填授权码
    app.config['MAIL_DEFAULT_SENDER'] = 'wkend@qq.com'  # 填邮箱，默认发送者

    msg = Message(subject, sender="wkend@qq.com", recipients=[recipients])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thread = Thread(target=send_asyc_email, args=[app, msg])
    thread.start()
    return thread
