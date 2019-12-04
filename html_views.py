# coding=utf-8
from flask import Blueprint,current_app
html_blueprint=Blueprint('html',__name__)

@html_blueprint.route('/<html:filename>')
def html(filename):
    if not filename:
        filename='index.html'
    filename='html/'+filename
    html=current_app.send_static_file(filename)
    return html
