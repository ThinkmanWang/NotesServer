
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

def select_alarm_list(uid):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("select * from alarm where uid=%s" , uid)  
    rows=cur.fetchall()
    
    lstAlarm = []
    for row in rows:
        alarm = Alarm()
        alarm.id = row['id']
        alarm.uid = row['uid']
        alarm.note_id = row['note_id']
        alarm.date = row['date']
        alarm.update_date = row['update_date']
    
        lstAlarm.append(alarm)
        
    cur.close()
    return lstAlarm       
    

def insert_alarm(uid, id, note_id, date, update_date):
    if (True == if_alarm_exists(id)):
        return update_alarm_info(uid, id, note_id, date, update_date)
    else:
        conn = g_dbPool.connection()
        cur=conn.cursor()    
        count = cur.execute("insert into alarm(id, uid, note_id, date, update_date) values (%s, %s, %s, %s, %s) " \
                            , (id, uid, note_id, date, update_date))
        conn.commit()
        if (1 == count):
            return True
        else:
            return False 
        
def if_alarm_exists(alarm_id):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("select * from alarm where id=%s" , alarm_id)
    
    rows=cur.fetchall()
    if (len(rows) < 1):
        return False
    else:
        return True
    
def update_alarm_info(uid, id, note_id, date, update_date):
    conn = g_dbPool.connection()
    cur=conn.cursor()
    count = cur.execute("update alarm set uid=%s, note_id=%s, date=%s, update_date = %s where id = %s" \
                , (uid, note_id, date, update_date, id))
    
    conn.commit()
    if (count >= 0):
        return True
    else:
        return False 

def remove_alarm(id):
    conn = g_dbPool.connection()
    cur=conn.cursor()
    count = cur.execute("delete from alarm id = %s", id)
    
    conn.commit()
    if (1 == count):
        return True
    else:
        return False     
    