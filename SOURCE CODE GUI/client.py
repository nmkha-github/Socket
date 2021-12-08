import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Nhập 
SERVER_HOST = input("Nhap IP Server: ")
SERVER_PORT = int(input("Nhap Port Server: "))
#SERVER_HOST = '127.0.0.1'
#SERVER_PORT = 8000
#
try:
    client.connect((SERVER_HOST, SERVER_PORT))
except:
    ## thông báo không tìm thấy server
    print("SERVER not found")
    input()
    client.close()
print("Client Address: ", client.getsockname())
# Đăng nhập
account = input("Nhap tai khoan: ")
password = input("Nhap mat khau: ")
client.sendall(account.encode('utf8'))
client.sendall(password.encode('utf8'))
print(client.recv(1024).decode('utf8'))
input()
# Tra cứu