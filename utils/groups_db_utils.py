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

def init_group(row):
    group = Group()
    group.id = row['id']
    group.uid = row['uid']
    group.group_name = row['group_name']    
    group.update_date = row['update_date']     
    group.is_deleted = row['is_deleted']     
    
    return group

def select_group_list(uid, type):
    if (0 == type):
        return select_all_group_list(uid)
    else:
        return select_exists_group_list(uid)
    
def select_all_group_list(uid):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)
    lstGroup = []
    try:
        cur.execute("select * from groups where uid=%s" , uid)
        rows=cur.fetchall()    
        
        for row in rows:
            lstGroup.append(init_group(row))
        
        return lstGroup      
    except MySQLdb.Error,e:
        return lstGroup
    finally:
        cur.close()         
    
def select_exists_group_list(uid):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)
    lstGroup = []
    try:
        cur.execute("select * from groups where uid=%s and is_deleted=0" , uid)
        rows=cur.fetchall()    
        
        for row in rows:
            lstGroup.append(init_group(row))
        
        return lstGroup      
    except MySQLdb.Error,e:
        return lstGroup
    finally:
        cur.close()     

def update_group_time(uid, group_name, update_date):
    conn = g_dbPool.connection()
    cur=conn.cursor()            
    try:
        count = cur.execute("update groups set update_date=%s is_deleted=0 where uid=%s and group_name=%s " \
                            , (update_date, uid, group_name))
        conn.commit()
        if (count >= 0):
            return True
        else:
            return False    
    except MySQLdb.Error,e:
        return False
    finally:
        cur.close()    

def restore_group(uid, group_name, update_date):
    conn = g_dbPool.connection()
    cur=conn.cursor()            
    try:
        count = cur.execute("update groups set update_date=%s, is_deleted=0 where uid=%s and group_name=%s " \
                            , (update_date, uid, group_name))
        conn.commit()
        if (count >= 0):
            return True
        else:
            return False    
    except MySQLdb.Error,e:
        return False
    finally:
        cur.close()

def insert_group(uid, group_name, update_date):
    if (True == if_group_exists(uid, group_name)):
        update_group_time(uid, group_name, update_date)
        return True
    else:
        if (is_group_deleted(uid, group_name, update_date)):
            if (is_group_need_restore(uid, group_name, update_date)):
                restore_group(uid, group_name, update_date)
                return update_group_time(uid, group_name, update_date)
            else:
                return True
        else:
            conn = g_dbPool.connection()
            cur=conn.cursor()            
            try:
                count = cur.execute("insert into groups(uid, group_name, update_date) values (%s, %s, %s) " \
                                    , (uid, group_name, int(time.time()) ))
                conn.commit()
                if (1 == count):
                    return True
                else:
                    return False    
            except MySQLdb.Error,e:
                return False
            finally:
                cur.close()
    
def if_group_exists(uid, group_name):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)
    try:
        cur.execute("select * from groups where uid=%s and group_name=%s and is_deleted=0" , (uid, group_name))
        
        rows=cur.fetchall()
        if (len(rows) < 1):
            return False
        else:
            return True
    except MySQLdb.Error,e:
        return False
    finally:
        cur.close()    
    
def is_group_deleted(uid, group_name, update_date):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)
    try:
        cur.execute("select * from groups where uid=%s and group_name=%s and is_deleted=1" , (uid, group_name))    
        
        rows=cur.fetchall()
        if (len(rows) < 1):
            return False
        else:
            return True    
    except MySQLdb.Error,e:
        return False
    finally:
        cur.close()  

def is_group_need_restore(uid, group_name, update_date):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)    
    try:
        if (is_group_deleted(uid, group_name, update_date)):
            #check the update_time and confirm if need restore group
            cur.execute("select * from groups where uid=%s and group_name=%s and is_deleted=1" , (uid, group_name))    
            rows=cur.fetchall()
            if (len(rows) < 1):
                return False    
            else:
                row = rows[0]
                _update_date = row['update_date']
                
                if (int(update_date) > int(_update_date)):
                    return True
                else:
                    return False
        else:
            return False
    except MySQLdb.Error,e:
        return False
    finally:
        cur.close()  
        
def remove_group(uid, group_name):
    if (False == if_group_exists(uid, group_name)):
        return True   
    
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)
    
    try:
        count = cur.execute("update groups set is_deleted=1, update_date=%s where uid=%s and group_name=%s" , (int(time.time()), uid, group_name))
        conn.commit()
        
        if (count >= 0):
            return True
        else:
            return False    
    except MySQLdb.Error,e:
        return False
    finally:
        cur.close()  