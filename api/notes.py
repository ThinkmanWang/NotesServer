
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
from utils.note_db_utils import *
from error_code import *

from flask import Blueprint
notes_api = Blueprint('notes_api', __name__)

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'models'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

#For notes

@notes_api.route("/api/get_notes_list", methods=['POST', 'GET'])
def get_notes_list():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )   
    
    if (request.form.get('uid', None) is None or request.form.get('token', None) is None):
        return obj2json(RetModel(21, dict_err_code[21]))    
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    

    if (request.form.get('limit', None) is None or request.form.get('offset', None) is None):
        return obj2json(RetModel(46, dict_err_code[46], {}) )    

    if (False == request.form['limit'].isdigit() or False == request.form['offset'].isdigit()):
        return obj2json(RetModel(46, dict_err_code[46], {}) )    


    if (request.form.get('member_uid', None) is not None):
        lstNoteId = select_note_list(request.form['member_uid'], int(request.form['limit']), int(request.form['offset']), request.form.get('type', '0'))
        szRet = obj2json(RetModel(0, dict_err_code[0], lstNoteId) )

        return szRet    

    else:
        lstNoteId = select_note_list(request.form['uid'], request.form['limit'], request.form['offset'], request.form.get('type', '0'))
        szRet = obj2json(RetModel(0, dict_err_code[0], lstNoteId) )

        return szRet    

@notes_api.route("/api/get_note", methods=['POST', 'GET'])
def get_note():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form.get('uid', None) is None or request.form.get('token', None) is None):
        return obj2json(RetModel(21, dict_err_code[21]))    
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    
    
    if (request.form.get('id', None) is None):
        return obj2json(RetModel(41, dict_err_code[41], {}) )      
    
    note = select_note(request.form['uid'], request.form['id'])
    szRet = ""
    if (note is None):
        szRet = obj2json(RetModel(40, dict_err_code[40], {}) )
    else:
        szRet = obj2json(RetModel(0, dict_err_code[0], note) )
        
    return szRet

@notes_api.route("/api/add_note", methods=['POST', 'GET'])
def add_note():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form.get('uid', None) is None or request.form.get('token', None) is None):
        return obj2json(RetModel(21, dict_err_code[21]))      
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    
    
    if (request.form.get('id', None) is None):
        return obj2json(RetModel(41, dict_err_code[41], {}) )          
    
    if (request.form.get('date', None) is None):
        return obj2json(RetModel(42, dict_err_code[42], {}) )     
    
    if (request.form.get('customer_id', None) is None):
        return obj2json(RetModel(31, dict_err_code[31], {}) )     
    
    if (request.form.get('address', None) is None):
        return obj2json(RetModel(43, dict_err_code[43], {}) )    
    
    if (request.form.get('longitude', None) is None):
        return obj2json(RetModel(44, dict_err_code[44], {}) )      
    
    if (request.form.get('latitude', None) is None):
        return obj2json(RetModel(45, dict_err_code[45], {}) )       
    
    if (request.form.get('note', None) is None):
        return obj2json(RetModel(40, dict_err_code[40], {}) )        
    
    note = {}
    note["id"] = request.form['id']
    note["uid"] = request.form['uid']
    note["date"] = request.form['date']
    note["update_date"] = request.form.get('update_date', int(time.time()))
    note["customer_id"] = request.form['customer_id']
    note["address"] = request.form['address']
    note["longitude"] = request.form['longitude']
    note["latitude"] = request.form['latitude']
    note["note"] = request.form['note']
    note["thumbnail"] = request.form.get('thumbnail', '')
    note["pic"] = request.form.get('pic', '')
    
    if (True == insert_note(request.form['uid'], note)):
        szRet = obj2json(RetModel(0, dict_err_code[0], {}) )
    else:
        szRet = obj2json(RetModel(1000, dict_err_code[1000], {}) )

    return szRet    

