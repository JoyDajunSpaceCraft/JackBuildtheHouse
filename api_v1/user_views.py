# coding=utf-8
from flask import Blueprint, make_response, jsonify, request, session, current_app
from qiniu_sdk import put_qiniu
user_blueprint = Blueprint('user', __name__)

# from captcha.captcha import captcha
# from ytx_sdk.ytx_send import sendTemplateSMS
from status_code import *
import re
from models import User
import logging

@user_blueprint.route('/', methods=['POST'])
def user_register():
  # 接收参数
  dict = request.form
  mobile = dict.get('mobile')
  # imagecode=dict.get('imagecode')
  # phonecode=dict.get('phonecode')
  password = dict.get('password')
  password2 = dict.get('password2')
  # 验证参数是否存在
  if not all([mobile, password, password2]):
    return jsonify(code=RET.PARAMERR, msg=ret_map[RET.PARAMERR])

  if not re.match(r'^1[34578]\d{9}$', mobile):
    return jsonify(code=RET.PARAMERR, msg=u'手机号格式错误')
  # 验证手机号是否存在
  if User.query.filter_by(phone=mobile).count():
    return jsonify(code=RET.PARAMERR, msg=u'手机号存在')
  # 保存用户对象
  user = User()
  user.phone = mobile
  user.name = mobile
  user.password = password

  try:
    user.add_update()
    return jsonify(code=RET.OK, msg=ret_map[RET.OK])
  except:
    logging.ERROR(u'用户注册更新数据库失败，手机号：%s，密码：%s' % (mobile, password))
    return jsonify(code=RET.DBERR, msg=ret_map[RET.DBERR])


@user_blueprint.route('/', methods=['GET'])
def user_my():
  # 获取当前登录的用户
  user_id = session['user_id']
  # 查询当前用户的头像、用户名、手机号，并返回
  user = User.query.get(user_id)
  return jsonify(user=user.to_basic_dict())


#
@user_blueprint.route('/auth', methods=['GET'])
def user_auth():
  # 获取当前登录用户的编号
  user_id = session['user_id']
  print(user_id)
  # 根据编号查询当前用户
  user = User.query.get(user_id)
  # 返回用户的真实姓名、身份证号
  return jsonify(user.to_auth_dict())


@user_blueprint.route('/', methods=['POST','PUT'])
def user_profile():
  dict = request.form
  if request.method == 'POST':
    # todo 1获取前端数据
    try:
      data = request.files.get('avatar1').read()
      print(data)
    except Exception as e:
      return jsonify(errmsg='获取前端数据错误')
    # todo 2使用自定义的上传文件系统，上传图片服务器
    try:
      # filename = put_qiniu(data)
      pass
    except Exception as e:
      return jsonify(errmsg='上传失败', errcode=RET.UNKOWNERR)
  return 'ok'

  # if 'avatar1' in dict:
  #   try:
  #     # 获取头像文件
  #     f1 = request.files['avatar']
  #     # print(f1)
  #     # print(type(f1))
  #     # from werkzeug.datastructures import FileStorage
  #     # mime-type:国际规范，表示文件的类型，如text/html,text/xml,image/png,image/jpeg..
  #     if not re.match('image/.*', f1.mimetype):
  #       return jsonify(code=RET.PARAMERR)
  #   except:
  #     return jsonify(code=RET.PARAMERR)
  #   # 上传到七牛云
  #   url = put_qiniu(f1)
  #   # 如果未出错
  #   # 保存用户的头像信息
  #   try:
  #     user = User.query.get(session['user_id'])
  #     user.avatar = url
  #     user.add_update()
  #   except:
  #     logging.ERROR(u'数据库访问失败')
  #     return jsonify(code=RET.DBERR)
  # elif 'name' in dict:
  #   # 修改用户名
  #   name = dict.get('name')
  #   # 判断用户名是否存在
  #   if User.query.filter_by(name=name).count():
  #     return jsonify(code=RET.DATAEXIST)
  #   else:
  #     user = User.query.get(session['user_id'])
  #     user.name = name
  #     user.add_update()
  #     return jsonify(code=RET.OK)
  # else:
  #   return jsonify(code=RET.PARAMERR, msg=ret_map[RET.PARAMERR])



'''
RESTful API
地址中只能出现名词，表示对某个资源的操作
insert--POST
update--PUT
delete--DELETE
select one--GET /id
select where--GET  ?k1=v1&k2=v2...

登录，是对用户的查询，登录后也是在session中增加一条数据，可以写为session的post操作
'''


@user_blueprint.route('/session', methods=['POST'])
def user_login():
  # 接收参数
  dict = request.form
  mobile = dict.get('mobile')
  password = dict.get('password')
  # 验证非空
  if not all([mobile, password]):
    return jsonify(code=RET.PARAMERR, msg=ret_map[RET.PARAMERR])
  # 验证手机号是否格式正确
  if not re.match(r'^1[34578]\d{9}$', mobile):
    return jsonify(code=RET.PARAMERR, msg=u'手机号格式错误')
  # 数据处理
  try:
    user = User.query.filter_by(phone=mobile).first()
  except:
    logging.ERROR('用户登录--数据库出错')
    return jsonify(code=RET.DBERR, msg=ret_map[RET.DBERR])
  # 判断手机号是否存在
  if user:
    # 判断密码是否正确
    if user.check_pwd(password):
      session['user_id'] = user.id
      return jsonify(code=RET.OK, msg=u'ok')
    else:
      return jsonify(code=RET.PARAMERR, msg=u'密码不正确')
  else:
    return jsonify(code=RET.PARAMERR, msg=u'手机号不存在')


@user_blueprint.route('/session', methods=['GET'])
def user_is_login():
  if 'user_id' in session:
    user = User.query.filter_by(id=session['user_id']).first()
    return jsonify(code=RET.OK, name=user.name)
  else:
    return jsonify(code=RET.DATAERR)


@user_blueprint.route('/session', methods=['DELETE'])
def user_logout():
  # del session['user_id']
  session.clear()
  return jsonify(code=RET.OK)
