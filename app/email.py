# 异步发送电子邮件
from threading import Thread
from flask_mail import Message
import app
from . import mail
import smtplib

def send_asyc_email(app, msg):
    with app.app_context():
        mail.send(msg)

app.config['MAIL_DEBUG'] = True             # 开启debug，便于调试看信息
app.config['MAIL_SUPPRESS_SEND'] = False    # 发送邮件，为True则不发送
app.config['MAIL_SERVER'] = 'smtp.qq.com'   # 邮箱服务器
app.config['MAIL_PORT'] = 465               # 端口

# 邮件主题前缀
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Welcome to Flasky]'
# 发件人地址
# app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <wkend@qq.com>'
app.config['MAIL_USE_SSL'] = True   # 使用SSL
app.config['MAIL_DEFAULT_SENDER'] = "wkend@qq.com"
app.config['MAIL_PASSWORD'] = 'sjfetjyvttscfjfd'      # 填授权码


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
    :param recipients: 收件人邮箱地址
    :param subject: 邮件主题
    :param template: 模板
    :param kwargs: 附加参数
    :return:
    """
    # content = '这是确认邮箱，欢迎来到flask blog!'
    # msg = MIMEText(content)
    # msg['Subject'] = app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject
    # msg['body'] = render_template(template + '.txt', **kwargs)
    # msg['html'] = render_template(template + '.html', **kwargs)


    try:
        msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'],
                      recipients=['wkend@qq.com'])
        msg.html = '<h1>please confirm your email</h1><b>Hello,,,,</b>'
        thread = Thread(target=send_asyc_email, args=[app, msg])
        thread.start()
        return thread
    except smtplib.SMTPException as e:
        print('发送失败，，，'+str(e.args))



