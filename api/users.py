
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'models'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from imp import reload


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

import uuid

from utils.user_db_utils import *  
from models.User import User
from error_code import *

from flask import Blueprint
user_api = Blueprint('user_api', __name__)

@user_api.route("/api/login", methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )
    if (request.form.get('user_name', None) is None or request.form.get('password', None) is None or request.form.get("verify_code", None) is None):
        return obj2json(RetModel(20, dict_err_code[20]))    
    
    user = user_login(request.form['user_name'], request.form['password'], request.form["verify_code"])
    
    szRet = ""
    if (user == None):
        szRet = obj2json(RetModel(1, "user_name or password is incorrect", {}) )
    else:
        retModel = RetModel(0, "success", user)
        szRet = obj2json(retModel)
            
    return szRet 