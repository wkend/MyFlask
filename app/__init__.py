# 导入Flask扩展
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager
from flask_pagedown import PageDown

login_manager = LoginManager()
login_manager.session_protection = 'strong'  # 设定不同的设定等级
login_manager.login_view = 'auth.login'

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()


def create_app(config_name):
    """
    程序工厂函数
    :param config_name: 配置文件名
    """
    app = Flask(__name__)
    login_manager.init_app(app)
    pagedown.init_app(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)  # 完成对之前创建的对象的初始化
    # 附加路由和自定义的错误页面

    # 注册蓝本
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # 附加蓝本
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
