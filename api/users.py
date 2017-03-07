
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
from utils.customer_db_utils import *

from models.RetModel import RetModel

import uuid

from utils.user_db_utils import *  
from models.User import User
from error_code import *

from flask import Blueprint
user_api = Blueprint('user_api', __name__)
import pdb
import thread

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


@user_api.route("/api/set_leader", methods=['POST', 'GET'])
def set_leader():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form.get('uid', None) is None or request.form.get('token', None) is None):
        return obj2json(RetModel(21, dict_err_code[21]))     
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    
	
    if (request.form.get('leader_id', None) is None):
        return obj2json(RetModel(70, dict_err_code[70], {}) )    
	
    if (False == db_is_user_exists(request.form["leader_id"])):
        return obj2json(RetModel(71, dict_err_code[71], {}) )

    if request.form["uid"] == request.form["leader_id"]:
        return obj2json(RetModel(75, dict_err_code[75], {}))

    #check if my member
    lstUser = db_get_member_list(request.form['uid'])
    for user in lstUser:
        if request.form["uid"] == str(user["leader_uid"]):
            return obj2json(RetModel(74, dict_err_code[74], {}) )
	
    if (False == db_set_user_leader(request.form['uid'], request.form["leader_id"])):
        return obj2json(RetModel(1000, dict_err_code[1000], {}) ) 

    return obj2json(RetModel(0, dict_err_code[0], {}) )    

@user_api.route("/api/query_users", methods=['POST', 'GET'])
def query_users():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form.get('uid', None) is None or request.form.get('token', None) is None):
        return obj2json(RetModel(21, dict_err_code[21]))     

    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    
    
    lstUser = db_query_users()
    return obj2json(RetModel(0, dict_err_code[0], lstUser) )

@user_api.route("/api/update_user_info", methods=['POST', 'GET'])
def update_user_info():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form.get('uid', None) is None or request.form.get('token', None) is None):
        return obj2json(RetModel(21, dict_err_code[21]))     
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    

    if (request.form.get('avatar', None) is None):
        return obj2json(RetModel(72, dict_err_code[72]))     

    if (request.form.get('show_name', None) is None):
        return obj2json(RetModel(73, dict_err_code[73]))     

    if (db_update_user_info(request.form["uid"], request.form["avatar"], request.form["show_name"])):
        return obj2json(RetModel(0, dict_err_code[0], {}) )
    else:
        return obj2json(RetModel(1000, dict_err_code[1000], {}) )

@user_api.route("/api/get_user_profile", methods=['POST', 'GET'])
def get_user_profile():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form.get('uid', None) is None or request.form.get('token', None) is None):
        return obj2json(RetModel(21, dict_err_code[21]))     
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    
    
    if (request.form.get('member_uid', None) is not None):
        #get profile for my member
        userProfile = db_query_user_profile(request.form['member_uid'])
        if (userProfile is None):
            return obj2json(RetModel(1000, dict_err_code[1000], {}) ) 
        else:
            return obj2json(RetModel(0, dict_err_code[0], userProfile) )

    else:
        #get profile for myself
        userProfile = db_query_user_profile(request.form['uid'])
        if (userProfile is None):
            return obj2json(RetModel(1000, dict_err_code[1000], {}) ) 
        else:
            return obj2json(RetModel(0, dict_err_code[0], userProfile) )

#get my member list
@user_api.route("/api/get_member_list", methods=['POST', 'GET'])
def get_member_list():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form.get('uid', None) is None or request.form.get('token', None) is None):
        return obj2json(RetModel(21, dict_err_code[21]))     
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    

    lstUser = db_get_all_member_list(request.form['uid'])
    return obj2json(RetModel(0, dict_err_code[0], lstUser) )


@user_api.route("/api/get_user_customer", methods=['POST', 'GET'])
def get_user_customer():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form.get('uid', None) is None or request.form.get('token', None) is None):
        return obj2json(RetModel(21, dict_err_code[21]))     
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    
    
    lstRet = []
    if (request.form.get('member_uid', None) is not None):
        #get profile for my member
        lstRet = select_customer_list(request.form['member_uid'], '0')

    else:
        #get profile for myself
        lstRet = select_customer_list(request.form['uid'], '0')
    
    return obj2json(RetModel(0, dict_err_code[0], lstRet) )

@user_api.route("/api/job_transfer", methods=['POST', 'GET'])
def job_transfer():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}))

    if (request.form.get('uid', None) is None or request.form.get('token', None) is None):
        return obj2json(RetModel(21, dict_err_code[21]))

    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )

    if (request.form.get('uid_src', None) is None):
        return obj2json(RetModel(80, dict_err_code[80], {}))

    if (request.form.get('uid_dst', None) is None):
        return obj2json(RetModel(81, dict_err_code[81], {}))

    #thread.start_new_thread(db_transfer_user_data, (request.form["uid_src"], request.form["uid_dst"]))
    db_transfer_user_data(request.form["uid_src"], request.form["uid_dst"])
    return obj2json(RetModel(0, dict_err_code[0], {}) )

@user_api.route("/api/get_password", methods=['POST', 'GET'])
def get_password():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}))

    if (request.form.get('phone', None) is None):
        return obj2json(RetModel(22, dict_err_code[22], {}))

    if (db_send_password(request.form['phone']) == True):
        return obj2json(RetModel(0, dict_err_code[0], {}))
    else:
        return obj2json(RetModel(1000, dict_err_code[1000], {}))