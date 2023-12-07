import requests


class HTTPHandler(object):
    def __init__(self):
        self.session = requests.session()

    def visit(self, url, method, params=None, data=None, json=None, **kwargs):
        """
        :param url: 请求地址
        :param method: 请求方式
        :param params: 请求params格式参数
        :param data: 请求表单格式参数
        :param json: 请球json格式参数
        :param kwargs:
        :return:   返回请求结果
        :return:
        """
        res = self.session.request(method, url, params=params, data=data, json=json, **kwargs)
        try:
            return res.json()
        except ValueError:
            print("not json")

    def close_session(self):
        self.session.close()

