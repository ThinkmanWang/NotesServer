
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
from utils.user_db_utils import *  

from models.User import User
from models.Customer import Customer

def insert_note(uid, note):
    if (True == if_note_exists(note)):
        return update_note_info(uid, note)
    else:
        if (is_note_deleted(note["id"])):
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
                                    , (note["id"], note["uid"], note["date"], note["update_date"], note["customer_id"], note["thumbnail"], note["pic"], note["address"], note["longitude"], note["latitude"], note["note"]))
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
        if (is_note_deleted(note["id"])):
            #check the update_date and confirm if need restore group
            cur.execute("select * from notes where id=%s and is_deleted=1 and update_date < %s" , (note["id"], note["update_date"]) )
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
                            , (note["update_date"], note["id"]))
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
        cur.execute("select * from notes where id=%s" , (note["id"], ))
        
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
        cur.execute("select * from notes where id=%s", (id, ))
        
        rows=cur.fetchall()
        if (len(rows) < 1):
            return False
        else:
            return True
    except MySQLdb.Error,e:
        return False
    finally:
        cur.close()

def find_notes(szUid, szCustomerId, note):
    conn = g_dbPool.connection()
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    try:
        #cur.execute("select * from view_notes where id=%s and uid=%s", (id, uid))
        cur.execute("select * from view_notes where uid=%s and customer_id=%s and note=%s and pic=%s", (szUid, szCustomerId, note["note"], note["pic"]))

        rows = cur.fetchall()
        if (len(rows) < 1):
            return False
        else:
            return True
    except MySQLdb.Error, e:
        return False
    finally:
        cur.close()

def update_note_info(uid, note):
    conn = g_dbPool.connection()
    cur=conn.cursor()
    try:
        count = cur.execute("update notes set uid=%s, date=%s, update_date = %s, customer_id=%s, thumbnail=%s, pic=%s, address=%s, longitude=%s, latitude=%s, note=%s, is_deleted=0 where id = %s and update_date <= %s" \
                    , (uid, note["date"], note["update_date"], note["customer_id"], note["thumbnail"], note["pic"], note["address"], note["longitude"], note["latitude"], note["note"], note["id"], note["update_date"]))
        
        conn.commit()
        if (count >= 0):
            return True
        else:
            return False    
    except MySQLdb.Error,e:
        return False
    finally:
        cur.close()     
        
def select_exists_note_list(uid, szLimit, szOffset):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)    
    lstNotes = []
    try: 
        szSql = "select * from view_notes where uid=" + uid + "  and repost_from='0' and is_deleted=0 limit " + szLimit + " offset" + szOffset
        cur.execute(szSql)
        
        rows=cur.fetchall()
        for row in rows:
            lstNotes.append(init_note(row))
        
        return lstNotes 
    except MySQLdb.Error,e:
        return lstNotes 
    finally:
        cur.close()  
        
def select_all_note_list(uid, szLimit, szOffset):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)    
    lstNotes = []
    try:
        szSql = "select * from view_notes where uid=" + uid + " and repost_from='0' limit " + str(szLimit) + " offset " + str(szOffset)
        cur.execute(szSql)
        
        rows=cur.fetchall()
        for row in rows:
            lstNotes.append(init_note(row))
        
        return lstNotes 

    except MySQLdb.Error,e:
        return lstNotes 
    finally:
        cur.close()  

def select_all_notes_for_customer(szUid, szCustomerId):
    conn = g_dbPool.connection()
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    lstNotes = []
    try:
        cur.execute("select * from view_notes where uid=%s and customer_id=%s", (szUid, szCustomerId) )

        rows = cur.fetchall()
        for row in rows:
            lstNotes.append(init_note(row))

        return lstNotes

    except MySQLdb.Error, e:
        return lstNotes
    finally:
        cur.close()

def select_note_list(uid, szLimit, szOffset, type=0):
    if (type.isdigit() and 0 == int(type)):
        return select_all_note_list(uid, szLimit, szOffset)
    else:
        return select_exists_note_list(uid, szLimit, szOffset)
        
def init_note(row):
    note = {}
    note["id"] = row['id']
    note["uid"] = row['uid']
    note["date"] = row['date']
    note["customer_id"] = row['customer_id']
    note["customer_name"] = row['customer_name']
    note["address"] = row['address']
    note["longitude"] = row['longitude']
    note["latitude"] = row['latitude'] 
    note["note"] = row['note']
    note["thumbnail"] = row['thumbnail']
    note["pic"] = row['pic']    
    note["update_date"] = row['update_date']    
    note["is_deleted"] = row['is_deleted']
    note["repost_from"] = row['repost_from']
    note["avatar"] = row['avatar']
    note["author"] = row['author']

    if note["repost_from"] == "0" :
        note["repost_note"] = {}
    else:
        note["repost_note"] = db_select_note(note["repost_from"])
    
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
        
def select_note_for_member(uid, szLimit, szOffset):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)
    lstNotes = []
    try:
        szSql = "select * from view_notes where uid=" + uid + "  order by date desc limit " + szLimit + " offset " + szOffset
        cur.execute(szSql)
        #cur.execute("select * from view_notes where uid=%s" , (uid, ))
        
        rows=cur.fetchall()
        if (len(rows) < 1):
            return lstNotes
        for row in rows:
            lstNotes.append(init_note(row))
        
        return lstNotes 
        
    
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

def db_query_posts_public_to_me(szUid, szLimit, szOffset):
    #1. query uids of my members to list
    #2. add my id into list
    #3. query all posts in uid list
    lstUser = []
    lstUser.extend(db_get_member_list(szUid))
    for user in lstUser:
        lstUser.extend(db_get_member_list(str(user["id"])))


    if (lstUser is None or 0 == len(lstUser)):
        return []

    user = lstUser[0]
    szUids = "(" + str(user["id"])


    for user in lstUser:
        szUids += ", " + str(user["id"])

    szUids += ", " + szUid + ")"

    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)    
    lstNotes = []
    try:
        szSql = "select * from view_notes where uid in " + szUids + \
                " or repost_from in (select id from view_notes where uid=" + szUid + ") order by date desc limit " + szLimit + " offset " + szOffset
        cur.execute(szSql)
        
        rows=cur.fetchall()
        for row in rows:
            lstNotes.append(init_note(row))
        
        return lstNotes 

    except MySQLdb.Error,e:
        return lstNotes 
    finally:
        cur.close()  

def db_select_note(szId):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)    
    try:
        cur.execute("select * from view_notes where id=%s", (szId, ))
        
        rows=cur.fetchall()
        if rows is None or 0 == len(rows):
            return None

        note = init_note(rows[0])
        
        return note

    except MySQLdb.Error,e:
        return None 
    finally:
        cur.close()  



def db_repost_note(uid, note):
    conn = g_dbPool.connection()
    cur=conn.cursor()    
    try:
        count = cur.execute("insert into notes(id, uid, date, update_date, customer_id, thumbnail, pic, address, \
                longitude, latitude, note, repost_from) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) " \
                , (note["id"], note["uid"], str(note["date"]), str(note["update_date"]), note["customer_id"], note["thumbnail"],
                    note["pic"], note["address"], note["longitude"], note["latitude"], note["note"], note["repost_from"]))
        conn.commit()
        if (1 == count):
            return True
        else:
            return False 
                
    except MySQLdb.Error,e:
        print e
        return False
    finally:
        cur.close()                
