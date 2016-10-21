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

g_dbPool = PooledDB(MySQLdb, 5, host='thinkman-wang.com', user='thinkman', passwd='Ab123456', db='db_notes', port=3306, charset = "utf8", use_unicode = True);


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

def user_login(user_name, password, verify):
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
        userRet = insert_or_update_token(userRet)
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

        if (1 == count):
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