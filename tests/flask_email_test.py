
from flask import Flask, request
from flask_script import Manager, Shell
from flask_mail import Mail, Message
from threading import Thread


app = Flask(__name__)
app.config['MAIL_DEBUG'] = True             # 开启debug，便于调试看信息
app.config['MAIL_SUPPRESS_SEND'] = False    # 发送邮件，为True则不发送
app.config['MAIL_SERVER'] = 'smtp.qq.com'   # 邮箱服务器
app.config['MAIL_PORT'] = 465               # 端口
app.config['MAIL_USE_SSL'] = True           # 重要，qq邮箱需要使用SSL
app.config['MAIL_USE_TLS'] = False          # 不需要使用TLS
app.config['MAIL_USERNAME'] = 'wkend@qq.com'  # 填邮箱
app.config['MAIL_PASSWORD'] = 'sjfetjyvttscfjfd'      # 填授权码
app.config['MAIL_DEFAULT_SENDER'] = 'wkend@qq.com'  # 填邮箱，默认发送者
manager = Manager(app)
mail = Mail(app)


# 异步发送邮件
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


@app.route('/')
def index():
    try:
        msg = Message(subject='hell,This is flask email test,,,',
                      sender="wkend@qq.com",  # 需要使用默认发送者则不用填
                      recipients=['wkend@qq.com'])
        # 邮件内容会以文本和html两种格式呈现，而你能看到哪种格式取决于你的邮件客户端。
        msg.body = 'sent by flask-email'
        msg.html = '<b>测试Flask发送邮件<b>'
        thread = Thread(target=send_async_email, args=[app, msg])
        thread.start()
        return '<h1>邮件发送成功</h1>'
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    manager.run()
