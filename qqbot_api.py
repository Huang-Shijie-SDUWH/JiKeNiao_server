import requests, json, re
from app import db, Orders, Managers, Volunteers

api_port = '2700'
socket_port = '1700'
bot_qq = 355731725
geek_group = 224272136


def send_group_msg(msg, group_id):
    try:
        requests.post("http://0.0.0.0:" + api_port + "/send_group_msg", data={'group_id': group_id, 'message': msg})
        return "OK"
    except Exception as e:
        print("发送群消息错误：" + str(e))
        return "Error"


def send_private_msg(msg, user_id):
    try:
        requests.post("http://0.0.0.0:" + api_port + "/send_private_msg", data={'user_id': user_id, 'message': msg})
        return "OK"
    except Exception as e:
        print("发送私聊消息错误：" + str(e))
        return "Error"


def order_analysis(message):
    try:
        print("开始解析")
        aaa = re.match(r"\[CQ:reply,id=(.*)]\[CQ:at,qq=" + str(bot_qq) + "] \[CQ:at,qq=" + str(bot_qq) + "] 接单", message)
        aaa.groups()
        reply_message = get_reply_msg(aaa.group(1))
        print(reply_message)
        bbb = re.findall(r'[1-9]+\.?[0-9]*', reply_message)
        ID = int(bbb[4])
        db.session.flush()
        order1 = db.session.query(Orders).filter(Orders.id == ID).first()
        return order1
    except Exception as e:
        print("订单信息解析错误：" + str(e))


def at(ID):
    try:
        return " [CQ:at,qq=" + ID + "] "
    except:
        return " [CQ:at,qq=" + str(ID) + "] "


def reply(ID):
    try:
        return " [CQ:reply,id=" + ID + "] "
    except:
        return " [CQ:reply,id=" + str(ID) + "] "


def get_reply_msg(ID):
    res = requests.post("http://0.0.0.0:" + str(api_port) + "/get_msg",
                        data={'message_id': ID})
    reply_message = json.loads(res.content)['data']['message']
    return reply_message


def get_sender(message_json):
    return message_json['sender']['user_id']


def get_group_id(message_json):
    return message_json['group_id']


def get_message(message_json):
    return message_json['message']


def get_register_info(String):
    try:
        print(String)
        aaa = re.match(r"\[CQ:at,qq=" + str(bot_qq) + "] 志愿者注册\n姓名：(.*)\n专业：(.*)\n学院：(.*)\n学号：(.*)", String)
        if aaa == None:
            aaa = re.match(r"\[CQ:at,qq=" + str(bot_qq) + "] 志愿者注册\r\n姓名：(.*)\r\n专业：(.*)\r\n学院：(.*)\r\n学号：(.*)", String)
        return aaa
    except Exception as e:
        print("获取志愿者注册信息错误：" + str(e))