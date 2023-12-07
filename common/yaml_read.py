import yaml

from config.setting import config


class YamlHanlder:

    def __init__(self, file):
        self.file = file

    def read_yaml(self, encoding="utf-8"):

        # 读取yaml配置
        with open(self.file, encoding="utf-8") as f:
            return yaml.load(f.read(), Loader=yaml.FullLoader)

    def write_yaml(self, data, encoding="utf-8"):
        """写入yaml"""
        with open(self.file, encoding=encoding, mode="w") as f:
            yaml.dump(data, stream=f, allow_unicode=True)


yaml_data = YamlHanlder(config.yaml_config_path).read_yaml()


if __name__ == "__main__":

    data = YamlHanlder(config.yaml_config_path).read_yaml()
    print(data)
