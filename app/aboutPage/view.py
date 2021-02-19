# encoding: utf-8
"""
@version: 1.0
@author: Jarrett
@file: view
@time: 2021/2/19 18:41
"""
from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import current_user
from app import login_required, User, Post, db, PostTweetForm, UploadPhotoForm, Coin
from werkzeug.utils import secure_filename

# 类似于Flask应用的app对象
about_page_blueprint = Blueprint('aboutPage', __name__,
                                 template_folder='templates',
                                 static_folder='static')


@login_required
@about_page_blueprint.route('/', methods=['GET', 'POST'])
def index():
    return render_template('about.html')
