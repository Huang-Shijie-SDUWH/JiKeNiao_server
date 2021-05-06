import datetime

import sqlalchemy as sqlalchemy
from flask import Flask, request, jsonify, make_response
import websocket
import requests, re, os, random
import json
from flask_sqlalchemy import SQLAlchemy
import pymysql
import string
from qqbot_api import *
app = Flask(__name__)
pymysql.install_as_MySQLdb()


def ranstr(num):
    salt = ''.join(random.sample(string.ascii_letters + string.digits, num))
    return salt


class Config(object):
    """配置参数"""
    # 设置连接数据库的URL
    user = 'geek'
    password = 'Geek2021!'
    database = 'JiKeNiao'

    SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@127.0.0.1:3306/%s' % (user, password, database)

    # 设置sqlalchemy自动更跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 开启自动提交数据处理
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False

    # 查询时会不显示原始SQL语句
    SQLALCHEMY_ECHO = False


# 读取配置
app.config.from_object(Config)
# 创建数据库sqlalchemy工具对象
db = SQLAlchemy(app)


class Orders(db.Model):
    __table_args__ = {'extend_existing': True}
    # 定义表名
    __tablename__ = 'Orders'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.Integer, default=0)
    secret = db.Column(db.String(255))
    time = db.Column(db.DateTime)
    date = db.Column(db.Date)
    volunteer_id = db.Column(db.Integer)
    client_name = db.Column(db.String(255))
    major = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    qq = db.Column(db.String(255))
    system_info = db.Column(db.String(255))
    question = db.Column(db.String(255))
    category = db.Column(db.String(255))
    service_content = db.Column(db.String(255))
    fault_content = db.Column(db.String(255))
    hours = db.Column(db.Integer, default=0)
    attitude_points = db.Column(db.Integer, default=0)
    skill_points = db.Column(db.Integer, default=0)
    experience_points = db.Column(db.Integer, default=0)
    comment = db.Column(db.String(255))


