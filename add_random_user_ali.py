#!/usr/bin/python
#coding=utf-8

import os
import sys

import MySQLdb
from DBUtils.PooledDB import PooledDB
import hashlib
import time
import random
import threading
import logging

THREAD_NUM = 5

g_dbPool = PooledDB(MySQLdb, THREAD_NUM, host='rm-bp19rkb764945yh98o.mysql.rds.aliyuncs.com', user='root', passwd='Ab123456', db='db_notes', port=3306, charset = "utf8", use_unicode = True);

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',\
    datefmt='%a, %d %b %Y %H:%M:%S',\
    filename='myapp_ali.log',\
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

g_nNum = 0
g_lock = threading.RLock()

def worker():
    global g_nNum
    while (True):
        g_lock.acquire()
        if (g_nNum >= 5000000):
            break
        else:
            g_nNum += 1
            continue
        g_lock.release()

        szPhone = str(random.randint(11111111111, 99999999999))
        szPwd = "123456"
        logging.info("create user %d %s ==> %s" % (g_nNum, szPhone, szPwd))
        create_random_user(szPhone, szPwd)

if __name__ == '__main__':
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        print >>sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)

    print ("start add rendom user")

    threads = []
    for i in range(THREAD_NUM):
        #create 150 thread for insert data
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    for i in range(THREAD_NUM):
        threads[i].join()

    print("Exit")
    logging.info("Exit")
