import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'models'))

#print(sys.path)

from mysql_python import MysqlPython
from models.User import User
from models.Customer import Customer
from models.Group import Group
import MySQLdb
from DBUtils.PooledDB import PooledDB
import hashlib
import time

from dbutils import * 

def select_group_list(uid):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("select * from groups where uid=%s and is_deleted=0" , uid)
    
    rows=cur.fetchall()    
    
    lstGroup = []
    for row in rows:
        group = Group()
        group.id = row['id']
        group.uid = row['uid']
        group.group_name = row['group_name']    
        group.update_date = row['update_date']  
        
        lstGroup.append(group)
    
    cur.close()
    return lstGroup       

def insert_group(uid, group_name):
    if (True == if_group_exists(uid, group_name)):
        return True
    else:
        conn = g_dbPool.connection()
        cur=conn.cursor()    
        count = cur.execute("insert into groups(uid, group_name, update_date) values (%s, %s, %s) " \
                            , (uid, group_name, int(time.time()) ))
        conn.commit()
        if (1 == count):
            return True
        else:
            return False            
    
def if_group_exists(uid, group_name):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("select * from groups where uid=%s and group_name=%s and is_deleted=0" , (uid, group_name))
    
    rows=cur.fetchall()
    if (len(rows) < 1):
        return False
    else:
        return True
    
def remove_group(uid, group_name):
    if (False == if_group_exists(uid, group_name)):
        return True   
    
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("update groups set is_deleted=1, update_date=%s where uid=%s and group_name=%s" , (int(time.time()), uid, group_name))
    
    rows=cur.fetchall()
    if (len(rows) < 1):
        return False
    else:
        return True    