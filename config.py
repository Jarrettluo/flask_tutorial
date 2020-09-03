#!/usr/bin/env python
# _*_coding:utf-8 _*_
"""
@Time    :   23:21
@Auther  : Jarrett
@FileName: config
@Software: PyCharm
"""
import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))
    # APP MODE
    # DEBUG = True

    # Top secret of website
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    #RECAPTCHA PUBLIC KEY
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY') or 'you-will-never-guess'

    # Database configuration,首先从环境变量中获取，
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')

    # 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 设置sqlalchemy自动更跟踪数据库
    # SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 查询时会显示原始SQL语句
    # SQLALCHEMY_ECHO = True

    # 禁止自动提交数据处理
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = False

    # Flask Gmail Config
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465 # 25
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'luojiarui2@163.com'    # os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = 'LJR199308'             # os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flask Admin <luojiarui2@163.com>'




