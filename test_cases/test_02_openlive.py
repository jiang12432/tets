# -*-coding:utf8-*-
import unittest
import json
from common import logger_handler
from common.mysql_handler import DBHandler
from common.yaml_read import yaml_data
from libs import ddt
from common.Request_handler import HTTPHandler
from common.Excel_Heandler import ExcelHandler
from config.setting import config
from middleware.helper import Context, save_data
import warnings


@ddt.ddt
class OpenLive(unittest.TestCase):
    excel_handler = ExcelHandler(config.data_path)
    data = excel_handler.read("Sheet2")
    # 数据放到前置条件当中
    # 每一个测试用例方法执行之前都会运行的方法
    # logger传一个接收的文件名
    logger = logger_handler.LoggerHandler(name=yaml_data["logger"]["name"],
                                          level=yaml_data["logger"]["level"],
                                          file=yaml_data["logger"]["file"])

    def setUp(self) -> None:
        warnings.simplefilter('ignore', ResourceWarning)
        self.req = HTTPHandler()
        self.db = DBHandler(host=yaml_data["database"]["host"],
                            port=yaml_data["database"]["port"],
                            user=yaml_data["database"]["user"],
                            password=yaml_data["database"]["password"],
                            charset=yaml_data["database"]["charset"],
                            database=yaml_data["database"]["database"],
                            )
        save_data()
        self.token = Context.token

    def tearDown(self) -> None:
        self.req.close_session()
        self.db.close()

    @ddt.data(*data)
    def test_live(self, test_data):
        # 读取excel当中的headers，得到字典
        headers = json.loads(test_data["headers"])
        # 添加X-Authorization头信息
        headers["X-Authorization"] = self.token
        res = self.req.visit(url=config.host + test_data["url"],
                             method=test_data["method"],
                             #  Excel表格数据转成json格式，且数据必须要用双引号
                             json=json.loads(test_data["data"]),
                             headers=headers)
        # 断言
        self.assertEqual(res["code"], test_data["expected"])


if __name__ == "__main__":
    unittest.main()
