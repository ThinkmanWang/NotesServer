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

def insert_customer(uid, customer):
    if (True == if_customer_exists(customer)):
        return update_customer_info(uid, customer)
    else:
        if (is_customer_deleted(customer)):
            if (is_customer_need_restore(customer)):
                restore_customer(customer)
            
            return True
      
        else:
            try:
                conn = g_dbPool.connection()
                cur=conn.cursor()    
                count = cur.execute("insert into customer(id, uid, name, group_name, spell, address, longitude, latitude, boss, phone, email, description, update_date) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) " \
                                    , (customer.id, uid, customer.name, customer.group_name, customer.spell, customer.address, customer.longitude, customer.latitude, customer.boss, customer.phone, customer.email, customer.description, customer.update_date))
                conn.commit()
                if (1 == count):
                    return True
                else:
                    return False        
            except MySQLdb.Error,e:
                return False
            finally:
                cur.close()            

def if_customer_exists(customer):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("select * from customer where id=%s and is_deleted=0" , customer.id)
    
    rows=cur.fetchall()
    if (len(rows) < 1):
        return False
    else:
        return True
    
def is_customer_deleted(customer):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("select * from customer where id=%s and is_deleted=1" , customer.id)
    
    rows=cur.fetchall()
    if (len(rows) < 1):
        return False
    else:
        return True
    
def is_customer_need_restore(customer):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)    
    try:
        if (is_customer_deleted(customer)):
            #check the update_time and confirm if need restore group
            cur.execute("select * from customer where id=%s and is_deleted=1 and update_time < %s" , customer.id, customer.update_date)    
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
        
def restore_customer(customer):
    conn = g_dbPool.connection()
    cur=conn.cursor()            
    try:
        count = cur.execute("update customer set update_date=%s, is_deleted=0 where id=%s " \
                            , (customer.update_date, customer.id))
        conn.commit()
        if (count >= 0):
            return True
        else:
            return False    
    except MySQLdb.Error,e:
        return False
    finally:
        cur.close()
    
def update_customer_info(uid, customer):
    conn = g_dbPool.connection()
    cur=conn.cursor()
    count = cur.execute("update customer set uid = %s, name = %s, group_name = %s, spell = %s, address = %s, longitude = %s, latitude = %s, boss = %s, phone = %s, email = %s, description = %s, update_date = %s where id = %s and update_date <= %s" \
                , (uid, customer.name, customer.group_name, customer.spell, customer.address, customer.longitude, customer.latitude, customer.boss, customer.phone, customer.email, customer.description, customer.update_date, customer.id, customer.update_date))
    
    conn.commit()
    if (count >= 0):
        return True
    else:
        return False   
    
def init_customer(row):
    customer = Customer()
    customer.id = row['id']
    customer.uid = row['uid']
    customer.name = row['name']
    customer.group_name = row['group_name']
    customer.spell = row['spell']

    customer.address = row['address']
    customer.longitude = row['longitude']
    customer.latitude = row['latitude']
    customer.boss = row['boss']
    customer.phone = row['phone']

    customer.email = row['email']
    customer.description = row['description']
    customer.update_date = row['update_date']    
    customer.is_deleted = row['is_deleted']
    
    return customer
    
def select_customer_list(uid, type = 0):
    if (0 == type):
        return select_all_customer_list(uid)
    else:
        return select_exists_customer_list(uid)

def select_all_customer_list(uid):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("select * from customer where uid=%s" , uid)
    
    rows=cur.fetchall()    
    
    lstCustomer = []
    for row in rows:
        lstCustomer.append(init_customer(row))
        
    cur.close()
    return lstCustomer       
    
def select_exists_customer_list(uid):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("select * from customer where uid=%s and is_deleted=0" , uid)
    
    rows=cur.fetchall()    
    
    lstCustomer = []
    for row in rows:
        lstCustomer.append(init_customer(row))
        
    cur.close()
    return lstCustomer       

def select_customer(uid, id):
    conn = g_dbPool.connection()
    cur=conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("select * from customer where id=%s and uid=%s and is_deleted=0" , (id, uid))
    
    rows=cur.fetchall()
    if (len(rows) < 1):
        return None
    
    row = rows[0]
    customer = init_customer(row)
    
    cur.close()
    return customer   