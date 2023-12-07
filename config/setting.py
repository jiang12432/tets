import os


class Config:
    # 项目路径
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 测试数据路径
    data_path = os.path.join(root_path, "data/cases.xlsx")
    # 测试用例路径
    case_path = os.path.join(root_path, "test_cases")
    # yaml路径
    config_path = os.path.join(root_path, "config")
    # 测试报告路径
    report_path = os.path.join(root_path, "report")
    game_data_path = os.path.join(root_path, "data/game_data.xlsx")
    if not os.path.exists(report_path):
        os.mkdir(report_path)

    yaml_config_path = os.path.join(config_path, "config.yaml")


class DevConfig(Config):
    # 项目域名
    host = "http://testapi.qaq888.com"
    gamehost = "http://testgame.qaq888.com"

config = DevConfig()
