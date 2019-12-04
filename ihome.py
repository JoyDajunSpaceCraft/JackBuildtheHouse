#coding=utf-8

#1、创建app对象
from manager import create_app
from config import DevelopConfig
app=create_app(DevelopConfig)

#2、初始化数据库
from models import db
db.init_app(app)

#3、创建管理对象
from flask_script import Manager
manager=Manager(app)

#4、添加迁移命令
from flask_migrate import Migrate,MigrateCommand
Migrate(app,db)
manager.add_command('db',MigrateCommand)

#5、注册蓝图
from html_views import html_blueprint
app.register_blueprint(html_blueprint)

from api_v1.user_views import user_blueprint
app.register_blueprint(user_blueprint,url_prefix='/api/v1/user')

from api_v1.house_views import house_blueprint
app.register_blueprint(house_blueprint,url_prefix='/api/v1/house')

from api_v1.order_views import order_blueprint
app.register_blueprint(order_blueprint,url_prefix='/api/v1/order')

#钩子，是否包含token
# from flask import request,jsonify,current_app
# from status_code import *
# @app.before_request
# def check_token():
#     if request.path.startswith('/api'):
#         if 'token' not in request.args or request.args.get('token')!=current_app.config['TOKEN']:
#             return jsonify(code=RET.REQERR)

if __name__ == '__main__':
    manager.run()
