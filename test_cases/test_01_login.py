# -*-coding:utf8-*-
import unittest
import json
from common import logger_handler
from common.mysql_handler import DBHandler
from common.yaml_read import yaml_data
from libs import ddt
from common.Request_handler import HTTPHandler
from common.Excel_Heandler import ExcelHandler
# 此路径为绝对路径
from config.setting import config


@ddt.ddt
class TestLogin(unittest.TestCase):
    excel_handler = ExcelHandler(config.data_path)
    data = excel_handler.read("Sheet1")
    # 数据放到前置条件当中
    # 每一个测试用例方法执行之前都会运行的方法
    # logger传一个接收的文件名
    logger = logger_handler.LoggerHandler(name=yaml_data["logger"]["name"],
                                          level=yaml_data["logger"]["level"],
                                          file=yaml_data["logger"]["file"])

    def setUp(self) -> None:
        self.req = HTTPHandler()
        self.db = DBHandler(host=yaml_data["database"]["host"],
                            port=yaml_data["database"]["port"],
                            user=yaml_data["database"]["user"],
                            password=yaml_data["database"]["password"],
                            charset=yaml_data["database"]["charset"],
                            database=yaml_data["database"]["database"],
                            )

    @ddt.data(*data)
    def test_login_success(self, test_data):
        """通过成功"""
        # 访问接口得到结果
        res = self.req.visit(config.host + test_data["url"],
                             test_data["method"],
                             #  Excel表格数据转成json格式，用json标准库，且数据必须要用双引号
                             json=json.loads(test_data["data"]),
                             headers=json.loads(test_data["headers"]))

        try:
            self.assertEqual(res["code"], test_data["expected"])
            self.excel_handler.write(config.data_path, "Sheet1", test_data["case_id"] + 1, 9, "测试通过")
        except AssertionError as e:
            self.logger.error(e)
            print(res)
            # 手动抛出异常，否则测试用例自动通过
            self.excel_handler.write(config.data_path, "Sheet1", test_data["case_id"] + 1, 9, "测试失败")
            raise e

    def tearDown(self) -> None:
        self.req.close_session()
        self.db.close()


# 以python脚本方式去执行才会执行的


if __name__ == "__main__":
    unittest.main()
