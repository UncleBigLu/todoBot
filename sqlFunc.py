
#!venv/bin/python3
import os
import psycopg2
from psycopg2 import sql
from datetime import date, datetime

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
    try:
        conn, cur = connect_sql()
    except psycopg2.DatabaseError as e:
        return False
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
    