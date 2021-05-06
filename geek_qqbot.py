import websocket
from qqbot_api import *

# 接单（发secret） 退单（改secret） 查询学时 月末发总结 志愿者注册 管理员注册


def order_receiving(message_json):
    the_message = get_message(message_json)
    sender_qq = get_sender(message_json)
    group_id = get_group_id(message_json)
    db.session.flush()
    try:
        order1 = order_analysis(the_message)
        volunteer_count = Volunteers.query.filter_by(qq=sender_qq).count()
        if order1.volunteer_id is not None:
            volunteer2 = Volunteers.query.filter_by(id=order1.volunteer_id).first()
            answer = at(sender_qq) + '该订单已被 ' + at(str(volunteer2.qq)) + "承包～"
            send_group_msg(msg=answer, group_id=group_id)
        elif volunteer_count == 0:
            answer = at(sender_qq) + ' 该用户未注册'
            send_group_msg(msg=answer, group_id=group_id)
        else:
            volunteer1 = Volunteers.query.filter_by(qq=sender_qq).first()
            Orders.query.filter_by(id=order1.id).update({'status': 1, 'volunteer_id': volunteer1.id})
            db.session.commit()
            answer = order1.secret
            send_private_msg(msg=answer, user_id=sender_qq)
            answer = at(sender_qq) + '接单成功！密钥已发送，请查收'
            send_group_msg(msg=answer, group_id=group_id)
    except Exception as e:
        print(Orders.query.count())
        print(str(e) + "接单错误")
        return


def volunteer_register(message_json):
    the_message = message_json['message']
    sender_qq = get_sender(message_json)
    group_id = get_group_id(message_json)
    try:
        aaa = get_register_info(the_message)
        volunteer1 = Volunteers(name=aaa.group(1), major=aaa.group(2), colleague=aaa.group(3),student_number=aaa.group(4), qq=sender_qq)
        if Volunteers.query.filter_by(qq=sender_qq).count() > 0:
            answer = at(sender_qq) + '该用户已注册'
            send_group_msg(group_id=group_id, msg=answer)
        else:
            db.session.add(volunteer1)
            db.session.commit()
            volunteer2 = Volunteers.query.filter_by(qq=sender_qq).first()
            name = volunteer2.name
            ID = str(volunteer2.id)
            answer = at(sender_qq) + ' 用户id' + ID + " " + name + " " + str(volunteer2.qq) + " " + "注册成功！"
            send_group_msg(group_id=group_id, msg=answer)
    except Exception as e:
        print(e)


def router(message_json):
    message = get_message(message_json)
    if message[-2:] == "接单":
        print("接单匹配成功")
        order_receiving(message_json)
        pass
    if len(message) > 30 and message[21:26] == "志愿者注册":
        print("注册匹配成功")
        volunteer_register(message_json)
        pass


def on_message(ws, message):
    message_json = json.loads(message)
    print(message_json)
    if message_json['post_type'] == 'message' and message_json['message_type'] == 'group' and message_json['group_id'] == geek_group:
        router(message_json)


def on_error(ws, error):
    print(ws)
    print(error)


def on_close(ws):
    print(ws)
    print("### closed ###")


websocket.enableTrace(True)
ws = websocket.WebSocketApp("ws://127.0.0.1:" + socket_port,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
ws.run_forever()
