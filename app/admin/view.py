#!/usr/bin/env python
# _*_coding:utf-8 _*_
"""
@Time    :   21:02
@Auther  : Jarrett
@FileName: view
@Software: PyCharm
"""

from flask import Blueprint, render_template, flash
from app import login_required, User, Post, db
admin_blueprint = Blueprint('admin', __name__,
                            template_folder='templates',
                            static_folder='static')  # 类似于Flask应用的app对象

"""
在模板中引用蓝图，应该要使用蓝图名+.+static来引用
<link href="{{ url_for('admin.static',filename='about.css') }}">
可以使用蓝图实现子域名
"""


@admin_blueprint.route('/index')
def admin_index():
    return '<h1>this is admin blueprint</h1>'

@admin_blueprint.route('/all_users')
def all_users_page():
    print('all_users')
    users = User.query.all()
    return render_template('all_users.html', users = users)

@admin_blueprint.route('/all_posts_admin')
def all_posts_admin():
    posts = Post.query.all()
    return render_template('admin_all_posts.html', posts=posts)

@admin_blueprint.route('/delete_user/<user_id>')
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        delete_user_name = user.username
        posts = user.posts
        db.session.delete(user)
        db.session.delete(posts)
        db.session.commit()
        flash(f'您已删除用户: {delete_user_name},以及他的所有资源', category='danger')
    users = User.query.all()
    return render_template('all_users.html', users=users)

@admin_blueprint.route('/delete_post/<post_id>')
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post:
        delete_post_name = post.title
        db.session.delete(post)
        db.session.commit()
        flash(f'您已删除资源< {delete_post_name} >!', category='danger')
    posts = Post.query.all()
    return render_template('admin_all_posts.html', posts=posts)

#
def get_all_posts():
    posts = Post.query.all()
    xx_list = []
    for post in posts:
        xx_list.append(str([post.id, post.title,post.body, post.author.username]))
    xx_list = '\n'.join(xx_list)
    with open('xx.txt','w') as f:
        f.write(str(xx_list))