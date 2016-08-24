#!/usr/bin/python
#coding=utf-8

import sys
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入 
sys.setdefaultencoding('utf-8')

import os

import MySQLdb
import json
import hashlib
import time

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask import render_template
from werkzeug import secure_filename

from utils.mysql_python import MysqlPython
from utils.object2json import obj2json
from models.RetModel import RetModel

app = Flask(__name__, static_url_path = "/upload", static_folder = "upload")
app.config['UPLOAD_FOLDER'] = 'upload/'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'TXT', 'PDF', 'PNG', 'JPG', 'JPEG', 'GIF'])

dict_err_code = { 
    0 : "success" 
    , 1 : "Server support post only" 
    , 10 : "Upload failed" 
    , 1000 : "Unknow error"
}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def get_file_ext(filename):
    if ('.' in filename):
        return filename.rsplit('.', 1)[1]
    else:
        return ""
    
@app.route("/", methods=['POST', 'GET'])
def index():
    return "Server API for ThinkNews!"

@app.route('/api/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return obj2json(RetModel(2, dict_err_code[2], {}) )
      
    file = request.files['pic1']
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        savedFileName = hashlib.md5(filename).hexdigest() + "." + get_file_ext(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], savedFileName ) )
        return obj2json(RetModel(0, dict_err_code[0], {}) )
    else:
        return obj2json(RetModel(10, dict_err_code[10], {}) ) 
    
if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=8080)