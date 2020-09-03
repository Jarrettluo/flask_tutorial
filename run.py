#!/usr/bin/env python
# _*_coding:utf-8 _*_
"""
@Time    :   23:24
@Auther  : Jarrett
@FileName: run
@Software: PyCharm
"""
from app import app, db
from app.models import User


class Init_db():
    # 删除所有表
    # db.drop_all()
    # db.create_all()
    # us1 = User(username= 'jiarui.luo', password = 'ljr', email = 'luojairui2@163.com')
    # db.session.add(us1)
    # db.session.commit()
    print('hahahh')


if __name__ == '__main__':
    # app.run(host = '0.0.0.0', debug=True)
    # Init_db()
    app.run(debug=True)
