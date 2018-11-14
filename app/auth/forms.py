from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,TextAreaField,SelectField
from wtforms.validators import DataRequired,Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from ..models import Role, User

"""用户登录表单"""
class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Length(1,64),
                        Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


"""用户注册表单"""
class RegisterationForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(),Length(1,64),Email()])
    # 使用WTForms的Regexp对用户名的字符进行限制，使其只能用数字、字母、下划线和点号
    username = StringField('Username',
                           validators=[DataRequired(),Length(1,64),
                            Regexp('^[A-Za-z0-9_.]*$',0,
                        'Usernames must have only letters, '
                        'numbers,dots or underscores')])
    # 为了安全起见，密码需要输入两次，使用WTForms的EqualTo进行验证
    password = PasswordField('Password',
                             validators=[DataRequired(),
                            EqualTo('password2',
                            message='Passwords must match.')])
    password2 = PasswordField('Confirm password',
                              validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self,field):
        """自定义验证函数"""
        if User.query.filter_by(email=field.data).first():
            # 利用异常将验证失败提示信息显示出来
            raise ValidationError('Email already registered')


    def validate_username(self,field):
        """自定义验证函数"""
        if User.query.filter_by(username=field.data).first():
            # 利用异常将验证失败提示信息显示出来
            raise ValidationError('Username already in use.')


class ChangePasswordForm(FlaskForm):
    """修改密码表单"""
    old_password = PasswordField('Old password',validators=[DataRequired()])
    password = PasswordField('New password',validators=[DataRequired(),EqualTo('password2',
                            message='Passwords must match.')])
    password2 = PasswordField('Confirm new password',validators=[DataRequired()])
    submit = SubmitField('Update Password')

class PasswordsetRequestForm(FlaskForm):
    email =  StringField('Email',validators=[DataRequired(),Length(1,64),Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
    password = PasswordField('New password',validators=[DataRequired(),EqualTo('password2',
                            message='Passwords must match.')])
    password2 = PasswordField('Confirm new password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')

class ChangeEmailForm(FlaskForm):
    email = StringField('New Email',validators=[DataRequired(),Length(1,64),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Update Email Address')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')