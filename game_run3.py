# -*- coding: UTF-8 -*-
"""
@Time ： 2022/5/7 14:32
@Auth ： rs
"""
import json
import time
from concurrent.futures import ThreadPoolExecutor
# 定义一个准备作为线程任务的函数
import openpyxl as openpyxl
import openpyxl
from common.yaml_read import yaml_data
from game_run2 import Longin, gameGun

login = Longin()
userid = []
for i in yaml_data["user4"]:
    a = login.getUserId(i)
    login.jionRoom()
    userid.append(a)
starttime = int(time.time())
print(starttime)


def action(userid):
    gamastart = gameGun()
    # 输入需要循环的次数
    b = gamastart.run_mian(50000, userid)
    return b


# 创建一个包含2条线程的线程池
pool = ThreadPoolExecutor(max_workers=19)

# 向线程池提交一个task，并添加进列表中
future = []
for i in userid:
    future.append(pool.submit(action, i))
    print("启动线程")

# 获取结果
# 总盈利金额
win_all = 0
# 幸运次数
lucky_all = 0
# 总次数（包含幸运次数,但不包含错误次数），请求次数错误次数+总次数
times_all = 0
# 总下注金额（花的金币总数）
bet_all = 0
# 请求错误次数
d_all = 0
# 返奖率
probability = 0
# 总中奖次数
wintimes_all = 0
# 获得单个线程的结果，将获得的对象转换成字典
winB = 0
for f in future:
    a_dict = json.loads(json.dumps(f.result().__dict__))
    dict_key = a_dict.keys()
    # 将取出的字典的key对应的值并相加
    for e in dict_key:
        if e == "win":
            win_all += a_dict.get("win")
        elif e == "lucky":
            lucky_all += a_dict.get("lucky")
        elif e == "times":
            times_all += a_dict.get("times")
        elif e == "bet":
            bet_all += a_dict.get("bet")
        elif e == "wintimes":
            wintimes_all += a_dict.get("wintimes")
        else:
            d_all += a_dict.get("d")
if bet_all != 0:
    probability = win_all / bet_all * 100
else:
    probability = 0
endtime = int(time.time())
longtime = endtime - starttime
winB = wintimes_all / times_all
print(winB)
# 将结果些人excel

wb = openpyxl.load_workbook(r"C:\Users\86187\PycharmProjects\KD接口自动化\data\gama_data.xlsx")
wa = wb.active
wa.append([win_all, lucky_all, times_all, bet_all, d_all, probability, longtime, wintimes_all, winB])
wb.save()
wb.close()
# excel_handler = ExcelHandler(r"C:\Users\86187\PycharmProjects\KD接口自动化\data\gama_data.xlsx")
# excel_handler.read("Sheet1")
# excel_handler.write(r"C:\Users\86187\PycharmProjects\KD接口自动化\data\gama_data.xlsx", "Sheet1", + 2, 1, win_all)
# excel_handler.write(r"C:\Users\86187\PycharmProjects\KD接口自动化\data\gama_data.xlsx", "Sheet1", + 2, 2, lucky_all)
# excel_handler.write(r"C:\Users\86187\PycharmProjects\KD接口自动化\data\gama_data.xlsx", "Sheet1", + 2, 3, times_all)
# excel_handler.write(r"C:\Users\86187\PycharmProjects\KD接口自动化\data\gama_data.xlsx", "Sheet1", + 2, 4, bet_all)
# excel_handler.write(r"C:\Users\86187\PycharmProjects\KD接口自动化\data\gama_data.xlsx", "Sheet1", + 2, 5, d_all)
# excel_handler.write(r"C:\Users\86187\PycharmProjects\KD接口自动化\data\gama_data.xlsx", "Sheet1", + 2, 6, probability)
# excel_handler.write(r"C:\Users\86187\PycharmProjects\KD接口自动化\data\gama_data.xlsx", "Sheet1", + 2, 7, longtime)
# excel_handler.write(r"C:\Users\86187\PycharmProjects\KD接口自动化\data\gama_data.xlsx", "Sheet1", + 2, 8, wintimes_all)
# excel_handler.write(r"C:\Users\86187\PycharmProjects\KD接口自动化\data\gama_data.xlsx", "Sheet1", + 2, 9, winB)
print(win_all)
print(bet_all)
print(times_all)
print(d_all)
print(lucky_all)
print(wintimes_all)

# 关闭线程池
pool.shutdown()
