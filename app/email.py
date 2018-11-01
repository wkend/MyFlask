# 异步发送电子邮件
from threading import Thread
from flask_mail import Message
from flask import current_app,render_template
from . import mail

def send_asyc_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject,recipients,template, **kwargs):
    """
    发送邮件
    :param subject: 邮件主题
    :param recipients: 收信人
    :param template: 邮件模板
    :param kwargs: 附加参数
    :return:
    """
    app = current_app._get_current_object()
    msg = Message(subject,recipients,sender=app.config['FLASKY_ADMIN_SENDER'])
    msg.body = render_template(template+'.txt',**kwargs)
    msg.html = render_template(template + '.html',**kwargs)
    thread = Thread(target=send_asyc_email,args=[app,msg])
    thread.start()
    return thread