@notes_api.route("/api/update_note", methods=['POST', 'GET'])
def update_note():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form.get('uid', None) is None or request.form.get('token', None) is None):
        return obj2json(RetModel(21, dict_err_code[21]))       
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )   
    
    if (request.form.get('id', None) is None):
        return obj2json(RetModel(41, dict_err_code[41], {}) )          
    
    if (request.form.get('date', None) is None):
        return obj2json(RetModel(42, dict_err_code[42], {}) )     
    
    if (request.form.get('customer_id', None) is None):
        return obj2json(RetModel(31, dict_err_code[31], {}) )     
    
    if (request.form.get('address', None) is None):
        return obj2json(RetModel(43, dict_err_code[43], {}) )    
    
    if (request.form.get('longitude', None) is None):
        return obj2json(RetModel(44, dict_err_code[44], {}) )      
    
    if (request.form.get('latitude', None) is None):
        return obj2json(RetModel(45, dict_err_code[45], {}) )       
    
    if (request.form.get('note', None) is None):
        return obj2json(RetModel(40, dict_err_code[40], {}) )         
    
    note = {}
    note["id"] = request.form['id']
    note["uid"] = request.form['uid']
    note["date"] = request.form['date']
    note["update_date"] = request.form.get('update_date', int(time.time()))
    note["customer_id"] = request.form['customer_id']
    note["address"] = request.form['address']
    note["longitude"] = request.form['longitude']
    note["latitude"] = request.form['latitude']
    note["note"] = request.form['note']
    note["thumbnail"] = request.form.get('thumbnail', '')
    note["pic"] = request.form.get('pic', '')
    
    szRet = ''
    if (False == if_note_exists(note)):
        szRet = obj2json(RetModel(40, dict_err_code[40], {}) )
    else:
        if (True == update_note_info(request.form['uid'], note)):
            szRet = obj2json(RetModel(0, dict_err_code[0], {}) )
        else:
            szRet = obj2json(RetModel(1000, dict_err_code[1000], {}) )
    
    return szRet    

@notes_api.route("/api/delete_note", methods=['POST', 'GET'])
def delete_note():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form.get('uid', None) is None or request.form.get('token', None) is None):
        return obj2json(RetModel(21, dict_err_code[21]))        
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    
    
    if (request.form.get('id', None) is None):
        return obj2json(RetModel(41, dict_err_code[41]))      
    
    if (remove_note(request.form['uid'], request.form['id'])):
        return obj2json(RetModel(0, dict_err_code[0], {}) ) 
    else:
        return obj2json(RetModel(1000, dict_err_code[1000], {}) )    
    

#for get all posts from my team & mine & public to me
@notes_api.route("/api/get_posts", methods=['POST', 'GET'])
def get_posts():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form.get('uid', None) is None or request.form.get('token', None) is None):
        return obj2json(RetModel(21, dict_err_code[21]))        
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    

    if (request.form.get('limit', None) is None or request.form.get('offset', None) is None):
        return obj2json(RetModel(46, dict_err_code[46], {}) )    

    if (False == request.form['limit'].isdigit() or False == request.form['offset'].isdigit()):
        return obj2json(RetModel(46, dict_err_code[46], {}) )    


    if (request.form.get('member_uid', None) is not None):
        lstNotes = select_note_for_member(request.form['member_uid'], request.form['limit'], request.form['offset'])
        szRet = obj2json(RetModel(0, dict_err_code[0], lstNotes) )
        return szRet    

    else:
        lstNotes = db_query_posts_public_to_me(request.form['uid'], request.form['limit'], request.form['offset'])
        szRet = obj2json(RetModel(0, dict_err_code[0], lstNotes) )
        return szRet    



#for repost notes
@notes_api.route("/api/repost", methods=['POST', 'GET'])
def repost():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form.get('uid', None) is None or request.form.get('token', None) is None):
        return obj2json(RetModel(21, dict_err_code[21]))        
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    

    if (request.form.get('id', None) is None):
        return obj2json(RetModel(41, dict_err_code[41], {}) )          
    
    if (request.form.get('address', None) is None):
        return obj2json(RetModel(43, dict_err_code[43], {}) )    
    
    if (request.form.get('longitude', None) is None):
        return obj2json(RetModel(44, dict_err_code[44], {}) )      
    
    if (request.form.get('latitude', None) is None):
        return obj2json(RetModel(45, dict_err_code[45], {}) )       
    
    if (request.form.get('customer_id', None) is None):
        return obj2json(RetModel(31, dict_err_code[31], {}) )     

    if (request.form.get('note', None) is None):
        return obj2json(RetModel(40, dict_err_code[40], {}) )        

    if (request.form.get('repost_from', None) is None):
        return obj2json(RetModel(47, dict_err_code[47], {}) )        
    
    note = {}
    note["id"] = request.form['id']
    note["uid"] = request.form['uid']
    note["date"] = request.form.get('date', int(time.time()))
    note["update_date"] = request.form.get('update_date', int(time.time()))
    note["customer_id"] = request.form['customer_id']
    note["address"] = request.form['address']
    note["longitude"] = request.form['longitude']
    note["latitude"] = request.form['latitude']
    note["note"] = request.form['note']
    note["thumbnail"] = request.form.get('thumbnail', '')
    note["pic"] = request.form.get('pic', '')
    note["repost_from"] = request.form.get('repost_from', '0')
    
    if (True == db_repost_note(request.form['uid'], note)):
        szRet = obj2json(RetModel(0, dict_err_code[0], {}) )
    else:
        szRet = obj2json(RetModel(1000, dict_err_code[1000], {}) )

    return szRet    
