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


def insert_customer(uid, customer):
    if (True == if_customer_exists(customer)):
        return update_customer_info(uid, customer)
    else:
        conn = g_dbPool.connection()
        cur=conn.cursor()    
        count = cur.execute("insert into customer(id, uid, name, group_name, spell, address, longitude, latitude, boss, phone, email, description) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) " \
                            , (customer.id, uid, customer.name, customer.group_name, customer.spell, customer.address, customer.longitude, customer.latitude, customer.boss, customer.phone, customer.email, customer.description))
        conn.commit()
        if (1 == count):
            return True
        else:
            return False        

def if_customer_exists(customer):
    conn = g_dbPool.connection()
    cur=conn.cursor()
    cur.execute("select * from customer where id=%s" , customer.id)
    
    rows=cur.fetchall()
    if (len(rows) < 1):
        return False
    else:
        return True
    
def update_customer_info(uid, customer):
    conn = g_dbPool.connection()
    cur=conn.cursor()
    count = cur.execute("update customer set uid = %s, name = %s, group_name = %s, spell = %s, address = %s, longitude = %s, latitude = %s, boss = %s, phone = %s, email = %s, description = %s where id = %s" \
                , (uid, customer.name, customer.group_name, customer.spell, customer.address, customer.longitude, customer.latitude, customer.boss, customer.phone, customer.email, customer.description, customer.id))
    
    conn.commit()
    if (count >= 0):
        return True
    else:
        return False        