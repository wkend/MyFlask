# 异步发送电子邮件
from threading import Thread
from flask import render_template
from flask_mail import Message
import app
from app import mail
import smtplib
from email.mime.text import MIMEText

def send_asyc_email(app, msg):
    with app.app_context():
        mail.send(msg)


# 邮件主题前缀
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
# 发件人地址
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <wkend@qq.com>'
# 开启邮件发送异常模块的使用
app.config['MAIL_USE_SSL'] = True

# def send_email(to, subject, template, **kwargs):
#     msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
#                   sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
#     msg.body = render_template(template + '.txt', **kwargs)
#     msg.html = render_template(template + '.html', **kwargs)
#     t = Thread(target=send_asyc_email, args=[app, msg])
#     t.start()
#     return t


def send_email(recipients, subject, template, **kwargs):
    """
    发送邮件
    :param recipients:
    :param subject:
    :param template:
    :param kwargs:
    :return:
    """
    content = '这是确认邮箱，欢迎来到flask blog!'
    msg = MIMEText(content)
    msg['Subject'] = app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject
    msg['body'] = render_template(template + '.txt', **kwargs)
    msg['html'] = render_template(template + '.html', **kwargs)


    s = smtplib.SMTP_SSL("smtp.qq.com",465) # 配置邮件发送服务器
    try:
        s.login(app.config['FLASK_ADMIN_SENDER'],app.config['FLASK_ADMIN_AUTHORIZATION_CODE'])
        s.sendmail(app.config['FLASK_ADMIN_SENDER'],recipients,msg.as_string())
        print('发送成功！')
        t = Thread(target=send_asyc_email, args=[app, msg])
        t.start()
        return t
    except smtplib.SMTPException as e:
        print('发送失败，，，')
    finally:
        s.quit()



