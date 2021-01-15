#!/usr/bin/env python
# _*_coding:utf-8 _*_
"""
@Time    :   21:40
@Auther  : Jarrett
@FileName: email.py
@Software: PyCharm
"""
from flask import current_app, render_template
from flask_mail import Message
from app import mail, app
from threading import Thread

def send_async_mail(app, msg):
    with app.app_context():
        mail.send(msg)

def send_reset_password_mail(user, token):
    msg = Message("Flask website information",
                    sender=current_app.config['MAIL_USERNAME'],
                    recipients= [user.email] ,
                    html=render_template('reset_password_mail.html', user = user, token = token)
                  )
    #mail.send(msg)
    Thread(target=send_async_mail, args=(app, msg)).start() # 开启新的线程


def send_recharge_source_mail(user, post):
    """

    :param user:
    :param post:
    :return:
    """
    msg = Message("资源信息网回复邮件，请查收！",
                    sender=current_app.config['MAIL_USERNAME'],
                    recipients= [user.email],
                    html=render_template('send_source_to_user_mail.html', user = user, post = post)
                  )
    Thread(target=send_async_mail, args=(app, msg)).start() # 开启新的线程

