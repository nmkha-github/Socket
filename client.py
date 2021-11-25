import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Nhập 
SERVER_HOST = input("Nhap IP Server: ")
SERVER_PORT = input("Nhap Port Server: ")
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8000
#
client.connect((SERVER_HOST, SERVER_PORT))
print("Client Address: ", client.getsockname())
# Đăng nhập
account = input("Nhap tai khoan: ")
password = input("Nhap mat khau: ")

client.sendall(account.encode('utf8'))
client.sendall(password.encode('utf8'))

# Tra cứu