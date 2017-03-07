#!/usr/bin/python
#coding=utf-8

import os
import sys

import MySQLdb
from DBUtils.PooledDB import PooledDB
import hashlib
import time
import random
import logging

g_dbPool = PooledDB(MySQLdb, 5, host='127.0.0.1', user='notes', passwd='welc0me', db='db_notes', port=3306, charset = "utf8", use_unicode = True);

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',\
    datefmt='%a, %d %b %Y %H:%M:%S',\
    filename='myapp.log',\
    filemode='w')

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
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        print >>sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)

    print ("start add rendom user")
    for i in range(1, 2500000):
        szPhone = str(random.randint(11111111111, 99999999999))
        szPwd = "123456"
        logging.info("create user %d %s ==> %s" % (i, szPhone, szPwd))
        # nPhone = random.randint(11111111111, 99999999999)
        create_random_user(szPhone, szPwd)

