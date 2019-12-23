# coding=utf-8
from flask import Blueprint, jsonify, current_app, request, session

house_blueprint = Blueprint('house', __name__)

from models import Area, Facility, House, HouseImage, User, Order
import json
from status_code import *


# from qiniu_sdk import put_qiniu

# 获取地区信息，并进行缓存
def get_areas():

  area_list = Area.query.all()
  area_dict_list = [area.to_dict() for area in area_list]

  return area_dict_list


# 获取设施信息并缓存
def get_facilities():
  facility_list = Facility.query.all()
  facility_dict_list = [facility.to_dict() for facility in facility_list]
  return facility_dict_list


@house_blueprint.route('/area_facility', methods=['GET'])
def newhouse():
  # 查询地址
  area_dict_list = get_areas()
  # 查询设施
  facility_dict_list = get_facilities()
  # 构造结果并返回
  return jsonify(area=area_dict_list, facility=facility_dict_list)


@house_blueprint.route('/image', methods=['POST'])
def newhouse_image():
  # 接收房屋编号
  house_id = request.form.get('house_id')
  # 接收图片信息
  f1 = request.files.get('house_image')
  # 保存到七牛云
  # url=put_qiniu(f1)
  # 保存图片对象
  image = HouseImage()
  image.house_id = house_id
  # image.url=url
  image.add_update()
  # 房屋的默认图片
  house = House.query.get(house_id)
  if not house.index_image_url:
    # house.index_image_url=url
    house.add_update()
  # 返回图片信息
  return jsonify(code=RET.OK, url= url)


@house_blueprint.route('/', methods=['POST'])
def newhouse_save():
  # 接收数据 request 中获取表单数据方法 再将其形式转换成字典
  params = request.form.to_dict()
  facility_ids = request.form.getlist('facility')
  # 验证数据的有效性

  # 创建对象并保存
  house = House()
  house.user_id = session['user_id']
  house.area_id = params.get('area_id')
  house.title = params.get('title')
  house.price = params.get('price')
  house.address = params.get('address')
  house.room_count = params.get('room_count')
  house.acreage = params.get('acreage')
  house.beds = params.get('beds')
  house.unit = params.get('unit')
  house.capacity = params.get('capacity')
  house.deposit = params.get('deposit')
  house.min_days = params.get('min_days')
  house.max_days = params.get('max_days')
  # 根据设施的编号查询设施对象
  if facility_ids:
    facility_list = Facility.query.filter(Facility.id.in_(facility_ids)).all()
    # 进行第三张表的写入
    house.facilities = facility_list
  house.add_update() # 提交表单
  # 返回结果
  return jsonify(code=RET.OK, house_id=house.id)


@house_blueprint.route('/', methods=['GET'])
def myhouse():
  user_id = session['user_id']
  user = User.query.get(user_id)
  if user:
    # 已经完成实名认证，查询当前用户的房屋信息
    house_list = House.query.filter(House.user_id == user_id).order_by(House.id.desc())
    house_list2 = []
    for house in house_list:
      house_list2.append(house.to_dict())
    return jsonify(code=RET.OK, hlist=house_list2)
  else:
    # 没有完成实名认证
    return jsonify(code=RET.USERERR)


@house_blueprint.route('/<int:id>', methods=['GET'])
def house_detail(id):
  # 查询房屋信息
  house = House.query.get(id)
  # 查询设施信息
  facility_list = get_facilities()
  # 判断当前房屋信息是否为当前登录的用户发布，如果是则不显示预订按钮
  booking = 1
  if 'user_id' in session:
    if house.user_id == session['user_id']:
      booking = 0

  return jsonify(house=house.to_full_dict(), facility_list=facility_list, booking=booking)


@house_blueprint.route('/index', methods=['GET'])
def index():
  # 查找是否登录
  code = RET.DATAERR
  user_name = ''
  if 'user_id' in session:
    user = User.query.filter_by(id=session['user_id']).first()
    user_name = user.name
    code = RET.OK
  # 返回最新的5个房屋信息
  hlist = House.query.order_by(House.id)[:5]
  hlist2 = [house.to_dict() for house in hlist]

  # 查找地区信息
  alist = get_areas()
  return jsonify(code=code, name=user_name, hlist=hlist2, alist=alist)


@house_blueprint.route('/search', methods=['GET'])
def search():
  # 接收参数
  dict = request.args
  # request.args存的都是url内的所有数据,等同于django内的request.GET
  area_id = int(dict.get('aid'))
  begin_date = dict.get('sd')
  end_date = dict.get('ed')
  sort_key = dict.get('sk')
  # 满足地区条件
  hlist = House.query.filter(House.area_id == area_id)
  # 不能查询自己发布的房源，排除当前用户发布的房屋
  if 'user_id' in session:
    hlist = hlist.filter(House.user_id != (session['user_id']))
  # 满足时间条件，当订单完成后再完成时间限制
  order_list = Order.query.filter(Order.status != 'REJECTED')

  # 情况一：
  # order_list1=Order.query.filter(Order.begin_date>=begin_date,Order.end_date<=end_date)
  # 情况二：
  order_list2 = order_list.filter(Order.begin_date < begin_date, Order.end_date > end_date)
  # 情况三：
  order_list3 = order_list.filter(Order.end_date >= begin_date, Order.end_date <= end_date)
  # 情况四：
  order_list4 = order_list.filter(Order.begin_date >= begin_date, Order.begin_date <= end_date)
  # 获取订单中的房屋编号
  house_ids = [order.house_id for order in order_list2]  # [1,2,3]
  for order in order_list3:
    house_ids.append(order.house_id)
  for order in order_list4:
    if order.house_id not in house_ids:
      house_ids.append(order.house_id)
  hlist = hlist.filter(House.id.notin_(house_ids))
  # 排序规则,默认根据最新排列
  sort = House.id.desc()
  if sort_key == 'booking':
    sort = House.order_count.desc()
  elif sort_key == 'price-inc':
    sort = House.price.asc()
  elif sort_key == 'price-des':
    sort = House.price.desc()
  hlist = hlist.order_by(sort)
  hlist2 = []
  for house in hlist:
    hlist2.append(house.to_dict())
  # 获取地区信息
  if request.args.get('area', '0') == '1':
    alist = get_areas()
  else:
    alist = []
  return jsonify(hlist=hlist2, alist=alist)
