
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
from user import *
from models.Customer import Customer
from utils.customer_db_utils import *
from error_code import *

from utils.mysql_python import MysqlPython
from utils.object2json import obj2json

from flask import Blueprint
customer_api = Blueprint('customer_api', __name__)

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'models'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

#For Customer
@customer_api.route("/api/get_customer_list", methods=['POST', 'GET'])
def get_customer_list():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form.get('uid', None) is None or request.form.get('token', None) is None):
        return obj2json(RetModel(21, dict_err_code[21]))     
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    
    
    lstCustomer = select_customer_list(request.form['uid'], request.form.get('type', '0'))
    szRet = obj2json(RetModel(0, dict_err_code[0], lstCustomer) )

    return szRet

@customer_api.route("/api/get_customer", methods=['POST', 'GET'])
def get_customer():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form.get('uid', None) is None or request.form.get('token', None) is None):
        return obj2json(RetModel(21, dict_err_code[21]))   
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )  
    
    if (request.form.get('id', None) is None):
        return obj2json(RetModel(31, dict_err_code[31], {}) )  
    
    customer = select_customer(request.form['uid'], request.form['id'])
    szRet = ""
    if (customer is None):
        szRet = obj2json(RetModel(30, dict_err_code[30], {}) )
    else:
        szRet = obj2json(RetModel(0, dict_err_code[0], customer) )
        
    return szRet

@customer_api.route("/api/add_customer", methods=['POST', 'GET'])
def add_customer():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form.get('uid', None) is None or request.form.get('token', None) is None):
        return obj2json(RetModel(21, dict_err_code[21]))   
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    
    
    if (request.form.get('id', None) is None):
        return obj2json(RetModel(31, dict_err_code[31], {}) )   
    
    if (request.form.get('name', None) is None):
        return obj2json(RetModel(32, dict_err_code[32], {}) )      
    
    if (request.form.get('address', None) is None):
        return obj2json(RetModel(33, dict_err_code[33], {}) )     
    
    if (request.form.get('longitude', None) is None):
        return obj2json(RetModel(34, dict_err_code[34], {}) ) 
    
    if (request.form.get('latitude', None) is None):
        return obj2json(RetModel(35, dict_err_code[35], {}) )     
    
    customer = Customer()
    customer.id = request.form['id']
    customer.uid = request.form['uid']
    customer.name = request.form['name']
    customer.group_name = request.form.get('group_name', '')
    customer.spell = request.form.get('spell', '')
    customer.address = request.form['address']
    customer.longitude = request.form['longitude']
    customer.latitude = request.form['latitude']
    customer.boss = request.form.get('boss', '')
    customer.phone = request.form.get('phone', '')
    customer.email = request.form.get('email', '')
    customer.description = request.form.get('description', '')
    customer.update_date = request.form.get('update_date', int(time.time()))
    
    if (True == insert_customer(request.form['uid'], customer)):
        szRet = obj2json(RetModel(0, dict_err_code[0], {}) )
    else:
        szRet = obj2json(RetModel(1000, dict_err_code[1000], {}) )
    
    return szRet

@customer_api.route("/api/update_customer", methods=['POST', 'GET'])
def update_customer():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form.get('uid', None) is None or request.form.get('token', None) is None):
        return obj2json(RetModel(21, dict_err_code[21]))     
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    
    
    if (request.form.get('id', None) is None):
        return obj2json(RetModel(31, dict_err_code[31], {}) )   
    
    if (request.form.get('name', None) is None):
        return obj2json(RetModel(32, dict_err_code[32], {}) )      
    
    if (request.form.get('address', None) is None):
        return obj2json(RetModel(33, dict_err_code[33], {}) )     
    
    if (request.form.get('longitude', None) is None):
        return obj2json(RetModel(34, dict_err_code[34], {}) ) 
    
    if (request.form.get('latitude', None) is None):
        return obj2json(RetModel(35, dict_err_code[35], {}) )       

    customer = Customer()
    customer.id = request.form['id']
    customer.uid = request.form['uid']
    customer.name = request.form['name']
    customer.group_name = request.form.get('group_name', '')
    customer.spell = request.form.get('spell', '')
    customer.address = request.form['address']
    customer.longitude = request.form['longitude']
    customer.latitude = request.form['latitude']
    customer.boss = request.form.get('boss', '')
    customer.phone = request.form.get('phone', '')
    customer.email = request.form.get('email', '')
    customer.description = request.form.get('description', '')
    customer.update_date = request.form.get('update_date', int(time.time()))
    
    szRet = ''
    if (False == if_customer_exists(customer)):
        szRet = obj2json(RetModel(30, dict_err_code[30], {}) )
    else:
        if (True == update_customer_info(request.form['uid'], customer)):
            szRet = obj2json(RetModel(0, dict_err_code[0], {}) )
        else:
            szRet = obj2json(RetModel(1000, dict_err_code[1000], {}) )
    
    return szRet    

@customer_api.route("/api/delete_customer", methods=['POST', 'GET'])
def delete_customer():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form.get('uid', None) is None or request.form.get('token', None) is None):
        return obj2json(RetModel(21, dict_err_code[21]))      
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    
    
    szRet = obj2json(RetModel(1024, dict_err_code[1024], {}) )
    return szRet


#get all customer of my members
@customer_api.route("/api/get_customer_list_of_user", methods=['POST', 'GET'])
def get_customer_list_of_user():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form.get('uid', None) is None or request.form.get('token', None) is None):
        return obj2json(RetModel(21, dict_err_code[21]))     
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    
    
    return obj2json(RetModel(1024, dict_err_code[1024], {}) )

@customer_api.route("/api/job_transfer", methods=['POST', 'GET'])
def job_transfer():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form.get('uid', None) is None or request.form.get('token', None) is None):
        return obj2json(RetModel(21, dict_err_code[21]))     
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    
    
    return obj2json(RetModel(1024, dict_err_code[1024], {}) )
