from flask import Flask, render_template
from sqlalchemy.orm import sessionmaker

from models.models import engine, User

from . import admin_blu

@admin_blu.route('/index.html')
def index2():
    # 进入本地地址
    return render_template('admin/index.html')


@admin_blu.route('/tables.html')
def tables():
    # 进入本地地址
        DBSession = sessionmaker(bind=engine)  # 创建与数据库的会话，返回的是一个类
        session = DBSession()  # 生成会话对象
        # 查询user表中所有的用户数据
        all_user_info = session.query(User).all()
        print(all_user_info)
        # 关闭session
        session.close()
        # return render_template("index.html")
        return render_template('admin/tables.html', user_infos=all_user_info)