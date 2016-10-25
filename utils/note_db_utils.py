
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

def insert_note(uid, note):
    if (True == if_note_exists(note)):
        return update_note_info(uid, note)
    else:
        if (is_note_deleted(note.id)):
            if (is_note_need_restore(note)):
                restore_note(note)
                return update_note_info(uid, note)
            else:
                return True
        
        else:        
            conn = g_dbPool.connection()
            cur=conn.cursor()    
            try:
                count = cur.execute("insert into notes(id, uid, date, update_date, customer_id, thumbnail, pic, address, longitude, latitude, note) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) " \
                                    , (note.id, note.uid, note.date, note.update_date, note.customer_id, note.thumbnail, note.pic, note.address, note.longitude, note.latitude, note.note))
                conn.commit()
                if (1 == count):
                    return True
                else:
                    return False 
                
            except MySQLdb.Error,e:
                return False
            finally:
                cur.close()                
        
def is_note_deleted(note_id):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)
    try:
        cur.execute("select * from notes where id=%s and is_deleted=1" , (note_id, ))
        
        rows=cur.fetchall()
        if (len(rows) < 1):
            return False
        else:
            return True
        
    except MySQLdb.Error,e:
        return False
    finally:
        cur.close()    
    
def is_note_need_restore(note):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)    
    try:
        if (is_note_deleted(note.id)):
            #check the update_date and confirm if need restore group
            cur.execute("select * from notes where id=%s and is_deleted=1 and update_date < %s" , (note.id, note.update_date) )    
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
        
def restore_note(note):
    conn = g_dbPool.connection()
    cur=conn.cursor()            
    try:
        count = cur.execute("update notes set update_date=%s, is_deleted=0 where id=%s " \
                            , (note.update_date, note.id))
        conn.commit()
        if (count >= 0):
            return True
        else:
            return False    
        
    except MySQLdb.Error,e:
        return False
    finally:
        cur.close()
        
        
def if_note_exists(note):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)
    try:
        cur.execute("select * from notes where id=%s" , (note.id, ))
        
        rows=cur.fetchall()
        if (len(rows) < 1):
            return False
        else:
            return True
    
    except MySQLdb.Error,e:
        return False
    finally:
        cur.close()        

def if_noteid_exists(id):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)
    try:
        cur.execute("select * from notes where id=%s" , (id, ))
        
        rows=cur.fetchall()
        if (len(rows) < 1):
            return False
        else:
            return True
    except MySQLdb.Error,e:
        return False
    finally:
        cur.close()        
    
def update_note_info(uid, note):
    conn = g_dbPool.connection()
    cur=conn.cursor()
    try:
        count = cur.execute("update notes set uid=%s, date=%s, update_date = %s, customer_id=%s, thumbnail=%s, pic=%s, address=%s, longitude=%s, latitude=%s, note=%s, is_deleted=0 where id = %s and update_date <= %s" \
                    , (uid, note.date, note.update_date, note.customer_id, note.thumbnail, note.pic, note.address, note.longitude, note.latitude, note.note, note.id, note.update_date))
        
        conn.commit()
        if (count >= 0):
            return True
        else:
            return False    
    except MySQLdb.Error,e:
        return False
    finally:
        cur.close()     
        
def select_exists_note_id_list(uid):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)    
    try:
        cur.execute("select id from notes where uid=%s and is_deleted=0" , (uid, ))
        rows=cur.fetchall()    
        
        lstNotesId = []
        for row in rows:
            noteId = {}
            noteId['id'] = row['id']
            lstNotesId.append(noteId)
        
        return lstNotesId   

    except MySQLdb.Error,e:
        return False
    finally:
        cur.close()   
        
def select_all_note_id_list(uid):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)    
    try:
        cur.execute("select id from notes where uid=%s" , (uid, ))
        rows=cur.fetchall()    
        
        lstNotesId = []
        for row in rows:
            noteId = {}
            noteId['id'] = row['id']
            lstNotesId.append(noteId)
        
        return lstNotesId   

    except MySQLdb.Error,e:
        return False
    finally:
        cur.close()  
    
    
def select_note_id_list(uid, type=0):
    if (type.isdigit() and 0 == int(type)):
        return select_all_note_id_list(uid)
    else:
        return select_exists_note_id_list(uid)
        
def init_note(row):
    note = Note()
    note.id = row['id']
    note.date = row['date']
    note.customer_id = row['customer_id']
    note.customer_name = row['customer_name']
    note.address = row['address']
    note.longitude = row['longitude']
    note.latitude = row['latitude'] 
    note.note = row['note']
    note.thumbnail = row['thumbnail']
    note.pic = row['pic']    
    note.update_date = row['update_date']    
    note.is_deleted = row['is_deleted']
    
    return note

def select_note(uid, id):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)
    try:
        cur.execute("select * from view_notes where id=%s and uid=%s" , (id, uid))
        
        rows=cur.fetchall()
        if (len(rows) < 1):
            return None
        
        row = rows[0]
        note = init_note(row)
        
        return note 
    
    except MySQLdb.Error,e:
        return False
    finally:
        cur.close()    
        
def remove_note(uid, id):
    conn = g_dbPool.connection()
    cur=conn.cursor()
    
    try:
        count = cur.execute("update notes set is_deleted=1, update_date=%s where id = %s", (int(time.time()), id))
        
        conn.commit()
        if (count >= 0):
            return True
        else:
            return False     
    
    except MySQLdb.Error,e:
        return False
    finally:
        cur.close()     
