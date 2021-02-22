#!/usr/bin/env python
# _*_coding:utf-8 _*_
"""
@Time    :   23:23
@Auther  : Jarrett
@FileName: routes
@Software: PyCharm
"""
import heapq
import os, json
import random
from datetime import time, datetime
from typing import Dict, List, Any

from flask import render_template, request, flash, redirect, url_for, jsonify
from sqlalchemy import or_

from app.forms import RegisterForm, LoginForm, PasswordResetRequestForm, ResetPasswordForm, PostTweetForm, \
    UploadPhotoForm
from app import app, bcrypt, db
from app.models import User, Post, Coin, PostComment
from flask_login import login_user, login_required, current_user, logout_user
from app.email import send_reset_password_mail, send_recharge_source_mail
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/all_posts', methods=['GET', 'POST'])
@login_required
def all_posts():
    form = PostTweetForm()

    n_followers = len(current_user.followers)
    n_followed = len(current_user.followed)

    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, 20, False)

    return render_template('all_posts.html',
                           form=form, followers=n_followers,
                           followed=n_followed, posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password = bcrypt.generate_password_hash(password)
        # bcrypt.check_password_hash(password, originpassword)
        default_img = '/static/asset/user_avatar/default/default_' + str(random.randint(1, 5)) + '.jpg'
        user = User(username=username, email=email, password=password, avatar_img=default_img, status=True, all_coins=0)
        db.session.add(user)
        db.session.commit()

        cost = 20
        describe = '新用户注册赠送20金币'
        operate = 2 # 新增
        new_coin = Coin(cost=cost, describe=describe, operate=operate)
        user.user_coins.append(new_coin)

        now_coin = user.all_coins + cost
        user.all_coins = now_coin
        db.session.add(user)
        db.session.commit()
        flash('注册成功，请登录!', category='success')
        return redirect(url_for('login'))
    else:
        flash("注册失败！请重新输入", category="danger")
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        # Check if password is matched
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            # User exists and password matched
            login_user(user, remember=remember)
            flash('登录成功', category='info')
            if request.args.get('next'):
                next_page = request.args.get('next')
                return redirect(next_page)
            return redirect(url_for('index'))
        flash('用户不存在或者密码错误', category='danger')
    # flash("请完善登录信息", category='info')
    return render_template('login.html', form=form)


@app.route("/settings")
@login_required
def settings():
    pass


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/send_password_reset_request', methods=['GET', 'POST'])
def send_password_reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        token = user.generate_reset_passpord_token()
        # print('--------------' + str(token))
        send_reset_password_mail(user, token)
        flash('Password reset request mail is sent, please check your mailbox.', category='info')
    return render_template('send_password_reset_request.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.check_reset_password_token(token)
        if user:
            password = bcrypt.generate_password_hash(form.password.data)
            user.password = password
            db.session.commit()
            flash('Your password reset is down, you can login with new password', category='info')
            return redirect(url_for('login'))
        else:
            flash('The user is not exist', category='info')
            return redirect(url_for('login'))
        # email = form.email.data
    return render_template('reset_password.html', form=form)


@app.route('/user_page/<username>')
@login_required
def user_page(username):
    user = User.query.filter_by(username=username).first()
    if user:
        n_followers = len(user.followers)
        n_followed = len(user.followed)
        # print(n_followers, n_followed)
        # print(user.followers)
        # print(user.followed)
        followers = user.followers
        followed = user.followed
        page = request.args.get('page', 1, type=int)
        posts = Post.query.filter_by(user_id=user.id).order_by(Post.timestamp.desc()).paginate(page, 20, False)
        return render_template('user_page.html', user=user, posts=posts, followers=followers,
                               followed=followed)
    else:
        return '404'


@app.route('/myPage/')
@login_required
def my_page():
    return redirect(url_for('user_page', username=current_user.username))


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user:
        current_user.follow(user)
        db.session.commit()
        page = request.args.get('page', 1, type=int)
        posts = Post.query.filter_by(user_id=user.id).order_by(Post.timestamp.desc()).paginate(page, 2, False)
        return render_template('user_page.html', user=user, posts=posts)
    else:
        return '404'


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user:
        current_user.unfollow(user)
        db.session.commit()
        page = request.args.get('page', 1, type=int)
        posts = Post.query.filter_by(user_id=user.id).order_by(Post.timestamp.desc()).paginate(page, 2, False)
        return render_template('user_page.html', user=user, posts=posts)
    else:
        return '404'


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
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
    return render_template('edit_profile.html', form=form)


@app.route('/index')
@app.route('/')
def index():
    """
    网站的首页返回内容。
    新注册的用户取全部用户的最后5名！
    :return:
    """
    posts = Post.query.order_by(Post.timestamp.desc())
    new_users = User.query.all()
    if len(new_users) > 5:
        new_users = new_users[-6:-1]
    all_posts = Post.query.all()
    if len(all_posts) > 5:
        all_posts = all_posts[-6:-1]
    if all_posts and new_users:
        for post in all_posts:
            if len(post.body) > 100:
                post.body = post.body[0:100] + "..."
        return render_template('home.html', posts=posts, new_users=new_users)
    else:
        return redirect('all_posts')


@app.route('/article_detail/<post_id>')
@login_required
def article_detail(post_id):
    post = Post.query.get(post_id)  # 根据文章ID查找
    return render_template('article_detail.html', post=post)


@app.route('/test_article/<post_id>')
@login_required
def test_article(post_id):
    post = Post.query.get(post_id)  # 根据文章ID查找
    return render_template('test_article.html', post=post)


@app.route('/search', methods=['GET', 'POST'])
def search_keyword():
    """
    全局搜索按钮！
    :return:
    """
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if request.method == 'POST':
        keyword = request.form['keyword']
        if keyword:
            result = Post.query.filter(or_(Post.body.contains(keyword),
                                           Post.title.contains(keyword))) \
                .order_by(Post.timestamp.desc())
            if result.all():
                flash('检索成功！', category='success')
                page = request.args.get('page', 1, type=int)
                posts = result.paginate(page, 20, False)
                return render_template('search_result.html', posts=posts)
            else:
                flash('没有检索到，查看全部资源', category='danger')
                return redirect('all_posts')
        else:
            return redirect('index')
    else:
        return redirect('index')


@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')


@app.route('/like/<post_id>')
@login_required
def like_post(post_id):
    username = current_user.username
    user = User.query.filter_by(username=username).first()
    post = Post.query.get(post_id)  # 根据文章ID查找
    if user and post:
        if not user.username == post.author.username:
            user.user2post.append(post)
            db.session.commit()
            return redirect(url_for('article_detail', post_id=post_id))
    return redirect(url_for('article_detail', post_id=post_id))


@app.route('/unlike/<post_id>')
@login_required
def unlike_post(post_id):
    post = Post.query.get(post_id)  # 根据文章ID查找
    if current_user in post.users:
        current_user.user2post.remove(post)  # 删除关系
        db.session.commit()
        return redirect(url_for('article_detail', post_id=post_id))
    return redirect(url_for('article_detail', post_id=post_id))


@app.route('/cash_resource/<post_id>')
@login_required
def cash_resource(post_id):
    post = Post.query.get(post_id)  # 根据文章ID查找
    if current_user == post.author:
        flash('不能兑换自己的资源', category='info')
        return redirect(url_for('article_detail', post_id=post_id))
    else:
        # 以下是结算的内容！
        cost = int(post.source_value)
        if current_user.all_coins < cost:
            flash('余额不足，不能兑换！', category='danger')
            return redirect(url_for('article_detail', post_id=post_id))
        else:
            current_user.all_coins = current_user.all_coins - cost  # 用户的总金币数减少
            describe = f'购买{post.id}_{post.title}'
            operate = 1  # 减少
            coin = Coin(cost=cost, describe=describe, operate=operate)
            current_user.user_coins.append(coin)

            post.author.all_coins = post.author.all_coins + cost
            describe = f'用户{current_user.id}_购买{post.id}'
            operate = 2  # 增加
            coin = Coin(cost=cost, describe=describe, operate=operate)
            post.author.user_coins.append(coin)
            db.session.commit()
            flash('兑换成功,请查收邮箱！', category='info')
            send_recharge_source_mail(current_user, post)
            return redirect(url_for('article_detail', post_id=post_id))


@app.route('/recommend', methods=['GET'])  # 推荐文章, 支持量最高的前十篇文章
def recommend():
    # print('这里是推荐的内容！')
    post = Post.query.all()  # 根据文章ID查找
    post_id = [post.index(i) for i in post]
    most_recommend = [len(i.users) for i in post]  # 获取每个文章的支持用户数
    all_post_dic = dict(zip(post_id, most_recommend))
    sorted_list = sorted(all_post_dic.items(), key=lambda all_post_dic: all_post_dic[1])  # 按照value进行排序
    sorted_list.reverse()  # 对列表进行反转

    # 筛选10个数
    if len(post) > 10:  # 获取总数目
        post_value = 10  # 只推荐十篇文章
    else:
        post_value = len(post)
    sorted_list = sorted_list[0:post_value]

    result, result_a = [], {}
    for lit in sorted_list:
        post_content = post[lit[0]]
        result_a['post_author'] = post_content.author.username
        result_a['post_body'] = post_content.body
        result_a['costumer'] = post_content.author.id
        result_a['post_id'] = post_content.id
        result_a['title'] = post_content.title
        result_a['timestamp'] = post_content.timestamp
        result_a['post_like_num'] = lit[1]
        result.append(result_a)
        result_a = {}
    return jsonify(result)


@app.route('/comment', methods=['GET', 'POST'])
def comment():
    resp = {}
    # print('到达comment页面！')
    if request.method == 'GET':
        args = request.args
        args = args.to_dict()  # 获取get的参数
        post_id = args['pathname'].split('/')[-1]  # 获取当前页面的id
        p1 = Post.query.filter_by(id=post_id).first()  # 筛选出当前页面的post内容
        data: List[Dict[Any, Any]] = []
        if p1:
            all_comment = p1.comment
            for comment in all_comment:
                usr_id = comment.comment_user_id
                usr_name = User.query.filter_by(id=usr_id).first().username
                usr_avaster = User.query.filter_by(id=usr_id).first().avatar_img
                struct_time = comment.comment_timestamp
                timestamp = datetime.strftime(struct_time, '%Y-%m-%d %H:%M:%S')
                data.append({
                    'msg': comment.comment_msg,
                    'timestamp': timestamp,
                    'usr_id': usr_id,
                    'usr_name': usr_name,
                    'usr_avaster': usr_avaster,
                }
                )
        resp['code'] = 200
        resp['data'] = data
        pass
    elif request.method == 'POST':
        data = json.loads(request.get_data(as_text=True))
        msg, title, username = data['comment'], data['title'], data['username']
        p1 = Post.query.filter_by(title=title).first()  # 根据标题筛选出post
        if p1:
            post_comment = PostComment(comment_msg=msg, comment_user_id=current_user.id)
            p1.comment.append(post_comment)  # post的评论添加
            db.session.commit()  # 更新数据库
            struct_time = post_comment.comment_timestamp
            timestamp = datetime.strftime(struct_time, '%Y-%m-%d %H:%M:%S')
            resp['code'] = 200
            resp['data'] = {
                'msg': post_comment.comment_msg,
                'timestamp': timestamp,
                'usr_id': post_comment.comment_user_id,
                'usr_name': current_user.username,
                'usr_avaster': current_user.avatar_img,
            }
    else:
        pass
    # print(resp)
    return jsonify(resp)


@app.route('/create', methods=['GET', 'POST'])
def create():
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
    return render_template('create_page.html', form=form)
