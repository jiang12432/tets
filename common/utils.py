import json

"""
字符串替换 根据type类型替换type_data的int类型值
 :param _data: 字符串数据源（excel读取的数据） 包含type数据类型格式即可替换
 :param type_data: 需要替换的值
 :return: 返回替换后的值
 """


def TypeConversionStrUidToInt(_type="", _data="", type_data=""):
    if str(_data).find(_type) != -1:
        meData = _data.replace(_type, str(type_data))
        # 将字符串转换成json
        dice = json.loads(meData)
        # # 将uid从字典里面取出并转换成int类型
        # a = int(dice["uid"])
        # # 赋值到字典
        # dice["uid"] = a
        print(dice)
        return dice
    else:
        return json.loads(_data)


class ParameterSubstitution(object):

    def TypeConversionStrUidToInt(self, _type=None, _data="", type_data=None):
        for i, b in zip(_type,type_data):
            if str(_data).find(str(i)) != -1:
                _data = _data.replace(i, str(b))
                # 将字符串转换成json


        return _data







if __name__ == "__main__":
    a = ParameterSubstitution()
    b= ["12","34"]
    c=["3","4"]
    d= "12345"
    print(a.TypeConversionStrUidToInt(b,d,c))


