import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'models'))

#print(sys.path)

from mysql_python import MysqlPython
from models.User import User
from models.Customer import Customer
import MySQLdb
from DBUtils.PooledDB import PooledDB
import hashlib
import time

g_dbPool = PooledDB(MySQLdb, 5, host='localhost', user='notes', passwd='welc0me', db='db_notes', port=3306, charset = "utf8", use_unicode = True);
