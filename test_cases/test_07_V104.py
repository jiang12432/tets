# -*-coding:utf8-*-
import unittest
import json
from common import logger_handler, utils
from common.yaml_read import yaml_data
from libs import ddt
from common.Request_handler import HTTPHandler
from common.Excel_Heandler import ExcelHandler
from config.setting import config
from middleware.helper import Context, save_data, save_uid, Live
import warnings
import time


@ddt.ddt
class OpenLive(unittest.TestCase):
    excel_handler = ExcelHandler(config.data_path)
    data = excel_handler.read("V104")
    # 数据放到前置条件当中
    # 每一个测试用例方法执行之前都会运行的方法
    # logger传一个接收的文件名
    logger = logger_handler.LoggerHandler(name=yaml_data["logger"]["name"],
                                          level=yaml_data["logger"]["level"],
                                          file=yaml_data["logger"]["file"])
    token1 = save_data()
    room = Live()
    # 用户加入直播间，并获取直播间的roomid
    roomdd = room.joinRoom()

    def setUp(self) -> None:
        warnings.simplefilter('ignore', ResourceWarning)
        self.req = HTTPHandler()

    def tearDown(self) -> None:
        self.req.close_session()

    @ddt.data(*data)
    def test_live(self, test_data):
        if test_data["data"] is None:
            test_data["data"] = "{}"
    # 读取excel当中的headers，得到字典
        headers = json.loads(test_data["headers"])
        # 添加X-Authorization头信息
        headers["X-Authorization"] = self.token1
        if test_data["method"] =="get":
            res = self.req.visit(url=config.host + test_data["url"],
                                 method=test_data["method"],
                                 params=json.loads(test_data["data"]),
                                 headers=headers)
            print(res)
        elif test_data["method"] =="post":
            res = self.req.visit(url=config.host + test_data["url"],
                                 method=test_data["method"],
                                 json=json.loads(test_data["data"]),
                                 headers=headers)
            print(res)
        try:
            self.assertEqual(res["code"], test_data["expected"])
            self.excel_handler.write(config.data_path, "V104", test_data["case_id"] + 1, 9, "测试通过")
        except AssertionError as e:
            self.logger.error(e)
            # 手动抛出异常，否则测试用例自动通过
            self.excel_handler.write(config.data_path, "V104", test_data["case_id"] + 1, 9, "测试失败")
            raise e


if __name__ == "__main__":
    unittest.main()
