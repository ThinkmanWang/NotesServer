#!/usr/bin/python
#coding=utf-8

import sys
from imp import reload

if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding("utf-8")

import os

import MySQLdb
import json
import hashlib
import time
import uuid

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask import render_template
from werkzeug import secure_filename

from utils.mysql_python import MysqlPython
from utils.object2json import obj2json

from models.RetModel import RetModel

app = Flask(__name__, static_url_path = "/upload", static_folder = "upload")
app.config['UPLOAD_FOLDER'] = 'upload/'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'TXT', 'PDF', 'PNG', 'JPG', 'JPEG', 'GIF'])

from api.error_code import *
from api.upload import *
from api.users import *
from api.alarm import *
from api.customer import *
from api.notes import *
from api.groups import *

app.register_blueprint(alarm_api)
app.register_blueprint(customer_api)
app.register_blueprint(notes_api)
app.register_blueprint(upload_api)
app.register_blueprint(user_api)
app.register_blueprint(groups_api)


@app.route("/", methods=['POST', 'GET'])
def index():
    return "Server API for Notes!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
