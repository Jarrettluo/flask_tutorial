#!/usr/bin/env python
# _*_coding:utf-8 _*_
"""
@Time    :   21:50
@Auther  : Jarrett
@FileName: forms
@Software: PyCharm
"""

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField,\
                    IntegerField

from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from app.models import User
from flask_wtf.file import FileField, FileRequired

class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min = 6, max= 20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(min = 8, max=20)])
    confirm = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password')])
    # recaptcha  = RecaptchaField()
    submit = SubmitField('注册')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('用户名已经被注册，请更换用户名重新注册。')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('Email已经被使用，请更换邮箱地址。')

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min = 6, max= 20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(min = 8, max=20)])
    remember = BooleanField('是否记住登录')
    submit = SubmitField('登录')

class PasswordResetRequestForm(FlaskForm):
    email = StringField('邮箱地址', validators=[DataRequired(), Email()])
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if not user:
            raise ValidationError('邮箱不存在，请确认。')
    submit = SubmitField('提交!')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('密码', validators=[DataRequired(), Length(min = 8, max=20)])
    confirm = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('重置')

class PostTweetForm(FlaskForm):
    title = StringField('标题',validators=[DataRequired(), Length(min=1, max=20)])
    text = TextAreaField('在这里说点什么吧，一共140字', validators=[DataRequired(), Length(min=1, max=140)])
    source_addr = StringField('资源地址，请输入网盘地址', validators=[DataRequired(), Length(min=1, max=80)])
    source_value = IntegerField('资源价值',validators=[NumberRange(min=0, max=9999)])
    submit = SubmitField('提交资源')

class UploadPhotoForm(FlaskForm):
    photo = FileField(validators=[FileRequired()])
    submit = SubmitField('提交')