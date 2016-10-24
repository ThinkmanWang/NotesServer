
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

from utils.user_db_utils import *  
from utils.alarm_db_utils import *
from utils.note_db_utils import *
from models.Note import Note
from models.Alarm import Alarm
from error_code import *

from flask import Blueprint
alarm_api = Blueprint('alarm_api', __name__)

#For alarm
@alarm_api.route("/api/get_alarm_list", methods=['POST', 'GET'])
def get_alarm_list():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form.get('uid', None) is None or request.form.get('token', None) is None):
        return obj2json(RetModel(21, dict_err_code[21]))     
    
    if (False == verify_user_token(request.form.get('uid', ''), request.form.get('token', ''))):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    
    
    lstAlarm = select_alarm_list(request.form['uid'])
    szRet = obj2json(RetModel(0, dict_err_code[0], lstAlarm) )

    return szRet    

@alarm_api.route("/api/get_alarm", methods=['POST', 'GET'])
def get_alarm():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form.get('uid', None) is None or request.form.get('token', None) is None):
        return obj2json(RetModel(21, dict_err_code[21]))     
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    
    
    szRet = obj2json(RetModel(1024, dict_err_code[1024], {}) )
    return szRet

@alarm_api.route("/api/add_alarm", methods=['POST', 'GET'])
def add_alarm():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form.get('uid', None) is None or request.form.get('token', None) is None):
        return obj2json(RetModel(21, dict_err_code[21]))     
    
    if (request.form.get('id', None) is None):
        return obj2json(RetModel(51, dict_err_code[51]))     
    
    if (request.form.get('note_id', None) is None):
        return obj2json(RetModel(52, dict_err_code[52]))       
    
    if (request.form.get('date', None) is None):
        return obj2json(RetModel(53, dict_err_code[53]))   
    
    if (request.form.get('update_date', None) is None):
        return obj2json(RetModel(54, dict_err_code[54]))          
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )      
    
    if (False == if_noteid_exists(request.form['note_id'])):
        return obj2json(RetModel(41, dict_err_code[41]))  
    
    if (True == insert_alarm(request.form['uid'], request.form['id'], request.form['note_id'], request.form['date'], request.form['update_date'])):
        szRet = obj2json(RetModel(0, dict_err_code[0], {}) )
    else:
        szRet = obj2json(RetModel(1000, dict_err_code[1000], {}) )

    return szRet    

@alarm_api.route("/api/update_alarm", methods=['POST', 'GET'])
def update_alarm():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )  
    
    if (request.form.get('uid', None) is None or request.form.get('token', None) is None):
        return obj2json(RetModel(21, dict_err_code[21]))  
    
    if (request.form.get('id', None) is None):
        return obj2json(RetModel(51, dict_err_code[51]))     
    
    if (request.form.get('note_id', None) is None):
        return obj2json(RetModel(52, dict_err_code[52]))       

    if (request.form.get('date', None) is None):
        return obj2json(RetModel(53, dict_err_code[53]))    
    
    if (request.form.get('update_date', None) is None):
        return obj2json(RetModel(54, dict_err_code[54]))        
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    
    
    if (False == if_noteid_exists(request.form['note_id'])):
        return obj2json(RetModel(41, dict_err_code[41]))      
    
    szRet = ''
    if (False == if_alarm_exists(request.form['id'])):
        szRet = obj2json(RetModel(51, dict_err_code[51], {}) )
    else:
        if (True == update_alarm_info(request.form['uid'], request.form['id'], request.form['note_id'], request.form['date'], request.form['update_date'])):
            szRet = obj2json(RetModel(0, dict_err_code[0], {}) )
        else:
            szRet = obj2json(RetModel(1000, dict_err_code[1000], {}) )  
            
    return szRet

@alarm_api.route("/api/delete_alarm", methods=['POST', 'GET'])
def delete_alarm():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form.get('uid', None) is None or request.form.get('token', None) is None):
        return obj2json(RetModel(21, dict_err_code[21]))    
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    
    
    if (request.form.get('id', None) is None):
        return obj2json(RetModel(51, dict_err_code[51]))    
    
    if (False == if_alarm_exists(request.form['id'])):
        return obj2json(RetModel(51, dict_err_code[51], {}))

    if (remove_alarm(request.form['id'])):
        return obj2json(RetModel(0, dict_err_code[0], {}) )
    else:
        return obj2json(RetModel(1000, dict_err_code[1000], {}) )
