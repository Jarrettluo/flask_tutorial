#!/usr/bin/env python
# _*_coding:utf-8 _*_
"""
@Time    :   23:22
@Auther  : Jarrett
@FileName: __init__.py
@Software: PyCharm
"""
# !/usr/bin/env python
# _*_coding:utf-8 _*_
"""
@Time    :   21:57
@Auther  : Jarrett
@FileName: app
@Software: PyCharm
"""
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(Config)
app.config['JSONIFY_MIMETYPE'] ="application/json;charset=utf-8" #指定浏览器渲染的文件类型，和解码格式；
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login = LoginManager(app)
login.login_view = 'login'
login.login_message = '你需要登录才能访问此页面。'
login.login_message_category = 'info'

mail = Mail(app)

from app.routes import *

# 添加蓝图
from .admin.view import admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix='/admin')