# encoding: utf-8
"""
@version: 1.0
@author: Jarrett
@file: view
@time: 2020/11/19 22:41
"""
from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import current_user
from app import login_required, User, Post, db, PostTweetForm, UploadPhotoForm, Coin
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg', 'gif'}

import os, json


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


user_center_blueprint = Blueprint('usercenter', __name__,
                                  template_folder='templates',
                                  static_folder='static')  # 类似于Flask应用的app对象

@login_required
@user_center_blueprint.route('/newContribute/', methods=['GET', 'POST'])
def user_new_contribute():
    form = PostTweetForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.text.data
        addr = form.source_addr.data
        post_value = form.source_value.data
        post = Post(title=title, body=body, source_addr=addr, source_value=post_value)
        current_user.posts.append(post)
        db.session.commit()
        flash('最新资源发送成功！浏览全部内容！', category='success')
        return redirect(url_for('all_posts'))
    return render_template('newContribute.html', form=form)

@login_required
@user_center_blueprint.route('/userAvatar/', methods=['GET', 'POST'])
def user_new_avatar():
    form = UploadPhotoForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        # if user does not select file, browser also
        # submit an empty part without filename
        if f.filename == '':
            flash('No selected file', category='danger')
            return redirect(request.url)
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join('app', 'static', 'asset', filename))
            current_user.avatar_img = '/static/asset/' + filename
            db.session.commit()
            return redirect(url_for('user_page', username=current_user.username))
        # f.save((os.path.join(app.instance_path, 'static/asset/', filename)))
    return render_template('userAvater.html', form=form)

@login_required
@user_center_blueprint.route('/userCollection/')
def user_collection():
    return render_template('userCollection.html')

@login_required
@user_center_blueprint.route('/userMessage/')
def user_message():
    return render_template('userMessage.html')

@login_required
@user_center_blueprint.route('/userSources/')
def user_sources():
    return render_template('userSources.html')

@login_required
@user_center_blueprint.route('/userRecharge/')
def user_recharge():
    coin_record = current_user.user_coins
    buy_num = 0
    # 计算总的消费金币数
    if coin_record:
        for record in coin_record:
            if record.operate == 1:
                buy_num = buy_num + record.cost
    page = request.args.get('page', 1, type=int)
    records = Coin.query.filter_by(user_id=current_user.id).order_by(Coin.timestamp.desc()).paginate(page, 6, False)
    return render_template('userRecharge.html', records=records, consumption=buy_num)

@login_required
@user_center_blueprint.route('/delete_post/<post_id>')
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post:
        delete_post_name = post.title
        db.session.delete(post)
        db.session.commit()
        flash(f'您已删除资源< {delete_post_name} >!', category='danger')
    return redirect(url_for('usercenter.user_sources'))
