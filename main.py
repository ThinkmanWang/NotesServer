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

from utils.user_db_utils import *  
from utils.customer_db_utils import *
from utils.note_db_utils import *
from utils.alarm_db_utils import *

from models.User import User
from models.Note import Note
from models.Alarm import Alarm
from models.Customer import Customer
from models.RetModel import RetModel

from api.error_code import *

app = Flask(__name__, static_url_path = "/upload", static_folder = "upload")


@app.route("/", methods=['POST', 'GET'])
def index():
    return "Server API for Notes!"

@app.route("/api/login", methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )
    if (request.form['user_name'] is None or request.form['password'] is None or request.form["verify_code"] is None):
        return obj2json(RetModel(20, dict_err_code[20]))    
    
    user = user_login(request.form['user_name'], request.form['password'], request.form["verify_code"])
    
    szRet = ""
    if (user == None):
        szRet = obj2json(RetModel(1, "user_name or password is incorrect", {}) )
    else:
        retModel = RetModel(0, "success", user)
        szRet = obj2json(retModel)
            
    return szRet    

#For Customer
@app.route("/api/get_customer_list", methods=['POST', 'GET'])
def get_customer_list():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form['uid'] is None or request.form['token'] is None):
        return obj2json(RetModel(21, dict_err_code[21]))     
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    
    
    lstCustomer = select_customer_list(request.form['uid'])
    szRet = obj2json(RetModel(0, dict_err_code[0], lstCustomer) )

    return szRet

@app.route("/api/get_customer", methods=['POST', 'GET'])
def get_customer():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form['uid'] is None or request.form['token'] is None):
        return obj2json(RetModel(21, dict_err_code[21]))    
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )  
    
    if (request.form['id'] is None):
        return obj2json(RetModel(31, dict_err_code[31], {}) )  
    
    customer = select_customer(request.form['uid'], request.form['id'])
    szRet = ""
    if (customer is None):
        szRet = obj2json(RetModel(30, dict_err_code[30], {}) )
    else:
        szRet = obj2json(RetModel(0, dict_err_code[0], customer) )
        
    return szRet

@app.route("/api/add_customer", methods=['POST', 'GET'])
def add_customer():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form['uid'] is None or request.form['token'] is None):
        return obj2json(RetModel(21, dict_err_code[21]))     
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    
    
    customer = Customer()
    customer.id = request.form['id']
    customer.uid = request.form['uid']
    customer.name = request.form['name']
    customer.group_name = request.form['group_name']
    customer.spell = request.form['spell']
    customer.address = request.form['address']
    customer.longitude = request.form['longitude']
    customer.latitude = request.form['latitude']
    customer.boss = request.form['boss']
    customer.phone = request.form['phone']
    customer.email = request.form['email']
    customer.description = request.form['description']
    customer.update_date = request.form['update_date']
    
    if (True == insert_customer(request.form['uid'], customer)):
        szRet = obj2json(RetModel(0, dict_err_code[0], {}) )
    else:
        szRet = obj2json(RetModel(1000, dict_err_code[1000], {}) )
    
    return szRet

@app.route("/api/update_customer", methods=['POST', 'GET'])
def update_customer():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form['uid'] is None or request.form['token'] is None):
        return obj2json(RetModel(21, dict_err_code[21]))     
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    

    customer = Customer()
    customer.id = request.form['id']
    customer.uid = request.form['uid']
    customer.name = request.form['name']
    customer.group_name = request.form['group_name']
    customer.spell = request.form['spell']
    customer.address = request.form['address']
    customer.longitude = request.form['longitude']
    customer.latitude = request.form['latitude']
    customer.boss = request.form['boss']
    customer.phone = request.form['phone']
    customer.email = request.form['email']
    customer.description = request.form['description']
    customer.update_date = request.form['update_date']
    
    szRet = ''
    if (False == if_customer_exists(customer)):
        szRet = obj2json(RetModel(30, dict_err_code[30], {}) )
    else:
        if (True == update_customer_info(request.form['uid'], customer)):
            szRet = obj2json(RetModel(0, dict_err_code[0], {}) )
        else:
            szRet = obj2json(RetModel(1000, dict_err_code[1000], {}) )
    
    return szRet    

@app.route("/api/delete_customer", methods=['POST', 'GET'])
def delete_customer():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form['uid'] is None or request.form['token'] is None):
        return obj2json(RetModel(21, dict_err_code[21]))     
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    
    
    szRet = obj2json(RetModel(1024, dict_err_code[1024], {}) )
    return szRet

#For notes
@app.route("/api/get_notes_id_list", methods=['POST', 'GET'])
def get_notes_id_list():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )   
    
    if (request.form['uid'] is None or request.form['token'] is None):
        return obj2json(RetModel(21, dict_err_code[21]))     
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    
    
    lstNoteId = select_note_id_list(request.form['uid'])
    szRet = obj2json(RetModel(0, dict_err_code[0], lstNoteId) )

    return szRet    

