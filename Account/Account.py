import pyodbc

#print(pyodbc.drivers())
# type in your DATABASE info here 

SERVER = 'LAPTOP-76D6AFE8\SQLEXPRESS'   # Sửa dòng này tùy theo máy
USER = 'kha'                            # Sửa dòng này tùy theo account tạo
PASSWORD = '123'                        # Sửa dòng này tùy theo account tạo
DATABASE = 'Socket_Account'             # import database vào

# connect to database 
conx = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};\
                        SERVER='+ SERVER +'; DATABASE='+ DATABASE +
                        ';UID='+ USER +'; PWD='+ PASSWORD + ';')
cursor = conx.cursor()

# function
def register(username, password):   #thêm tài khoản đăng kí vào database
    cursor.execute("insert Account values (?, ?)", username, password)
    conx.commit()
    return

def check_Account(username, password):  #kiểm tra tài khoản mật khẩu
    data = cursor.execute("SELECT * FROM Account")
    for row in data:
        if username == row[0]:
            if password == row[1]:
                return 'ACCEPTED'
            else:
                return 'WRONG PASSWORD'
    return 'ACCOUNT IS NOT EXIST'

conx.close()