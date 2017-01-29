import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'models'))

#print(sys.path)

from mysql_python import MysqlPython
from models.User import User

import MySQLdb
from DBUtils.PooledDB import PooledDB
import hashlib
import time
import uuid

from dbutils import *
from utils.customer_db_utils import *
from utils.note_db_utils import *

#g_dbPool = PooledDB(MySQLdb, 5, host='thinkman-wang.com', user='thinkman', passwd='Ab123456', db='db_notes', port=3306, charset = "utf8", use_unicode = True);


def get_all_users() :
    conn = g_dbPool.connection()
    cur=conn.cursor()
    SQL="select * from user"
    cur.execute(SQL)

    rows=cur.fetchall()

    lstUser = []
    for row in rows:
        user = User()
        user.id = row[0]
        user.user_name = row[1]
        user.password = row[2]
        lstUser.append(user)

    cur.close()
    return lstUser

def if_user_exists(user_name):
    conn = g_dbPool.connection()
    cur=conn.cursor()
    cur.execute("select * from view_user where user_name=%s" , (user_name, ))
    
    rows=cur.fetchall()
    if (len(rows) < 1):
        return False
    else:
        return True
    
def create_user(user_name):
    #create user by cell phone number and send dynamic password
    conn = g_dbPool.connection()
    cur=conn.cursor()    
    count = cur.execute("insert into user(user_name, password) values (%s, %s) " \
                        , (user_name, hashlib.md5("123456").hexdigest()))
    conn.commit()

    if (1 == count):
        return True
    else:
        return False    

def user_login(user_name, password, verify):
    if (False == if_user_exists(user_name)):
        create_user(user_name)
        
    conn = g_dbPool.connection()
    cur=conn.cursor()
    cur.execute("select * from view_user where user_name=%s AND password=%s" , (user_name, password))

    rows=cur.fetchall()
    lstUser = []
    for row in rows:
        user = User()
        user.id = row[0]
        user.user_name = row[1]
        user.password = row[2]
        user.token = row[3]
        user.create_time = row[4]
        user.expire_time = row[5]
        lstUser.append(user)

    cur.close()

    if (lstUser != None and len(lstUser) >= 1):
        userRet = lstUser[0]
        userRet = insert_user_token(userRet)
        return userRet
    else:
        return None    
    
def verify_user_token(uid, token):
    conn = g_dbPool.connection()
    cur=conn.cursor()
    cur.execute("select * from token where uid=%s AND token=%s" , (uid, token))    
    rows=cur.fetchall()
    
    if(len(rows) > 0):
        nTime = int(time.time())
        count = cur.execute("update token set expire_time=%s where uid=%s" \
                            , (nTime + (365*24*3600), uid))
        conn.commit()        
        return True
    else:
        return False
    
def insert_user_token(user):
    conn = g_dbPool.connection()
    cur=conn.cursor()    
    
    try:
        nTime = int(time.time())
        szToken = ("%s%d" % (user.password, nTime))
        szToken = hashlib.md5(szToken).hexdigest()        
        
        count = cur.execute("insert into token(uid, token, create_time, expire_time) values (%s, %s, %s, %s) " \
                            , (user.id, szToken, nTime, nTime + (365*24*3600)))
        conn.commit()

        if (1 == count):
            user.token = szToken
            user.create_time = nTime
            user.expire_time = nTime + (365*24*3600)
            return user
        else:
            return None        
    except MySQLdb.Error,e:
        return lstGroup
    finally:
        cur.close()        
    
def insert_or_update_token(user):
    conn = g_dbPool.connection()
    cur=conn.cursor()
    cur.execute("select * from token where uid=%s " , (user.id,))
    rows=cur.fetchall()

    nTime = int(time.time())
    szToken = ("%s%d" % (user.password, nTime))
    szToken = hashlib.md5(szToken).hexdigest()
    if (len(rows) > 0):

        count = cur.execute("update token set token=%s, create_time=%s, expire_time=%s where uid=%s" \
                            , (szToken, nTime, nTime + (365*24*3600), user.id))
        conn.commit()

        if (count >= 0):
            user.token = szToken
            user.create_time = nTime
            user.expire_time = nTime + (365*24*3600)
            return user
        else:
            return None
    else:
        count = cur.execute("insert into token(uid, token, create_time, expire_time) values (%s, %s, %s, %s) " \
                            , (user.id, szToken, nTime, nTime + (365*24*3600)))
        conn.commit()

        if (1 == count):
            user.token = szToken
            user.create_time = nTime
            user.expire_time = nTime + (365*24*3600)
            return user
        else:
            return None


def db_is_user_exists(szUid):
    conn = g_dbPool.connection()
    cur=conn.cursor()
    cur.execute("select * from view_user where id=%s" , (szUid, ))
    
    rows=cur.fetchall()
    if (len(rows) < 1):
        return False
    else:
        return True

