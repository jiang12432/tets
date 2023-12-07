from common import Request_handler, yaml_read
from common.Request_handler import HTTPHandler
from common.yaml_read import yaml_data
from config import setting
from config.setting import config
from jsonpath import jsonpath
import time


def login():
    """登录，返回的是token
    1.从登录的excel当中读取
    2.从配置文件中读取
    """

    req = HTTPHandler()
    res = req.visit(config.host + '/apis-user/authz/login/login',
                    method="post",
                    json=yaml_data["user"],
                    headers={"X-APP-CHANNEL": "1", "X-Device-IMEI": "1", "X-Device-IDFA": "1", "X-APP-VERSION": "1",
                             "X-Device-Model": "realme RMX2202",
                             "X-Device-ANDROIDID": "50bc5547615d713248726230b8ae297",
                             "X-Language": "zh", "X-APP-ID": "1"})
    return res


def login2():
    req = HTTPHandler()
    res = req.visit(config.host + '/apis-user/authz/login/login',
                    method="post",
                    json=yaml_data["user2"],
                    headers={"X-APP-CHANNEL": "1", "X-Device-IMEI": "1", "X-Device-IDFA": "1", "X-APP-VERSION": "1",
                             "X-Device-Model": "realme RMX2202",
                             "X-Device-ANDROIDID": "50bc5547615d713248726230b8ae297",
                             "X-Language": "zh", "X-APP-ID": "1"})

    return res


def userlive():
    test_data = login2()
    token = jsonpath(test_data, "$..token")[0]
    Context.token1 = token
    req = HTTPHandler()
    res = req.visit(config.host + "/apis-room/live/startLive",
                    method="post",
                    json={"romTicket": "自动化测试", "roomType": 1},
                    headers={"X-APP-CHANNEL": "1", "X-Device-IMEI": "1", "X-Device-IDFA": "1", "X-APP-VERSION": "1",
                             "X-Device-Model": "realme RMX2202",
                             "X-Device-ANDROIDID": "50bc5547615d713248726230b8ae297",
                             "X-Language": "zh", "X-APP-ID": "1", "X-Authorization": token})
    return res, token


class Context:
    token = ""
    uid = ""


def save_data():
    """保存token信息
    :return:
    """
    test_data = login()
    token = jsonpath(test_data, "$..token")[0]
    Context.token = token
    return token


def save_uid():
    test_data = login()
    uid = jsonpath(test_data, "$..userId")[0]
    Context.uid = uid
    return uid


class Live(object):
    def __init__(self):
        self.test_data1 = login()
        self.token1 = jsonpath(self.test_data1, "$..token")[0]
        self.test_data = login2()
        self.token = jsonpath(self.test_data, "$..token")[0]
        time.sleep(10)

    def userLive(self):
        req = HTTPHandler()
        res = req.visit(config.host + "/apis-room/live/startLiveV2",
                        method="post",
                        json={"roomTitle": "自动化测试", "roomType": "1"},
                        headers={"X-APP-CHANNEL": "1", "X-Device-IMEI": "1", "X-Device-IDFA": "1", "X-APP-VERSION": "1",
                                 "X-Device-Model": "realme RMX2202",
                                 "X-Device-ANDROIDID": "50bc5547615d713248726230b8ae297",
                                 "X-Language": "zh", "X-APP-ID": "1", "X-Authorization": self.token})
        return res

    def save_Roomid(self):
        test_data = self.userLive()
        roomid = jsonpath(test_data, "$..roomId")[0]
        return roomid

    def joinRoom(self):
        roomdd = self.save_Roomid()
        req = HTTPHandler()
        res = req.visit(config.host + "/apis-room/live/joinRoom",
                        method="post",
                        json={"roomId": roomdd},
                        headers={"X-APP-CHANNEL": "1", "X-Device-IMEI": "1", "X-Device-IDFA": "1", "X-APP-VERSION": "1",
                                 "X-Device-Model": "realme RMX2202",
                                 "X-Device-ANDROIDID": "50bc5547615d713248726230b8ae297",
                                 "X-Language": "zh", "X-APP-ID": "1", "X-Authorization": self.token1})
        return roomdd


if __name__ == "__main__":
    a =login()
    print(a)
