import sqlite3
import pandas as pd

conn = sqlite3.connect('INSTRUCTOR.db')
cursor_obj = conn.cursor()

cursor_obj.execute("DROP TABLE IF EXISTS INSTRUCTOR")
table = """ create table IF NOT EXISTS INSTRUCTOR(ID INTEGER PRIMARY KEY NOT NULL, FNAME VARCHAR(20), LNAME VARCHAR(20), CITY VARCHAR(20), CCODE CHAR(2)); """
cursor_obj.execute(table)
print("Table is Ready")

cursor_obj.execute(
    '''insert into INSTRUCTOR values (1, 'Rav', 'Ahuja', 'TORONTO', 'CA')''')
cursor_obj.execute(
    '''insert into INSTRUCTOR values (2, 'Raul', 'Chong', 'Markham', 'CA'), (3, 'Hima', 'Vasudevan', 'Chicago', 'US')''')

statement = ''' SELECT * FROM INSTRUCTOR'''
cursor_obj.execute(statement)

print("All the data")
output_all = cursor_obj.fetchall()
for row_all in output_all:
    print(row_all)

print("All the data")
output_many = cursor_obj.fetchmany(2)
for row_many in output_many:
    print(row_many)

print("All the data")
output_column = cursor_obj.fetchall()
for fetch in output_column:
    print(fetch)

query_update = '''update INSTRUCTOR set CITY='MOOSETOWN' where FNAME="Rav"'''
cursor_obj.execute(query_update)

statement = '''SELECT * FROM INSTRUCTOR'''
cursor_obj.execute(statement)

print("All the data")
output1 = cursor_obj.fetchmany(2)
for row in output1:
    print(row)

df = pd.read_sql_query("SELECT * FROM INSTRUCTOR;", conn)
print(df)

print(df.LNAME[0])
print(df.shape)

conn.close()