def db_set_user_leader(szUid, szLeaderUid):
    conn = g_dbPool.connection()
    cur=conn.cursor()    
    
    try:
        count = cur.execute("update user set leader_uid=%s where id=%s" \
                            , (szLeaderUid, szUid))
        conn.commit()

        if (count >= 0):
            return True
        else:
            return False        
    except MySQLdb.Error,e:
        return False
    finally:
        cur.close()        
    

def db_query_users():
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("select * from user")

    try:
        rows=cur.fetchall()
        lstUser = []
        for row in rows:
            user = {}
            user["id"] = row["id"]
            user["user_name"] = row["user_name"]
            user["avatar"] = row["avatar"]
            user["leader_uid"] = row["leader_uid"]
            user["show_name"] = row["show_name"]
            user["title"] = row["title"]
            lstUser.append(user)


        if (lstUser != None and len(lstUser) >= 1):
            return lstUser
        else:
            return None    
    except MySQLdb.Error,e:
        return None
    finally:
        cur.close()        


def db_update_user_info(szUid, avatar, show_name):
    conn = g_dbPool.connection()
    cur=conn.cursor()    
    
    try:
        count = cur.execute("update user set avatar=%s, show_name=%s where id=%s" \
                            , (avatar, show_name, szUid))
        conn.commit()

        if (count >= 0):
            return True
        else:
            return False        
    except MySQLdb.Error,e:
        return False
    finally:
        cur.close()        

def db_query_user_profile(szUid):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("select id, user_name, avatar, leader_uid" \
            " , (select d.show_name from user as d where d.id=a.leader_uid) as leader_name" \
            " , show_name, (select count(*) from user as b where b.leader_uid=a.id) as member_count " \
            " , (select count(*) from notes as c where c.uid=a.id) as note_count " \
            " , (select count(*) from customer as d where d.uid=a.id) as customer_count" \
            " from user as a where a.id=%s;" \
            , (szUid, ))

    try:
        rows=cur.fetchall()
        if (0 == len(rows)):
            return None
        
        row = rows[0]
        userProfile = {}

        lstUser = db_get_all_member_list(szUid)

        userProfile["id"] = row["id"]
        userProfile["user_name"] = row["user_name"]
        userProfile["avatar"] = row["avatar"]
        userProfile["leader_uid"] = row["leader_uid"]
        userProfile["leader_name"] = row["leader_name"]

        userProfile["show_name"] = row["show_name"]
        userProfile["member_count"] = len(lstUser)
        userProfile["note_count"] = row["note_count"]
        userProfile["customer_count"] = row["customer_count"]

        return userProfile


    except MySQLdb.Error,e:
        return None
    finally:
        cur.close()        

def db_get_all_member_list(szUid):
    #1. query uids of my members to list
    #2. add my id into list
    #3. query all posts in uid list
    lstUser = []
    lstUser.extend(db_get_member_list(szUid))
    for user in lstUser:
        lstUser.extend(db_get_member_list(str(user["id"])))

    return lstUser

def db_get_member_list(szUid):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("select id, user_name, avatar, leader_uid, show_name, title from user where leader_uid=%s" \
            , (szUid, ))

    lstUser = []
    try:
        rows=cur.fetchall()
        for row in rows:
            user = {}
            user["id"] = row["id"]
            user["user_name"] = row["user_name"]
            user["avatar"] = row["avatar"]
            user["leader_uid"] = row["leader_uid"]
            user["show_name"] = row["show_name"]
            user["title"] = row["title"]
            lstUser.append(user)


        return lstUser
    except MySQLdb.Error,e:
        return lstUser
    finally:
        cur.close()        

def db_transfer_user_data(szUidFrom, szUidDst):

    # copy all customer, and note info from User src to user dst
    # groups and alarm will not be copied

    # select all customer from user src
    # for each customer in user src, copy all notes
    lstCustomer = select_all_customer_list(szUidFrom)
    for customer in lstCustomer :
        _customer = find_customer_by_name_address(szUidDst, customer.name, customer.address)
        szCustomerId = None
        if (_customer is None):
            # No exist customer for user dst, create new customer for user dst
            szCustomerId = str(uuid.uuid4())
            _customer = customer
            _customer.id = szCustomerId

            if (False == insert_customer(szUidDst, _customer)):
                return
        else:
            # customer exists, copy notes to exist customer
            szCustomerId = _customer.id

        # select all notes from user src for customer and insert to _customer
        lstNotes = select_all_notes_for_customer(szUidFrom, customer.id)

        for note in lstNotes :
            #1. check if this note exist in user dst
            if (find_notes(szUidDst, szCustomerId, note)):
                continue

            #2. insert
            note["id"] = uuid.uuid4()
            note["uid"] = szUidDst
            note["customer_id"] = szCustomerId

            insert_note(szUidDst, note)

