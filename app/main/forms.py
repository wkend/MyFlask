from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

"""定义表单类"""
class NameForm(FlaskForm):
    """
    使用Flask-WTF时，每个Web表单都由一个继承自Form的类表示。这个类定义表单中的
    一组字段，每个字段都用对象表示。字段对象可附属一个或对个验证函数，验证函数用来
    验证用户提交的注入值是否符合要求。
    """
    # StringField类表示属性为 type="text" 的 <input> 元素
    # validators指定一个验证函数的列表，DataRequired确保提交的字段不为空
    name = StringField('What is your name?',validators=[DataRequired()])
    # SubmitField类表示属性为 type="submit" 的<input> 元素
    submit = SubmitField('Submit')


"""用户编辑器表单"""
class EditProfileForm(FlaskForm):
    """
    这个人表单中的所有字段都是可选的，所以长度验证函数允许为零
    """
    name = StringField('Real name',validators=[Length(0,64)])
    location = StringField('Location',validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('submit')

