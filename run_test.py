
"""
收集测试用例：TestLoader
放到测试集合（测试套件）TestSuite
1.初始化TestLoader
2.testloader.discober(文件夹路径，demo_*.py),发现测试用例,默认test开头
3,如果你想运行的用例，放到指定的文件夹当中
4.运行器TestRunner，运行用例，生成测试报告
"""
import os
import unittest
from datetime import datetime
from config.setting import config
from libs.HTMLTestRunner import HTMLTestRunner

# 初始化testloader
testloader = unittest.TestLoader()
# 查找测试用例，加载
suite = testloader.discover(config.case_path)
# 生成测试报告
ts = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
file_name = "test_result_{}.html".format(ts)
file_path = os.path.join(config.report_path,
                         file_name)
with open(file_path, "wb") as f:
    # 初始化运行期，是以普通文本生成测试报告
    runner = HTMLTestRunner(f,
                            title="测试报告",
                            description="v1.0")
    runner.run(suite)
