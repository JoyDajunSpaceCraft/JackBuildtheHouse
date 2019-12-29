# coding=utf-8
from qiniu import Auth,put_data
import logging
from flask import jsonify
from status_code import RET

def put_qiniu(f1):
    access_key = 'HhKtntX3fbUdZ-53r3yVmsIu6OywiZ5ACBdf4jEf'
    secret_key = 'btL5jz1M4IO158TUjnmn8xLuq8px6HgDyNOJ2ydj'
    # 空间名称
    bucket_name = 'jackbuildthehouse'
    try:
        # 构建鉴权对象
        q = Auth(access_key, secret_key)
        # 生成上传 Token
        token = q.upload_token(bucket_name)
        # 上传文件数据，ret是字典，键为hash、key，值为新文件名，info是response对象
        ret, info = put_data(token, None, f1.read())
        return ret.get('key')
    except:
        logging.ERROR(u'访问七牛云出错')
        return jsonify(code=RET.SERVERERR)
