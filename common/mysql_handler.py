"""
python 操作数据库
mysql，oracle，sqlserver，mongodb
操作MYSQL数据库，db-api，pymysql

"""
import pymysql
from pymysql.cursors import DictCursor

from common import yaml_read
from common.yaml_read import yaml_data
from config.setting import config


class DBHandler(object):

    def __init__(self, host, port, user, password, charset, database=None, cursorclass=DictCursor, **kw):
        """初始化"""
        # 第一步  建立连接 注意utf-8 要写成utf8
        self.conn = pymysql.connect(host=host,
                                    port=port,
                                    user=user,
                                    password=password,
                                    charset=charset,
                                    database=database,
                                    cursorclass=cursorclass,
                                    **kw)
        # 第二步  游标，数据库操作当中的一个概念,初始化游标
        self.cursor = self.conn.cursor()

    def query(self, sql, args=None, one=True):
        """查询语句"""
        # 执行sql语句
        self.cursor.execute(sql, args)
        # 提交事务
        self.conn.commit()
        # 获取结果
        if one:
            return self.cursor.fetchone()
        else:
            return self.cursor.fetchall()

    def close(self):
        """关闭连接"""
        self.cursor.close()
        self.conn.close()


if __name__ == "__main__":
    db = DBHandler(host=yaml_data["database"]["host"],
                   port=yaml_data["database"]["port"],
                   user=yaml_data["database"]["user"],
                   password=yaml_data["database"]["password"],
                   charset=yaml_data["database"]["charset"],
                   database=yaml_data["database"]["database"],
                   )

    res = db.query("select * from sys_role")
    print(res)
