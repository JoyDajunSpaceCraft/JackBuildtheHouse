# coding=utf-8
from flask import Flask
from werkzeug.routing import BaseConverter
import os
# from flask_session import Session
# from redis import StrictRedis

BASE_DIR=os.path.dirname(os.path.abspath(__file__))

class HTMLConverter(BaseConverter):
    regex = '.*'


def create_app(config):
    app=Flask(__name__)
    app.config.from_object(config)
    app.url_map.converters['html']=HTMLConverter

    #session初始化，将session存储到redis中
    # Session(app)

    #创建redis存储对象
    # redis_store=StrictRedis(host=config.REDIS_HOST,port=config.REDIS_PORT)
    # app.redis=redis_store

    # 日志处理
    import logging
    from logging.handlers import RotatingFileHandler
    logging.basicConfig(level=logging.DEBUG)
    file_log_handler = RotatingFileHandler(os.path.join(BASE_DIR, "logs/ihome.log"), maxBytes=1024 * 1024 * 100,backupCount=10)
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    file_log_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_log_handler)

    return app

