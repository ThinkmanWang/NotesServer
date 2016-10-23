
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

from dbutils import * 

def insert_note(uid, note):
    if (True == if_note_exists(note)):
        return update_note_info(uid, note)
    else:
        conn = g_dbPool.connection()
        cur=conn.cursor()    
        count = cur.execute("insert into notes(id, uid, date, customer_id, thumbnail, pic, address, longitude, latitude, note) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) " \
                            , (note.id, note.uid, note.date, note.customer_id, note.thumbnail, note.pic, note.address, note.longitude, note.latitude, note.note))
        conn.commit()
        if (1 == count):
            return True
        else:
            return False 
        
def if_note_exists(note):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("select * from notes where id=%s" , note.id)
    
    rows=cur.fetchall()
    if (len(rows) < 1):
        return False
    else:
        return True
    
def update_note_info(uid, note):
    conn = g_dbPool.connection()
    cur=conn.cursor()
    count = cur.execute("update notes set uid=%s, date=%s, customer_id=%s, thumbnail=%s, pic=%s, address=%s, longitude=%s, latitude=%s, note=%s where id = %s" \
                , (uid, note.date, note.customer_id, note.thumbnail, note.pic, note.address, note.longitude, note.latitude, note.note, note.id))
    
    conn.commit()
    if (count >= 0):
        return True
    else:
        return False    
    
def select_note_id_list(uid):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)    
    cur.execute("select id from notes where uid=%s" , uid)
    rows=cur.fetchall()    
    
    lstNotesId = []
    for row in rows:
        noteId = {}
        noteId['id'] = row['id']
        lstNotesId.append(noteId)
    
    cur.close()
    return lstNotesId       