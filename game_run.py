from common import logger_handler
from common.Request_handler import HTTPHandler
from common.yaml_read import yaml_data
from config.setting import config
from jsonpath import jsonpath
import time
from middleware.helper import Live, login


logger = logger_handler.LoggerHandler(name=yaml_data["logger"]["name"],
                                          level=yaml_data["logger"]["level"],
                                          file=yaml_data["logger"]["file"])

jionroom = Live()
#  用户100015开播，并获取他的roomid，用户100012进入直播间
roomid = jionroom.joinRoom()
#  获取用户100012的token
test_data = login()
userId = jsonpath(test_data, "$..userId")[0]
req = HTTPHandler()
# 总盈利金额
win = 0
# 幸运次数
lucky = 0
# 运行总次数（包含幸运次数）
times = 0
# 总下注金额（花的金币总数）
bet = 0
# 总循环次数
cycles = 1
# 请求错误次数
d = 0
startimen_wm = time.time()
print(startimen_wm)
try:
    for i in range(cycles):
        res = req.visit(config.gamehost + "/luckypig/play/action",
                    method="post",
                    json={"amount": 45, "anchorId": roomid, "anchorType": 1,
                          "gameId": 3, "roomId": roomid, "userId": userId},
                    headers={"X-APP-CHANNEL": "ASO001", "X-Device-IMEI": "1",
                             "X-Device-IDFA": "1", "X-APP-VERSION": "1181", "X-Device-Model": "realme RMX2202",
                             "X-Device-ANDROIDID": "50bc5547615d713248726230b8ae297",
                             "X-Language": "zh", "X-APP-ID": "1", "Content-Type": "application/json",
                             "X-APP-KEY": "FrDdTSFF", "X-Country-Code": "cn"})
        print(res)
        if jsonpath(res, "$..code")[0] == 200:
            times += 1
            print(times)
            if jsonpath(res, "$..free")[0] == 0:
                bet += 45
            elif jsonpath(res, "$..free")[0] == 5:
                lucky += 1
            winningAmount = jsonpath(res, "$..rewards")[0]
            win += winningAmount
        else:
            d +=1
except Exception as e:
    logger.error(e)
    d +=1
endtiem_wm = time.time()

if bet == 0:
    print("返奖率0")
else:
    print("返奖率{}%".format(win/bet*100))
print("运行总次数{}".format(times))
print("总下注金额{}".format(bet))
print("幸运次数{}".format(lucky))
print("总获奖金额{}".format(win))
print("错误请求次数{}".format(d))
print("耗时总时长{}秒".format(endtiem_wm - startimen_wm))



