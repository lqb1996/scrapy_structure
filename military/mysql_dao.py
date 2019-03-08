#coding=utf-8
import MySQLdb
from dataclasses import field

reserve_list = ['Call','Long','Engines','Year','From','To']
ip_host = '192.168.12.148'
db_user = 'root'
db_passwd = 'mininglamp'
which_db = 'kgvisual'


def check_reserve(raw):
    if raw in reserve_list:
        raw = 'r_'+raw
    return raw


def fetch_row(table_name, row_name_list, input_db=which_db, local_key=False, local_value=False):
    conn = MySQLdb.connect(
        host=ip_host,
        port=3306,
        user=db_user,
        passwd=db_passwd,
        db=input_db,
        charset="utf8"
    )
    cur = conn.cursor()
    sql = "select "
    if isinstance(row_name_list, str):
        sql += row_name_list
    else:
        for i in row_name_list:
            sql += i + "," if i != row_name_list[-1] else i
    sql += " from " + table_name + " where " + local_key + ' = ' +str(local_value) if local_key != False else " from " + table_name
    cur.execute(sql)
    result_list = []
    for row in cur.fetchall():       
        result_list.append(row)
    cur.close()
    conn.commit()
    conn.close()
    return result_list
    
def find_line(table_name, primary_key, key_value, input_db = which_db):
    conn= MySQLdb.connect(
        host = ip_host,
        port = 3306,
        user = db_user,
        passwd = db_passwd,
        db = input_db,
        charset="utf8"
    )
    cur = conn.cursor()
    sql_str = u'select * from '+table_name +' where '+ primary_key +'='+str(key_value)
    cur.execute(sql_str)
    results = cur.fetchall()
    if len(results) == 0:
        cur.close()
        conn.commit()
        conn.close()
        return False
    cur.close()
    conn.commit()
    conn.close()
    return True

    
def insert_field(table_name, field_name, value_name, input_db = which_db):
    conn= MySQLdb.connect(
        host = ip_host,
        port = 3306,
        user = db_user,
        passwd = db_passwd,
        db = input_db,
        charset="utf8"
    )
    sql_str = u'insert into '+ table_name +'('
    field_len = len(field_name)
    for i in range(field_len):
        if i < field_len - 1:
            sql_str = sql_str + check_reserve(field_name[i]) + ','
        else:
            sql_str = sql_str + check_reserve(field_name[i]) + ') '
    sql_str = sql_str + 'values ('
    for i in range(field_len):
        if i < field_len - 1:
            sql_str = sql_str + '"' + str(value_name[i]).replace('"', '') + '"' + ','
        else:
            sql_str = sql_str + '"' + str(value_name[i]).replace('"', '') + '"' + ') '
    try:
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
    except Exception as e:
        print(sql_str)
        print(e)
        raise
    cur.close()
    conn.close()
    
def update_field(table_name, field_name, value_name, key, value, input_db = which_db):
    try:
        conn= MySQLdb.connect(
            host = ip_host,
            port = 3306,
            user = db_user,
            passwd = db_passwd,
            db =input_db,
            charset="utf8"
        )
        sql_str = u'update '+ table_name +' set '
        field_len = len(field_name)
        for i in range(field_len):
            if i < field_len - 1:
                sql_str = sql_str + check_reserve(field_name[i]) + '=' + '"' + str(value_name[i]).replace('"', '') + '"' + ','
            else:
                sql_str = sql_str + check_reserve(field_name[i]) + '=' + '"' + str(value_name[i]).replace('"', '') + '"'
        sql_str = sql_str + ' where '+ key + '=' + '"' + str(value) + '"'
        cur = conn.cursor()
        cur.execute(sql_str)
        cur.close()
        conn.commit()
        conn.close()
    except Exception as e:
        print(sql_str)
        print(e)
        raise
    
if __name__ == '__main__':
    #a = find_line("ais_basic", "Id", 1)
    #print(a)
    table_name = "ais_basic"
    field_name =  ["Id","Icao"]
    value_name = [2,"3"]
    update_field(table_name, field_name, value_name)
    #insert_field(table_name, field_name, value_name)