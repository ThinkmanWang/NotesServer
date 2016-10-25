
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'models'))

#print(sys.path)

from mysql_python import MysqlPython
import MySQLdb
from DBUtils.PooledDB import PooledDB
import hashlib
import time

from dbutils import * 

from models.User import User
from models.Customer import Customer
from models.Note import Note
from models.Alarm import Alarm

def init_alarm(row):
    alarm = Alarm()
    alarm.id = row['id']
    alarm.uid = row['uid']
    alarm.note_id = row['note_id']
    alarm.date = row['date']
    alarm.update_date = row['update_date']
    alarm.is_deleted = row['is_deleted']    
    
    return alarm

def select_exists_alarm_list(uid):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)
    
    try:
        cur.execute("select * from alarm where uid=%s and is_deleted=0" , uid)  
        rows=cur.fetchall()
        
        lstAlarm = []
        for row in rows:
            lstAlarm.append(init_alarm(row))
            
        return lstAlarm          

    except MySQLdb.Error,e:
        return False
    finally:
        cur.close()

def select_all_alarm_list(uid):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)
    
    try:
        cur.execute("select * from alarm where uid=%s" , uid)  
        rows=cur.fetchall()
        
        lstAlarm = []
        for row in rows:
            lstAlarm.append(init_alarm(row))
            
        return lstAlarm   

    except MySQLdb.Error,e:
        return False
    finally:
        cur.close()

def select_alarm_list(uid, type = 0):
    if (0 == type):
        return select_all_alarm_list(uid)
    else:
        return select_exists_alarm_list(uid)          
    

def insert_alarm(uid, id, note_id, date, update_date):
    if (True == if_alarm_exists(id)):
        return update_alarm_info(uid, id, note_id, date, update_date)
    else:
        if (is_alarm_deleted(alarm_id)):
            if (is_alarm_need_restore(alarm_id, update_date)):
                restore_alarm(alarm_id, update_date)
        
            return True
    
        else:        
            conn = g_dbPool.connection()
            cur=conn.cursor()    
            try:
                count = cur.execute("insert into alarm(id, uid, note_id, date, update_date) values (%s, %s, %s, %s, %s) " \
                                    , (id, uid, note_id, date, update_date))
                conn.commit()
                if (1 == count):
                    return True
                else:
                    return False 
            except MySQLdb.Error,e:
                return False
            finally:
                cur.close()        
        
def if_alarm_exists(alarm_id):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)
    try:
        cur.execute("select * from alarm where id=%s and is_deleted=0" , alarm_id)
        
        rows=cur.fetchall()
        if (len(rows) < 1):
            return False
        else:
            return True
        
    except MySQLdb.Error,e:
        return False
    finally:
        cur.close()    
    
def is_alarm_deleted(alarm_id):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)
    try:
        cur.execute("select * from alarm where id=%s and is_deleted=1" , alarm_id)
        
        rows=cur.fetchall()
        if (len(rows) < 1):
            return False
        else:
            return True
        
    except MySQLdb.Error,e:
        return False
    finally:
        cur.close()     
        
def is_alarm_need_restore(alarm_id, update_date):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)    
    try:
        if (is_alarm_deleted(alarm_id)):
            #check the update_time and confirm if need restore group
            cur.execute("select * from alarm where id=%s and is_deleted=1 and update_time < %s" , (alarm_id, update_date))    
            rows=cur.fetchall()
            if (len(rows) < 1):
                return False    
            else:
                return True
        else:
            return False
        
    except MySQLdb.Error,e:
        return False
    finally:
        cur.close()   
        
def restore_alarm(alarm_id, update_date):
    conn = g_dbPool.connection()
    cur=conn.cursor()            
    try:
        count = cur.execute("update alarm set update_date=%s, is_deleted=0 where id=%s " \
                            , (update_date, alarm_id))
        conn.commit()
        if (count >= 0):
            return True
        else:
            return False    
        
    except MySQLdb.Error,e:
        return False
    finally:
        cur.close()
    
def update_alarm_info(uid, id, note_id, date, update_date):
    conn = g_dbPool.connection()
    cur=conn.cursor()
    try:
        count = cur.execute("update alarm set uid=%s, note_id=%s, date=%s, update_date = %s where id = %s and update_date <= %s" \
                    , (uid, note_id, date, update_date, id, update_date))
        
        conn.commit()
        if (count >= 0):
            return True
        else:
            return False 
    
    except MySQLdb.Error,e:
        return False
    finally:
        cur.close()    

def remove_alarm(id):
    conn = g_dbPool.connection()
    cur=conn.cursor()
    
    try:
        count = cur.execute("update alarm set is_delete=%s, update_date=%s where id = %s", (int(time.time()), id))
        
        conn.commit()
        if (1 == count):
            return True
        else:
            return False     
    
    except MySQLdb.Error,e:
        return False
    finally:
        cur.close()    
    