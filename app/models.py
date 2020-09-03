#!/usr/bin/env python
# _*_coding:utf-8 _*_
"""
@Time    :   23:42
@Auther  : Jarrett
@FileName: model
@Software: PyCharm
"""
from flask import current_app
from app import db, login
import jwt
from flask_login import UserMixin
from datetime import datetime


@login.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()


followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),
                     )

# 对应用户给文章支持的关系模型
likes = db.Table('likes',
                 db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                 db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
                 )

# 对应用户购买支持的关系模型
orders = db.Table('orders',
                  db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),  # 用户id
                  db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),  # 资源id
                  db.Column('cost', db.Integer),  # 购买价格
                  db.Column('operate_time', db.DateTime, nullable=False, default=datetime.utcnow),  # 操作时间
                  db.Column('order_status', db.Integer),  # 商品状态，过去（已经购买），现在（购买中）
                  db.Column('order_email', db.String(120), nullable=False)
                  )

# 资源和用户评论之间的关系模型,关系表多对多
user_comment = db.Table('comments',
                        db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
                        db.Column('comment_id', db.Integer, db.ForeignKey('postcomment.id'), primary_key=True)
                        )


class User(db.Model, UserMixin):
    # 定义表名
    # __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    avatar_img = db.Column(db.String(120), default='/static/asset/user_avater.jpg', nullable=False)

    user_coins = db.relationship('Coin', backref='coin_host', lazy=True)  # 金币
    user_status = db.relationship('UserStatus', backref='status_host', lazy=True)

    status = db.Column(db.String(20), nullable=False)  # 用户状态，可以被举报
    all_coins = db.Column(db.Integer, nullable=False)

    user_msg = db.relationship('SiteMsg', backref='msg_host', lazy=True)  # 站内信
    posts = db.relationship('Post', backref='author', lazy=True)
    # 和Post连接，通过post.author就能找到，连接用True

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy=True), lazy=True
    )

    user2post = db.relationship('Post', secondary=likes, lazy=True,
                                primaryjoin=(likes.c.user_id == id),
                                backref=db.backref('users', lazy=True))

    # 用户订单
    user_order = db.relationship('Post', secondary=orders, lazy=True,
                                 primaryjoin=(orders.c.user_id == id),
                                 backref=db.backref('costumer', lazy=True))

    def __repr__(self):
        return '<User %r>' % self.username

    def generate_reset_passpord_token(self):
        data = jwt.encode({'id': self.id}, current_app.config['SECRET_KEY'], algorithm='HS256')
        return data

    @staticmethod
    def check_reset_password_token(token):
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithm='HS256')
            return User.query.filter_by(id=data['id']).first()
        except:
            return

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.count(user) > 0


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    body = db.Column(db.String(140), nullable=False)
    source_addr = db.Column(db.String(140), nullable=False)
    source_value = db.Column(db.Integer, nullable=False)  # 该资源所价值的积分
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # 这里是资源的评论
    comment = db.relationship("PostComment", secondary=user_comment, backref=db.backref('comments'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


# 用户金币数
class Coin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Integer, nullable=False)
    describe = db.Column(db.String(140), nullable=False)
    operate = db.Column(db.Integer, nullable=False)  # 是增加还是减少
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Post {}>'.format(self.cost)


# 用户状态，可以被举报
class UserStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    describe = db.Column(db.String(140), nullable=False)
    expired = db.Column(db.DateTime, nullable=False)  # 过期的时间
    operate_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Post {}>'.format(self.describe)


# 用户站内信
class SiteMsg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    body = db.Column(db.String(140), nullable=False)
    send_user = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Post {}>'.format(self.body)


# 资源评论
class PostComment(db.Model):
    __tablename__ = 'postcomment'
    id = db.Column(db.Integer, primary_key=True)
    comment_msg = db.Column(db.String(20), nullable=False)
    comment_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    comment_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __repr__(self):
        return '<PostComment {}>'.format(self.id)
