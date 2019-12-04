# coding=utf-8
from flask import Blueprint,jsonify,request,session
order_blueprint=Blueprint('order',__name__)
from datetime import datetime
from models import House,Order
from status_code import RET,ret_map
from my_decorators import is_login
import logging

#查询指定编号的房屋信息
@order_blueprint.route('/house/<int:id>')
def booking_house(id):
    house=House.query.get(id)
    return jsonify(house=house.to_dict())

#创建订单
@is_login
@order_blueprint.route('/',methods=['POST'])
def booking():
    #接收参数
    dict=request.form
    house_id=int(dict.get('house_id'))
    start_date=datetime.strptime(dict.get('start_date'),'%Y-%m-%d')
    end_date=datetime.strptime(dict.get('end_date'),'%Y-%m-%d')
    #验证有效性
    if not all([house_id,start_date,end_date]):
        return jsonify(code=RET.PARAMERR,msg=ret_map[RET.PARAMERR])
    if start_date>end_date:
        return jsonify(code=RET.PARAMERR,msg=ret_map[RET.PARAMERR])
    #查询房屋对象
    try:
        house=House.query.get(house_id)
    except:
        logging.error(u'下订单-查询房屋出错，房屋编号%d'%house_id)
        return jsonify(code=RET.DBERR,msg=ret_map[RET.DBERR])
    #创建订单对象
    order=Order()
    order.user_id=session['user_id']
    order.house_id=house_id
    order.begin_date=start_date
    order.end_date=end_date
    order.days=(end_date-start_date).days+1
    order.house_price=house.price
    order.amount=order.days*order.house_price

    try:
        order.add_update()
    except:
        logging.error(u'下订单-出错')
        return jsonify(code=RET.DBERR,msg=ret_map[RET.DBERR])

    #返回信息
    return jsonify(code=RET.OK)

#作为租客查询订单
@is_login
@order_blueprint.route('/',methods=['GET'])
def orders():
    uid=session['user_id']
    order_list=Order.query.filter(Order.user_id==uid).order_by(Order.id.desc())
    order_list2=[order.to_dict() for order in order_list]
    return jsonify(olist=order_list2)

#作为房东查询订单
@is_login
@order_blueprint.route('/fd',methods=['GET'])
def lorders():
    uid=session['user_id']
    #查询当前用户的所有房屋编号
    hlist=House.query.filter(House.user_id==uid)
    hid_list=[house.id for house in hlist]
    #根据房屋编号查找订单
    order_list=Order.query.filter(Order.house_id.in_(hid_list)).order_by(Order.id.desc())
    #构造结果
    olist=[order.to_dict() for order in order_list]
    return jsonify(olist=olist)

#修改状态
@order_blueprint.route('/<int:id>',methods=['PUT'])
def status(id):
    #接收参数：状态
    status=request.form.get('status')
    #查找订单对象
    order=Order.query.get(id)
    #修改
    order.status=status
    #如果是拒单，需要添加原因
    if status=='REJECTED':
        order.comment=request.form.get('comment')
    #保存
    order.add_update()

    return jsonify(code=RET.OK)

