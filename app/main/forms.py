from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Role, User
from flask_pagedown.fields import PageDownField


"""定义表单类"""
class NameForm(FlaskForm):
    """
    使用Flask-WTF时，每个Web表单都由一个继承自Form的类表示。这个类定义表单中的
    一组字段，每个字段都用对象表示。字段对象可附属一个或对个验证函数，验证函数用来
    验证用户提交的注入值是否符合要求。
    """
    # StringField类表示属性为 type="text" 的 <input> 元素
    # validators指定一个验证函数的列表，DataRequired确保提交的字段不为空
    name = StringField('What is your name?', validators=[DataRequired()])
    # SubmitField类表示属性为 type="submit" 的<input> 元素
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    """普通用户资料编辑表单"""
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class EditProfileAdminForm(FlaskForm):
    """管理员用户编辑表单"""
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class PostForm(FlaskForm):
    """博客文章表单"""
    body = PageDownField("What's on your minds?", validators=[DataRequired()])
    submit = SubmitField('submit')
