# # coding=utf-8
# from qiniu import Auth,put_data
# import logging
# from flask import jsonify
# from status_code import RET
#
# def put_qiniu(f1):
#     access_key = 'H999S3riCJGPiJOity1GsyWufw3IyoMB6goojo5e'
#     secret_key = 'uOZfRdFtljIw7b8jr6iTG-cC6wY_-N19466PXUAb'
#     # 空间名称
#     bucket_name = 'itcast20171104'
#     try:
#         # 构建鉴权对象
#         q = Auth(access_key, secret_key)
#         # 生成上传 Token
#         token = q.upload_token(bucket_name)
#         # 上传文件数据，ret是字典，键为hash、key，值为新文件名，info是response对象
#         ret, info = put_data(token, None, f1.read())
#         return ret.get('key')
#     except:
#         logging.ERROR(u'访问七牛云出错')
#         return jsonify(code=RET.SERVERERR)
