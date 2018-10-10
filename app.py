from flask import Flask,request

app = Flask(__name__)


@app.route('/index')
def index():
    '''
    视图函数
    :return:
    '''
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is %s!</p>' % user_agent


@app.route('/user/<name>')
def user(name):
    return "<h1>Hello %s</h1><p>Welcome!<p>" % name


if __name__ == '__main__':
    '''
    确保执行这个脚本时才启动服务器，服务器启动后进入轮询，等待并处理请求
    '''
    app.run(debug=True)   # 启动web服务器,开启调试
