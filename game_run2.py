import json

from common import logger_handler
from common.Request_handler import HTTPHandler
from common.yaml_read import yaml_data
from config.setting import config
from jsonpath import jsonpath
import time
from middleware.helper import Live, login
class Longin(object):

    def getUserId(self,account):
        req = HTTPHandler()
        res = req.visit(config.host + '/apis-user/authz/login/login',
                    method="post",
                    json={"account": account, "password": "88888888"},
                    headers={"X-APP-CHANNEL": "1", "X-Device-IMEI": "1", "X-Device-IDFA": "1", "X-APP-VERSION": "1",
                             "X-Device-Model": "realme RMX2202",
                             "X-Device-ANDROIDID": "50bc5547615d713248726230b8ae297",
                             "X-Language": "zh", "X-APP-ID": "1"})
        self.token = jsonpath(res, "$..token")[0]
        userid = jsonpath(res, "$..userId")[0]
        return userid
    def jionRoom(self):
        req = HTTPHandler()
        res = req.visit(config.host + '/apis-room/live/joinRoom',
                    method="post",
                    json={"roomId": "851632803459104000", "roomPassword": ""},
                    headers={"X-APP-CHANNEL": "1", "X-Device-IMEI": "1", "X-Device-IDFA": "1", "X-APP-VERSION": "1",
                             "X-Device-Model": "realme RMX2202",
                             "X-Device-ANDROIDID": "50bc5547615d713248726230b8ae297",
                             "X-Language": "zh", "X-APP-ID": "1", "X-Authorization": self.token})







class gameGun(object):

    def __init__(self):
        self.logger = logger_handler.LoggerHandler(name=yaml_data["logger"]["name"],
                                                  level=yaml_data["logger"]["level"],
                                                  file=yaml_data["logger"]["file"])
        self.result = result_data()


    def run_mian(self, cycles,userId):
        req = HTTPHandler()
        try:
            for i in range(cycles):
                res = req.visit(config.gamehost + "/luckypig/play/action",
                            method="post",
                            json={"amount": 45, "anchorId":851632803459104000, "anchorType": 1,
                                  "gameId": 3, "roomId": 851632803459104000, "userId": userId},
                            headers={"X-APP-CHANNEL": "ASO001", "X-Device-IMEI": "1",
                                     "X-Device-IDFA": "1", "X-APP-VERSION": "1181", "X-Device-Model": "realme RMX2202",
                                     "X-Device-ANDROIDID": "50bc5547615d713248726230b8ae297",
                                     "X-Language": "zh", "X-APP-ID": "1", "Content-Type": "application/json",
                                     "X-APP-KEY": "FrDdTSFF", "X-Country-Code": "cn"})

                if jsonpath(res, "$..code")[0] == 200:
                    self.result.times += 1
                    print("当前执行次数："+str(self.result.times)+ "\n")
                    if jsonpath(res, "$..free")[0] == 0:
                        self.result.bet += 45
                    elif jsonpath(res, "$..free")[0] == 5:
                        self.result.lucky += 1
                    winningAmount = jsonpath(res, "$..rewards")[0]
                    self.result.win += winningAmount
                    if jsonpath(res, "$..rewards")[0] != 0:
                        self.result.wintimes += 1
                else:
                    print(res)
                    self.result.d += 1
        except Exception as e:
            self.logger.error(e)
            self.result.d += 1

        return self.result


class result_data(object):
    def __init__(self):
        # 总盈利金额
        self.win = 0
        # 幸运次数
        self.lucky = 0
        # 运行总次数（包含幸运次数）
        self.times = 0
        # 总下注金额（花的金币总数）
        self.bet = 0
        # 请求错误次数
        self.d = 0
        # 中奖次数
        self.wintimes = 0


if __name__ =="__main__":
    login = Longin()
    userid = []
    for i in yaml_data["user4"]:
        a = login.getUserId(i)
        login.jionRoom()
        userid.append(a)




