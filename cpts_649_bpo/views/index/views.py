from crypt import methods

import flask
from flask import render_template, url_for, request, make_response
from flask import session
from sqlalchemy import and_, or_
from sqlalchemy.orm import sessionmaker
from werkzeug.utils import redirect
from models.models import engine, User
from . import index_blu

LOGIN_FIAG = False


@index_blu.route('/profile_v7/<user_id>')
def profile7(user_id):
    login_fiag = flask.session.get('login_flag', 'fail')

    if login_fiag == 'success':
        # 获取数据库会话类
        DBSession = sessionmaker(bind=engine)
        # 创建会话对象
        session = DBSession()
        # 根据userid查询到user对象
        user = session.query(User).filter(User.user_id == user_id).one()
        # 会话关闭
        session.close()
        print(user.user_name)
        print('session运行')
        return render_template('index/profile.html', user_name=user.user_name, short_description=user.short_description
                               , head_img=user.head_img)
    else:
        return '你还没有登录，请先<a href="http://127.0.0.1:5000/index/login.html">登录</a>'


# @index_blu.route('/index.html')
# def index():
#     return 'index--'

@index_blu.route('/login.html')
def login():
    '''显示登录页面'''
    return render_template('index/login.html')


@index_blu.route('/login', methods=['GET', 'POST'])
def login_vf():
    '''处理登录验证'''
    print('登录验证')
    username = request.form.get('username')
    password = request.form.get('password')
    print(username, password)
    DBsession = sessionmaker(bind=engine)
    sqlsession = DBsession()
    global LOGIN_FIAG
    try:
        obj = sqlsession.query(User).filter(and_(User.user_id == username, User.password == password)).one()
        print(obj)
    except:
        # response = "登录失败...<br>"
        # LOGIN_FIAG = False
        response = make_response('"登录失败...请<a href="http://127.0.0.1:5000/index/login.html">重新登录</a>"')
        # cook当验证失败的时候就会发出false
        # response.set_cookie('login_flg', 'False')
        # 升级为session
        session['login_flag'] = 'fail'
    else:
        # 验证通过重定向去用户页面
        LOGIN_FIAG = True
        response = redirect(url_for('index.profile7', user_id=username))
        # 当验证成功的时候就会返回TRUE，设置cook的时长为60秒
        # response.set_cookie('login_flg', 'True', max_age=60)
        # 升级为session
        session['login_flag'] = 'success'

    # @index_blu.route("/logout")
    # def logout():
    #     response = redirect(url_for("index.login"))
    #     response.delete_cookie("login_flag")
    #     return response
    finally:
        sqlsession.close()
    '''返回各自的数值'''
    return response


# 注册页面
@index_blu.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        # 如果是get请求  就是请求页面
        return render_template("index/register.html")

    elif request.method == "POST":
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        captcha = request.form.get('captcha')

        print(email, password, name)
        print(captcha)
        if not (email and password and name and captcha):
            ret = {
                'status': 1,
                'msg': '缺少参数'
            }
            return flask.jsonify(ret)

            # 从session里面取出验证码
        session_captcha = session.get('captcha')
        # 如果session_captcha不等于captcha的话
        if session_captcha.lower() != captcha.lower():
            ret = {
                'status': 3,
                'msg': '验证码错误'
            }
            return flask.jsonify(ret)

        # 业务处理：注册用户
        # 判断是否注册过
        # 1. 业务处理
        db_session = sessionmaker(bind=engine)()  # 生成会话对象
        # 去数据库查询 获取结果的第一条数据
        user_ret = db_session.query(User).filter(or_(User.email == email, User.user_name == name)).first()
        if user_ret:
            # 2. 如果邮箱或者用户名已经存在，则不允许使用
            # 3. 返回对应的数据
            ret = {
                "status": 1,
                "msg": "邮箱或用户名已存在，请修改"
            }
        else:
            # 3. 未注册，那么则进行注册
            new_user = User(email=email, user_id=name, password=password, user_name=name)
            db_session.add(new_user)
            db_session.commit()
            # 3. 返回对应的数据
            ret = {
                "status": 0,
                "msg": "注册成功"
            }
        db_session.close()
        return flask.jsonify(ret)


from utils.captcha.captcha import captcha


@index_blu.route("/captcha")
def generate_captcha():
    # 1. 获取到当前的图片编号id
    captcah_id = request.args.get('id')

    print(type(captcah_id), captcah_id)

    # 2. 生成验证码
    # 返回保存的图片名字  验证码值  图片二进制内容
    name, text, image = captcha.generate_captcha()

    # print("注册时的验证码为：", name, text, image)  # 图片名字  验证码值  图片二进制内容

    # 3. 将生成的图片验证码值作为value，存储到session中
    session["captcha"] = text
    print(text)
    print(111)
    # 返回响应内容
    resp = make_response(image)
    # 设置内容类型
    resp.headers['Content-Type'] = 'image/jpg'
    return resp


@index_blu.route("/logout")
# 退出函数
def logout():
    response = redirect(url_for("index.login"))
    response.delete_cookie("login_flag")
    return response
