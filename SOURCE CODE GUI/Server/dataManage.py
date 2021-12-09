import json
import requests
from bs4 import BeautifulSoup
from datetime import date, datetime

Wiki_URL = 'https://vi.wikipedia.org/wiki/B%E1%BA%A3n_m%E1%BA%ABu:D%E1%BB%AF_li%E1%BB%87u_%C4%91%E1%BA%A1i_d%E1%BB%8Bch_COVID-19/S%E1%BB%91_ca_nhi%E1%BB%85m_theo_t%E1%BB%89nh_th%C3%A0nh_t%E1%BA%A1i_Vi%E1%BB%87t_Nam#cite_note-1'
# Biến toàn cục chứa dữ liệu
#fi = open("data.json", "r", encoding="utf-8")
fi = open("F:\Project Python\Do an socket\Socket\SOURCE CODE GUI\Server\data.json", "r", encoding="utf-8")
full_data = fi.read()
full_data = json.loads(full_data)
fi.close()
# Biến toàn cục để lưu thông tin tài khoản
#fi2 = open('accounts.json', "r", encoding="utf-8")
fi2 = open("F:\Project Python\Do an socket\Socket\SOURCE CODE GUI\Server\\accounts.json", "r", encoding="utf-8")
accounts = fi2.read()
accounts = json.loads(accounts)
fi2.close()


# Data (nhiều ngày) được lưu trong file data.json với cấu trúc list
# full_data=[{dict ngày 1}, {dict ngày 2}, {dict ngày 3}, ...]
# dict dữ liệu mỗi ngày có dạng :
#                  oneday_data = {
#                                  'time':{ string yyyymmdd },                                       (dict)
#                                  'data': [{dict tỉnh 1}, {dict tỉnh 2}, {dict tỉnh 3}, ...]        (list of dict)
#                                }
# dict dữ liệu mỗi tỉnh có dạng:
#                  {
#                       'province': ,
#                       'cases': ,
#                       'deaths': ,
#                       'newCases': ,
#                  }


# Đổi ngày thành string
def DateToString(date):
    date_str = ''
    date_str += str(date.year)
    if (date.month < 10):
        date_str += '0'
    date_str += str(date.month)
    if (date.day < 10):
        date_str += '0'
    date_str += str(date.day)
    return date_str


# Nhiệm vụ: lấy dữ liệu từ thirty web về và tạo thành list dữ liệu các tỉnh
# Sử dụng thư viện BeautifulSoup để biến HTML thành cây obj, lọc dữ liệu
def get_API():
    HTMLtext = requests.get(Wiki_URL).text
    soup = BeautifulSoup(HTMLtext, 'html.parser')
    table = soup.find('table', attrs={'class': 'wikitable'})
    data_table = table.tbody.find_all('tr')
    data_table = data_table[1:len(data_table)-1]

    covid_data = []
    for row in data_table:
        row = row.find_all('td')
        covid_data.append({
            'province': row[0].contents[0].string,
            'cases': row[1].string,
            'deaths': row[2].string,
            'newCases': row[3].string[:-1],
        })
    return covid_data


# Chức năng: update data (mỗi 60p server cần gọi hàm này)
# Lấy data các tỉnh dưới dạng list, kết hợp với time, tạo thành 1 khối data hoàn chỉnh
# So sánh với ngày mới nhất, nếu trùng thời gian (cùng ngày) thì update lại ngày đó
# Nếu khác ngày (qua ngày mới) thì thêm ngày mới vào (không thay đổi các ngày khác nữa)
def update_data():
    # Tạo thành 1 khối dữ liệu (new_data = time_data + covid_data)
    time_data = DateToString(date.today())
    covid_data = get_API()
    new_data = {
        'time': time_data,
        'data': covid_data
    }

    # So sánh với latest_data (ngày mới nhất được thêm vào sau cùng)
    add_data = True
    if (len(full_data) != 0):
        latest_data = full_data[-1]
        if (latest_data['time'] == new_data['time']):
            add_data = False

    if (add_data):
        full_data.append(new_data)
        print(1)
    else:
        full_data[-1] = new_data
        print(2)

    json_string = json.dumps(full_data, ensure_ascii=False)
    fo = open('data.json', "w", encoding="utf-8")
    fo.write(json_string)
    fo.close()

    print("Updated data successfully!", date.today())


# update_data()


def SearchData(province, date):
    # Binary search
    left = 0
    right = len(full_data) - 1
    mid = 0
    checkDate = False

    while(right >= left):
        mid = int((left + right)/2)
        if (full_data[mid]['time'] == date):
            checkDate = True
            break
        if (full_data[mid]['time'] < date):
            left = mid+1
        else:
            right = mid-1

    if (checkDate == False):
        return "Date not found!"
    dataBlock = full_data[mid]['data']
    for provinceData in dataBlock:
        if (provinceData['province'] == province):
            return provinceData
    return "Province not found!"


# Dữ liệu account lưu trong file accounts.json
# với dạng list các account
# mỗi account là 1 dict {'username':, 'password': }

# Kiểm tra một username đã tồn tại hay chưa
# True tồn tại, False chưa tồn tại
def checkAccounts(username):
    if (len(accounts) == 0):
        return False
    for account in accounts:
        if (account['username'] == username):
            return account['password']
    return False


def SignIn(username, password):
    psw = checkAccounts(username)
    if (psw == False):
        return "Unsuccessful! Username does not exist!"
    if (psw != password):
        return "Unsuccessful! Password does not match!"
    return "Login successful!"


def SignUp(username, password):
    if (checkAccounts(username) == False):
        accounts.append({
            'username': username,
            'password': password
        })

        json_string = json.dumps(accounts, ensure_ascii=False)
        fo = open('accounts.json', "w", encoding="utf-8")
        fo.write(json_string)
        fo.close()

        return "Sign up successfully!"
    return "Username exists!"


# print(SignUp('phong', '1'))
# print(SignUp('phong', '2'))
# print(SignUp('phongg', '1'))
# print(SignIn('phong', '1'))
# print(SignIn('phong', '2'))
