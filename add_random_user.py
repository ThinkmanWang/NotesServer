#!/usr/bin/python
#coding=utf-8

import sys

import MySQLdb
from DBUtils.PooledDB import PooledDB
import hashlib
import time
import random

g_dbPool = PooledDB(MySQLdb, 5, host='function-hz.com', user='notes', passwd='welc0me', db='db_notes', port=3306, charset = "utf8", use_unicode = True);

def create_random_user(user_name, szPwd):
    #create user by cell phone number and send dynamic password
    conn = g_dbPool.connection()
    cur=conn.cursor()
    count = cur.execute("insert into user(user_name, password) values (%s, %s) " \
                        , (user_name, hashlib.md5(szPwd).hexdigest()))
    conn.commit()

    if (1 == count):
        return True
    else:
        return False

if __name__ == '__main__':
    print ("start add rendom user")
    for i in range(1, 5000000):
        szPhone = str(random.randint(11111111111, 99999999999))
        szPwd = "123456"
        print ("create user %d %s ==> %s" % (i, szPhone, szPwd))
        # nPhone = random.randint(11111111111, 99999999999)
        create_random_user(szPhone, szPwd)

