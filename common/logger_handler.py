import logging


class LoggerHandler(logging.Logger):

    def __init__(self,
                 name="root",
                 level="DEBUG",
                 file=None,
                 formmat="%(filename)s-%(lineno)d-%(name)s-%(levelname)s-%(message)s"):
        # Logger(name)实例化
        super().__init__(name)
        # 设置级别
        self.setLevel(level)

        fmt = logging.Formatter(formmat)
        # 初始化处理器
        if file:
            file_handler = logging.FileHandler(file)
            file_handler.setLevel(level)
            file_handler.setFormatter(fmt)
            self.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        # 设置 handler的级别
        stream_handler.setLevel(level)
        stream_handler.setFormatter(fmt)
        self.addHandler(stream_handler)


# logger = LoggerHandler(config.logger_name, config.logger_file)

# if __name__ == "__main__":
#
#     logger = LoggerHandler()
#     logger.debug("fei")







