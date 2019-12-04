# coding=utf-8
from flask import session,jsonify
from status_code import *

import functools
def is_login(view_fun):
    @functools.wraps(view_fun)
    def fun():
        if 'user_id' in session:
            return view_fun()
        else:
            return jsonify(code=RET.LOGINERR)
    return fun
