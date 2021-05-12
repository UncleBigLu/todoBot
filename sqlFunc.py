
#!venv/bin/python3
import os
import psycopg2
from psycopg2 import sql
from datetime import date, datetime, timedelta

DB_NAME = 'todobot'
TABLE_NAME = 'todolist'

def connect_sql():
    conn = psycopg2.connect(dbname=DB_NAME, user="postgres", host="127.0.0.1", password=os.environ['sqlPasswd'])
    # Open a cursor to perform database operations
    cur = conn.cursor()
    return conn, cur

# cur.execute("SELECT * FROM todolist")
# data = cur.fetchall()
# print(data)
def disconnect_sql(conn, cur):
    cur.close()
    conn.close()

def insert_data(time, event):

    conn, cur = connect_sql()
    current_time = datetime.now()
   
    cur.execute(
        sql.SQL('''
        INSERT INTO {}
        VALUES(%s, %s, %s, %s)
        ''').format(sql.Identifier(TABLE_NAME))
        , [event, time, False, current_time]
    )
    conn.commit()

    disconnect_sql(conn, cur)

def select_daily():
    conn, cur = connect_sql()

    current_time = datetime.now()
    cur.execute(
        '''
        SELECT event_name FROM todolist
        WHERE todo_time::date = %s;
        '''
        , [current_time.date()]
    )
    ret = cur.fetchall()
    
    disconnect_sql(conn, cur)
    return ret

def select_per_hour():
    conn, cur = connect_sql()

    current_time = datetime.now()
    cur.execute(
        '''
        SELECT event_name, todo_time FROM todolist
        WHERE todo_time BETWEEN %s AND %s;
        '''
        , [current_time, current_time+timedelta(hours=4)]
    )
    ret = cur.fetchall()
    disconnect_sql(conn, cur)
    return ret

