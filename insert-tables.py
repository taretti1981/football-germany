import mysql.connector
from mysql.connector.cursor import MySQLCursorPrepared
import csv
import math
from mysql.connector import Error
from mysql.connector import errorcode
from datetime import datetime

with open('1-bundesliga.csv', 'r') as csvFile:
    csvTable = csv.reader(csvFile, delimiter=';')
    csvTable = list(csvTable)


connection = mysql.connector.connect(host='195.201.131.193',
                        database='football',
                        user='root',
                        password='e(7&UE<1v)i6k=7P',
                        use_pure=True)
cursor = connection.cursor(cursor_class=MySQLCursorPrepared)
sql_insert_query = """ INSERT INTO `football_germany`
                          (`home`,`visitor`,`goals_home`,`goals_visitor`,`goals_home_half`,`goals_visitor_half`,`season`,`matchday`,`league`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
num_iter = list(range(0, math.floor(len(csvTable)/1000)+1))

try:
    for i in num_iter:
        print(str(i + 1) + ' of ' + str(len(num_iter)))
        if i == num_iter[len(num_iter)-1]:
            temp_data = csvTable[i*1000:]
        else:
            temp_data = csvTable[i*1000:(i+1)*1000]
        idx = 0
        for row in temp_data:
            if row[4]=='':
                row[4] = None
            if row[5] == '':
                row[5] = None
            temp_data[idx] = row
            idx += 1

        #idx = [j for j, s in enumerate(temp_data) if '' in s]
        #if len(idx)>0:
        #    for j in idx:


        result = cursor.executemany(sql_insert_query, temp_data)
        connection.commit()
    print("Record inserted successfully into python_users table")
    connection.close()
except NameError:
    print('error at trying to upload on iteration ' + str(i+1))
    connection.close()



