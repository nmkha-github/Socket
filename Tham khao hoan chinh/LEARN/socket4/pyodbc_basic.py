import pyodbc

# type in your DATABASE info here 
SERVER = 'MON-ASUS\SQLEXPRESS'
DATABASE = 'Socket_Account'
USER = 'dh'
PASSWORD = '123456'

# connect to database 
conx = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};\
                        SERVER='+ SERVER +'; DATABASE='+ DATABASE +
                        ';UID='+ USER +'; PWD='+ PASSWORD + ';')


cursor = conx.cursor()

# for row in cursor.execute("select * from Account where username = 'a'"):
#     print(row.username)
#     print(row[0])
#     print(row)


# cursor.execute("select * from Account")

# data = cursor.fetchall()

# print(data)
# print(data[1][0])

# username = 'abc'
# pswd = '123'

# cursor.execute("insert Account values (?, ?)", username, pswd)
# conx.commit()

conx.close()


