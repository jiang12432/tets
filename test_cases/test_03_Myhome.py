# -*-coding:utf8-*-
import unittest
import json
from common import logger_handler, utils
from common.mysql_handler import DBHandler
import common.utils as rep
from common.yaml_read import yaml_data
from libs import ddt
from common.Request_handler import HTTPHandler
from common.Excel_Heandler import ExcelHandler
from config.setting import config
from middleware.helper import Context, save_data,save_uid
import warnings


@ddt.ddt
class OpenLive(unittest.TestCase):
    excel_handler = ExcelHandler(config.data_path)
    data = excel_handler.read("myhome")
    # 数据放到前置条件当中
    # 每一个测试用例方法执行之前都会运行的方法
    # logger传一个接收的文件名
    logger = logger_handler.LoggerHandler(name=yaml_data["logger"]["name"],
                                          level=yaml_data["logger"]["level"],
                                          file=yaml_data["logger"]["file"])

    def setUp(self) -> None:
        warnings.simplefilter('ignore', ResourceWarning)
        self.req = HTTPHandler()
        save_data()
        save_uid()
        self.token = Context.token
        self.uid = Context.uid

    def tearDown(self) -> None:
        self.req.close_session()

    @ddt.data(*data)
    def test_01_live(self, test_data):
        # dice = dict()
        # if "#uid#" in test_data["data"]:
        #     test_data["data"] = test_data["data"].replace("#uid#", str(self.uid))
        #     # 将字符串转换成json
        #     dice = json.loads(test_data["data"])
        #     # 将uid从字典里面取出并转换成int类型
        #     a = int(dice["uid"])
        #     # 赋值到字典
        #     dice["uid"] = a
        #
        #  读取excel当中的headers，得到字典
        if test_data["model_name"] != "钱包资产":
            headers = json.loads(test_data["headers"])
            # 添加X-Authorization头信息
            headers["X-Authorization"] = self.token
            res = self.req.visit(url=config.host + test_data["url"],
                                 method=test_data["method"],
                                 #  Excel表格数据转成json格式，且数据必须要用双引号
                                 params=utils.TypeConversionStrUidToInt("\"#uid#\"", test_data["data"], save_uid()),
                                 headers=headers)
            # 断言
            self.assertEqual(res["code"], test_data["expected"])
            self.assertEqual(res["status"], "success")
        else:
            headers = json.loads(test_data["headers"])
            # 添加X-Authorization头信息
            headers["X-Authorization"] = self.token
            res = self.req.visit(url=config.host + test_data["url"],
                                 method=test_data["method"],
                                 #  Excel表格数据转成json格式，且数据必须要用双引号
                                 headers=headers)


if __name__ == "__main__":
    unittest.main()
