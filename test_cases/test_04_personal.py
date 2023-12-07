# -*-coding:utf8-*-
import unittest
import json
from common import logger_handler, utils
from common.yaml_read import yaml_data
from libs import ddt
from common.Request_handler import HTTPHandler
from common.Excel_Heandler import ExcelHandler
from config.setting import config
from middleware.helper import Context, save_data, save_uid
import warnings


@ddt.ddt
class OpenLive(unittest.TestCase):
    excel_handler = ExcelHandler(config.data_path)
    data = excel_handler.read("Sheet3")
    # 数据放到前置条件当中
    # 每一个测试用例方法执行之前都会运行的方法
    # logger传一个接收的文件名
    logger = logger_handler.LoggerHandler(name=yaml_data["logger"]["name"],
                                          level=yaml_data["logger"]["level"],
                                          file=yaml_data["logger"]["file"])

    def setUp(self) -> None:
        warnings.simplefilter('ignore', ResourceWarning)
        self.req = HTTPHandler()
        self.token = save_data()

    def tearDown(self) -> None:
        self.req.close_session()

    @ddt.data(*data)
    def test_live(self, test_data):
        # 读取excel当中的headers，得到字典
        headers = json.loads(test_data["headers"])
        # 添加X-Authorization头信息
        headers["X-Authorization"] = self.token
        if test_data["data"] is None:
            test_data["data"] = "{}"

        res = self.req.visit(url=config.host + test_data["url"],
                             method=test_data["method"],
                             #  Excel表格数据转成json格式，且数据必须要用双引号
                             # {"followUserId":"sssss"}
                             json=utils.TypeConversionStrUidToInt("\"#uid#\"", test_data["data"], save_uid()),
                             headers=headers)
        # 断言
        print(res)
        self.assertEqual(res["code"], test_data["expected"])
        try:
            self.assertEqual(res["code"], test_data["expected"])
            self.excel_handler.write(config.data_path, "Sheet3", test_data["case_id"] + 1, 9, "测试通过")
        except AssertionError as e:
            self.logger.error(e)
            print(res)
            # 手动抛出异常，否则测试用例自动通过
            self.excel_handler.write(config.data_path, "Sheet3", test_data["case_id"] + 1, 9, "测试失败")
            raise e


if __name__ == "__main__":
    unittest.main()
