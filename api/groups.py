
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
from models.Group import Group

from utils.user_db_utils import *  
from utils.groups_db_utils import *
from error_code import *

from flask import Blueprint
groups_api = Blueprint('groups_api', __name__)

@groups_api.route("/api/add_group", methods=['POST', 'GET'])
def add_group():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form.get('uid', None) is None or request.form.get('token', None) is None):
        return obj2json(RetModel(21, dict_err_code[21]))     

    if (False == verify_user_token(request.form.get('uid', ''), request.form.get('token', ''))):
        return obj2json(RetModel(21, dict_err_code[21], {}) )        

    if (request.form.get('group_name', None) is None or len(request.form.get('group_name', '')) <= 0):
        return obj2json(RetModel(60, dict_err_code[60], {}) ) 
    
    if (request.form.get('update_date', None) is None or len(request.form.get('update_date', '')) <= 0):
            return obj2json(RetModel(61, dict_err_code[61], {}) )     
    
    if (insert_group(request.form['uid'], request.form['group_name'], request.form['update_date'])):
        return obj2json(RetModel(0, dict_err_code[0], {}) ) 
    else:
        return obj2json(RetModel(1024, dict_err_code[1024], {}) )


@groups_api.route("/api/get_group_list", methods=['POST', 'GET'])
def get_group_list():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form.get('uid', None) is None or request.form.get('token', None) is None):
        return obj2json(RetModel(21, dict_err_code[21]))     

    if (False == verify_user_token(request.form.get('uid', ''), request.form.get('token', ''))):
        return obj2json(RetModel(21, dict_err_code[21], {}) )   
    
    lstGroup = select_group_list(request.form['uid'])
    szRet = obj2json(RetModel(0, dict_err_code[0], lstGroup) )

    return szRet    
  

@groups_api.route("/api/delete_group", methods=['POST', 'GET'])
def delete_group():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form.get('uid', None) is None or request.form.get('token', None) is None):
        return obj2json(RetModel(21, dict_err_code[21]))     

    if (False == verify_user_token(request.form.get('uid', ''), request.form.get('token', ''))):
        return obj2json(RetModel(21, dict_err_code[21], {}) )        

    if (request.form.get('group_name', None) is None or len(request.form.get('group_name', '')) <= 0):
        return obj2json(RetModel(60, dict_err_code[60], {}) ) 
    
    if (remove_group(request.form['uid'], request.form['group_name'])):
        return obj2json(RetModel(0, dict_err_code[0], {}) ) 
    else:
        return obj2json(RetModel(1000, dict_err_code[1000], {}) )