class Volunteers(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'Volunteers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True)
    major = db.Column(db.String(255))
    colleague = db.Column(db.String(255))
    student_number = db.Column(db.String(255))
    order_number = db.Column(db.Integer, default=0)
    hours_of_service = db.Column(db.Integer, default=0)
    month_hours = db.Column(db.Integer, default=0)
    qq = db.Column(db.String(255), unique=True)


class Managers(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'Managers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True)

    qq = db.Column(db.Integer)


@app.route('/appointment', methods=["POST"])
def appointment():
    if request.method == 'POST':
        json_data = request.get_json()
        print(json_data)
        date = datetime.datetime.date(datetime.datetime.now())
        time = datetime.datetime.now()
        str_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        secret = ranstr(30)
        order1 = Orders(client_name=json_data['userName'], major=json_data['userMajor'],
                        phone_number=json_data['phoneNumber'],
                        qq=json_data['QQ'], system_info=json_data['computerInfo'], question=json_data['computerInfo'],
                        date=date, time=time, secret=secret)
        db.session.add(order1)
        db.session.commit()
        id = len(Orders.query.all())
        my_message = "[CQ:face,id=260][CQ:face,id=260][CQ:face,id=260]兄弟们来活啦～～" + '\n' \
                     + "\n[CQ:face,id=54]" + "订单编号：" + str(id) \
                     + "\n[CQ:face,id=54]" + "姓名：" + json_data['userName'] \
                     + '\n[CQ:face,id=54]' + "专业：" + json_data['userMajor'] \
                     + "\n[CQ:face,id=54]" + "手机号：" + json_data['phoneNumber'] \
                     + '\n[CQ:face,id=54]' + "QQ：" + json_data['QQ'] \
                     + "\n[CQ:face,id=54]" + "系统信息：" + json_data['computerInfo'] \
                     + '\n[CQ:face,id=54]' + "问题详情：" + json_data['problemDetail'] \
                     + "\n[CQ:face,id=54]" + "下单时间：" + str_time
        message_json = {}
        message_json['group_id'] = geek_group
        res = requests.post("http://0.0.0.0:" + api_port + "/send_group_msg",
                            data={'group_id': message_json['group_id'], 'message': my_message})
        response = make_response(jsonify({'message': 'OK'}, 200))
        return response


@app.route('/feedback', methods=["POST"])
def feedback():
    if request.method == 'POST':
        json_data = request.get_json()
        content = ""
        taidu = ""
        jishu = ""
        tiyan = ""
        if json_data['serverContent']['guide']: content = content + " 日常预约"
        if json_data['serverContent']['reserve']: content = content + " 产品导购"
        for i in range(json_data['attitudeStar']):
            taidu = taidu + " ⭐ "
        for i in range(json_data['skillStar']):
            jishu = jishu + " ⭐ "
        for i in range(json_data['serverStar']):
            tiyan = tiyan + " ⭐ "
        order1 = Orders.query.filter_by(secret=json_data['secret']).first()
        Orders.query.filter_by(id=order1.id).update(
            {'status': 2, 'category': content, 'fault_content': json_data['problemShow'],
             'hours': json_data['serverLast'],
             'attitude_points': json_data['attitudeStar']
                , 'skill_points': json_data['skillStar'], 'experience_points': json_data['serverStar'],
             'comment': json_data['volunteerAssess']})
        db.session.commit()
        volunteer1 = Volunteers.query.filter_by(id=order1.volunteer_id).first()
        volunteer_name = volunteer1.name
        Volunteers.query.filter_by(id=volunteer1.id).update(
            {'month_hours': volunteer1.month_hours + int(json_data['serverLast']),
             'hours_of_service': volunteer1.hours_of_service + int(json_data['serverLast']), 'order_number': volunteer1.order_number + 1})
        db.session.commit()
        my_message = "🎉🎉🎉反馈表小贴士：" + "\n" \
                     + "\n✨ " + "专业和姓名：" + order1.major \
                     + "\n✨ " + "联系方式：" + order1.phone_number \
                     + "\n✨ " + "服务内容：" + content \
                     + "\n✨ " + "故障简述：" + json_data['problemShow'] \
                     + "\n✨ " + "志愿者姓名：" + volunteer_name \
                     + "\n✨ " + "服务时长：" + str(json_data['serverLast']) \
                     + "\n✨ " + "提交预约的日期：" + str(order1.time) \
                     + "\n✨ " + "志愿者态度分：" + taidu \
                     + "\n✨ " + "志愿者技术分：" + jishu \
                     + "\n✨ " + "服务综合体验分：" + tiyan \
                     + "\n✨ " + "给志愿者的评语：" + json_data['volunteerAssess']
        message_json = {}
        message_json['group_id'] = geek_group
        send_group_msg(group_id=message_json['group_id'],msg=my_message)
        res = requests.post("http://0.0.0.0:" + api_port + "/send_group_msg",
                            data={'group_id': message_json['group_id'], 'message': my_message})
        response = make_response(jsonify({'message': 'OK'}, 200))
        return response


@app.route('/confirm', methods=["POST"])
def confirm():
    if request.method == 'POST':
        json_data = request.get_json()
        num = Orders.query.filter_by(secret=json_data['secret']).count()
        if num == 0:
            response = make_response(jsonify({'message': '查无此secret'}, 500))
            return response
        else:
            order1 = Orders.query.filter_by(secret=json_data['secret']).first()
            volunteer1 = Volunteers.query.filter_by(id=order1.volunteer_id).first()
            volunteer_name = volunteer1.name
            time1 = order1.time.strftime("%Y-%m-%d %H:%M:%S")
            response = make_response(
                jsonify({'client_name': order1.client_name, 'volunteer_name': volunteer_name, 'time': time1}),
                200)
            return response


if __name__ == "__main__":
    # db.drop_all()
    # # 创建所有表
    # db.create_all()

    app.config['SERVER_NAME'] = 'mylifemeaning.cn:8888'

    app.run('0.0.0.0', debug=True, port=8888, ssl_context=("../ssl/mylifemeaning.cn.pem", '../ssl/mylifemeaning.cn.key'))