@app.route("/api/get_note", methods=['POST', 'GET'])
def get_note():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form['uid'] is None or request.form['token'] is None):
        return obj2json(RetModel(21, dict_err_code[21]))     
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    
    
    if (request.form['id'] is None):
        return obj2json(RetModel(41, dict_err_code[41], {}) )      
    
    note = select_note(request.form['uid'], request.form['id'])
    szRet = ""
    if (note is None):
        szRet = obj2json(RetModel(40, dict_err_code[40], {}) )
    else:
        szRet = obj2json(RetModel(0, dict_err_code[0], note) )
        
    return szRet

@app.route("/api/add_note", methods=['POST', 'GET'])
def add_note():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form['uid'] is None or request.form['token'] is None):
        return obj2json(RetModel(21, dict_err_code[21]))     
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    
    
    note = Note()
    note.id = request.form['id']
    note.uid = request.form['uid']
    note.date = request.form['date']
    note.update_date = request.form['update_date']
    note.customer_id = request.form['customer_id']
    note.address = request.form['address']
    note.longitude = request.form['longitude']
    note.latitude = request.form['latitude']
    note.note = request.form['note']
    note.thumbnail = request.form['thumbnail']
    note.pic = request.form['pic']
    
    if (True == insert_note(request.form['uid'], note)):
        szRet = obj2json(RetModel(0, dict_err_code[0], {}) )
    else:
        szRet = obj2json(RetModel(1000, dict_err_code[1000], {}) )

    return szRet    

@app.route("/api/update_note", methods=['POST', 'GET'])
def update_note():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form['uid'] is None or request.form['token'] is None):
        return obj2json(RetModel(21, dict_err_code[21]))     
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )   
    
    note = Note()
    note.id = request.form['id']
    note.uid = request.form['uid']
    note.date = request.form['date']
    note.update_date = request.form['update_date']
    note.customer_id = request.form['customer_id']
    note.address = request.form['address']
    note.longitude = request.form['longitude']
    note.latitude = request.form['latitude']
    note.note = request.form['note']
    note.thumbnail = request.form['thumbnail']
    note.pic = request.form['pic']   
    
    szRet = ''
    if (False == if_note_exists(note)):
        szRet = obj2json(RetModel(40, dict_err_code[40], {}) )
    else:
        if (True == update_note_info(request.form['uid'], note)):
            szRet = obj2json(RetModel(0, dict_err_code[0], {}) )
        else:
            szRet = obj2json(RetModel(1000, dict_err_code[1000], {}) )
    
    return szRet    

@app.route("/api/delete_note", methods=['POST', 'GET'])
def delete_note():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form['uid'] is None or request.form['token'] is None):
        return obj2json(RetModel(21, dict_err_code[21]))     
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    
    
    szRet = obj2json(RetModel(1024, dict_err_code[1024], {}) )
    return szRet

#For alarm
@app.route("/api/get_alarm_list", methods=['POST', 'GET'])
def get_alarm_list():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form['uid'] is None or request.form['token'] is None):
        return obj2json(RetModel(21, dict_err_code[21]))     
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    
    
    lstAlarm = select_alarm_list(request.form['uid'])
    szRet = obj2json(RetModel(0, dict_err_code[0], lstAlarm) )

    return szRet    

@app.route("/api/get_alarm", methods=['POST', 'GET'])
def get_alarm():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form['uid'] is None or request.form['token'] is None):
        return obj2json(RetModel(21, dict_err_code[21]))     
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    
    
    szRet = obj2json(RetModel(1024, dict_err_code[1024], {}) )
    return szRet

@app.route("/api/add_alarm", methods=['POST', 'GET'])
def add_alarm():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form['uid'] is None or request.form['token'] is None):
        return obj2json(RetModel(21, dict_err_code[21]))     
    
    if (request.form['id'] is None):
        return obj2json(RetModel(51, dict_err_code[51]))     
    
    if (request.form['note_id'] is None):
        return obj2json(RetModel(52, dict_err_code[52]))       
    
    if (request.form['date'] is None):
        return obj2json(RetModel(53, dict_err_code[53]))   
    
    if (request.form['update_date'] is None):
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

@app.route("/api/update_alarm", methods=['POST', 'GET'])
def update_alarm():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )  
    
    if (request.form['uid'] is None or request.form['token'] is None):
        return obj2json(RetModel(21, dict_err_code[21]))  
    
    if (request.form['id'] is None):
        return obj2json(RetModel(51, dict_err_code[51]))     
    
    if (request.form['note_id'] is None):
        return obj2json(RetModel(52, dict_err_code[52]))       

    if (request.form['date'] is None):
        return obj2json(RetModel(53, dict_err_code[53]))    
    
    if (request.form['update_date'] is None):
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

@app.route("/api/delete_alarm", methods=['POST', 'GET'])
def delete_alarm():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form['uid'] is None or request.form['token'] is None):
        return obj2json(RetModel(21, dict_err_code[21]))    
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    
    
    if (request.form['id'] is None):
        return obj2json(RetModel(51, dict_err_code[51]))    
    
    if (False == if_alarm_exists(request.form['id'])):
        return obj2json(RetModel(51, dict_err_code[51], {}))

    if (remove_alarm(request.form['id'])):
        return obj2json(RetModel(0, dict_err_code[0], {}) )
    else:
        return obj2json(RetModel(1000, dict_err_code[1000], {}) )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
