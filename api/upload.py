
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

from utils.user_db_utils import *  
from models.RetModel import RetModel
from error_code import *

from flask import Blueprint

upload_api = Blueprint('upload_api', __name__)
UPLOAD_FOLDER = 'upload/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'TXT', 'PDF', 'PNG', 'JPG', 'JPEG', 'GIF'])

def allowed_file(filename):
    #return ('.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']) or filename == "data"
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_file_ext(filename):
    if ('.' in filename):
        return "." + filename.rsplit('.', 1)[1]
    else:
        return ""
    
    
@upload_api.route('/api/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )

    dictFiles = {};

    if 'pic1' not in request.files:
        return obj2json(RetModel(11, dict_err_code[11], {}) )

    file1 = request.files['pic1']
    if file1 and allowed_file(file1.filename):
        filename = secure_filename(file1.filename)

        savedFileName = str(uuid.uuid4()) + get_file_ext(filename)
        file1.save(os.path.join(UPLOAD_FOLDER, savedFileName ) )
        dictFiles["pic1"] = savedFileName;

    else:
        return obj2json(RetModel(10, dict_err_code[10], {}) )

    if 'pic2' in request.files:
        file2= request.files['pic2']
        if file2 and allowed_file(file2.filename):
            filename = secure_filename(file2.filename)

            savedFileName = str(uuid.uuid4()) + get_file_ext(filename)
            file2.save(os.path.join(UPLOAD_FOLDER, savedFileName ) )
            dictFiles["pic2"] = savedFileName;

        else:
            return obj2json(RetModel(10, dict_err_code[10], {}) )

    if 'pic3' in request.files:
        file3= request.files['pic3']
        if file3 and allowed_file(file3.filename):
            filename = secure_filename(file3.filename)

            savedFileName = str(uuid.uuid4()) + get_file_ext(filename)
            file3.save(os.path.join(UPLOAD_FOLDER, savedFileName ) )
            dictFiles["pic3"] = savedFileName;

        else:
            return obj2json(RetModel(10, dict_err_code[10], {}) )

    if 'pic4' in request.files:
        file4= request.files['pic4']
        if file4 and allowed_file(file4.filename):
            filename = secure_filename(file4.filename)

            savedFileName = str(uuid.uuid4()) + get_file_ext(filename)
            file4.save(os.path.join(UPLOAD_FOLDER, savedFileName ) )
            dictFiles["pic4"] = savedFileName;

        else:
            return obj2json(RetModel(10, dict_err_code[10], {}) )

    if 'pic5' in request.files:
        file5= request.files['pic5']
        if file5 and allowed_file(file5.filename):
            filename = secure_filename(file5.filename)

            savedFileName = str(uuid.uuid4()) + get_file_ext(filename)
            file5.save(os.path.join(UPLOAD_FOLDER, savedFileName ) )
            dictFiles["pic5"] = savedFileName;

        else:
            return obj2json(RetModel(10, dict_err_code[10], {}) )

    if 'pic6' in request.files:
        file6= request.files['pic6']
        if file6 and allowed_file(file6.filename):
            filename = secure_filename(file6.filename)

            savedFileName = str(uuid.uuid4()) + get_file_ext(filename)
            file6.save(os.path.join(UPLOAD_FOLDER, savedFileName ) )
            dictFiles["pic6"] = savedFileName;

        else:
            return obj2json(RetModel(10, dict_err_code[10], {}) )

    if 'pic7' in request.files:
        file7= request.files['pic7']
        if file7 and allowed_file(file7.filename):
            filename = secure_filename(file7.filename)

            savedFileName = str(uuid.uuid4()) + get_file_ext(filename)
            file7.save(os.path.join(UPLOAD_FOLDER, savedFileName ) )
            dictFiles["pic7"] = savedFileName;

        else:
            return obj2json(RetModel(10, dict_err_code[10], {}) )

    if 'pic8' in request.files:
        file8= request.files['pic8']
        if file8 and allowed_file(file8.filename):
            filename = secure_filename(file8.filename)

            savedFileName = str(uuid.uuid4()) + get_file_ext(filename)
            file8.save(os.path.join(UPLOAD_FOLDER, savedFileName ) )
            dictFiles["pic8"] = savedFileName;

        else:
            return obj2json(RetModel(10, dict_err_code[10], {}) )

    if 'pic9' in request.files:
        file9= request.files['pic9']
        if file9 and allowed_file(file9.filename):
            filename = secure_filename(file9.filename)

            savedFileName = str(uuid.uuid4()) + get_file_ext(filename)
            file9.save(os.path.join(UPLOAD_FOLDER, savedFileName ) )
            dictFiles["pic9"] = savedFileName;

        else:
            return obj2json(RetModel(10, dict_err_code[10], {}) )

    return obj2json(RetModel(0, dict_err_code[0], dictFiles) )