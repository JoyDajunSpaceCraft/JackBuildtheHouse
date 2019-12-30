# coding=utf-8
# 设置后端传参 帮助验证Ajax是否success
class MESSAGE:
    OK = "0"
    DBERR = "4001"
    NODATA = "4002"
    DATAEXIST = "4003"
    DATAERR = "4004"
    SESSIONERR = "4101"
    LOGINERR = "4102"
    PARAMERR = "4103"
    USERERR = "4104"
    ROLEERR = "4105"
    PWDERR = "4106"
    REQERR = "4201"
    IPERR = "4202"
    THIRDERR = "4301"
    IOERR = "4302"
    SERVERERR = "4500"
    UNKOWNERR = "4501"

ret_map = {
    MESSAGE.OK: u"成功",
    MESSAGE.DBERR: u"数据库错误",
    MESSAGE.NODATA: u"无数据",
    MESSAGE.DATAEXIST: u"数据已存在",
    MESSAGE.DATAERR: u"数据错误",
    MESSAGE.SESSIONERR: u"用户未登录",
    MESSAGE.LOGINERR: u"用户登录失败",
    MESSAGE.PARAMERR: u"参数错误",
    MESSAGE.USERERR: u"用户不存在或未激活",
    MESSAGE.ROLEERR: u"用户身份错误",
    MESSAGE.PWDERR: u"密码错误",
    MESSAGE.REQERR: u"非法请求或请求次数受限",
    MESSAGE.IPERR: u"IP受限",
    MESSAGE.THIRDERR: u"第三方系统错误",
    MESSAGE.IOERR: u"文件读写错误",
    MESSAGE.SERVERERR: u"内部错误",
    MESSAGE.UNKOWNERR: u"未知错误",
}
