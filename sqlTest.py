
#!venv/bin/python3
import os
import psycopg2

DB_NAME = 'todobot'
TABLE_NAME = 'todolist'

conn = psycopg2.connect(dbname="todobot",user="postgres", host="127.0.0.1", password=os.environ['sqlPasswd'])
# Open a cursor to perform database operations
cur = conn.cursor()
cur.execute("SELECT * FROM todolist")
data = cur.fetchall()
print(data)

cur.close()
conn.close()