
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
from models.Note import Note
from error_code import *

from flask import Blueprint
notes_api = Blueprint('notes_api', __name__)

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'models'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

#For notes
@notes_api.route("/api/get_notes_id_list", methods=['POST', 'GET'])
def get_notes_id_list():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )   
    
    if (request.form.get('uid', None) is None or request.form.get('token', None) is None):
        return obj2json(RetModel(21, dict_err_code[21]))    
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    
    
    lstNoteId = select_note_id_list(request.form['uid'])
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

@notes_api.route("/api/update_note", methods=['POST', 'GET'])
def update_note():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form.get('uid', None) is None or request.form.get('token', None) is None):
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

@notes_api.route("/api/delete_note", methods=['POST', 'GET'])
def delete_note():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    if (request.form.get('uid', None) is None or request.form.get('token', None) is None):
        return obj2json(RetModel(21, dict_err_code[21]))        
    
    if (False == verify_user_token(request.form['uid'], request.form['token'])):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    
    
    szRet = obj2json(RetModel(1024, dict_err_code[1024], {}) )
    return szRet
