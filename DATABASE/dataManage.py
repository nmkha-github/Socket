import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

Wiki_URL = 'https://vi.wikipedia.org/wiki/B%E1%BA%A3n_m%E1%BA%ABu:D%E1%BB%AF_li%E1%BB%87u_%C4%91%E1%BA%A1i_d%E1%BB%8Bch_COVID-19/S%E1%BB%91_ca_nhi%E1%BB%85m_theo_t%E1%BB%89nh_th%C3%A0nh_t%E1%BA%A1i_Vi%E1%BB%87t_Nam#cite_note-1'

# Data (nhiều ngày) được lưu trong file data.json với cấu trúc list
# full_data=[{dict ngày 1}, {dict ngày 2}, {dict ngày 3}, ...]
# dict dữ liệu mỗi ngày có dạng :
#                  oneday_data = {
#                                  'time':{ 'day': , 'month': , 'year':},                                  (dict)
#                                  'data': [{dict tỉnh 1}, {dict tỉnh 2}, {dict tỉnh 3}, ...]        (list of dict)
#                                }
# dict dữ liệu mỗi tỉnh có dạng:
#                  {
#                       'province': ,
#                       'cases': ,
#                       'deaths': ,
#                       'newCases': ,
#                  }

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
    today = datetime.today()
    time_data = {
        'day': today.day,
        'month': today.month,
        'year': today.year
    }
    covid_data = get_API()
    new_data = {
        'time': time_data,
        'data': covid_data
    }

    # Đọc file lấy tất cả dữ liệu các ngày ra
    fi = open('data.json', "r", encoding="utf-8")
    full_data = fi.read()
    full_data = json.loads(full_data)
    fi.close()

    # So sánh với latest_data (ngày mới nhất được thêm vào sau cùng)
    add_data = True
    if (len(full_data) != 0):
        latest_data = full_data[-1]
        if (latest_data['time'] == new_data['time']):
            add_data = False

    if (add_data):
        full_data.append(new_data)
    else:
        full_data[-1] = new_data

    json_string = json.dumps(full_data, ensure_ascii=False)
    fo = open('data.json', "w", encoding="utf-8")
    fo.write(json_string)
    fo.close()

    print("Updated data successfully!", today)


# update_data()
def SearchData(province, date):
    print()
