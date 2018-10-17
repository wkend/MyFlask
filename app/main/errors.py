"""蓝本中的错误处理程序"""

from flask import render_template
from . import main


@main.app_errorhandler(404) # 使用全局修饰，注册程序全局的错误处理函数
def page_not_found(e):
    return render_template('404.html'),404

@main.app_errorhandler(500) # 使用全局修饰，注册程序全局的错误处理函数
def internal_server_error(e):
    return render_template('500.html'),500


