import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import date, datetime
abspath = os.path.abspath(__file__) 
dname = os.path.dirname(abspath)
os.chdir(dname)
Wiki_URL = 'https://vi.wikipedia.org/wiki/B%E1%BA%A3n_m%E1%BA%ABu:D%E1%BB%AF_li%E1%BB%87u_%C4%91%E1%BA%A1i_d%E1%BB%8Bch_COVID-19/S%E1%BB%91_ca_nhi%E1%BB%85m_theo_t%E1%BB%89nh_th%C3%A0nh_t%E1%BA%A1i_Vi%E1%BB%87t_Nam#cite_note-1'
from convert import *
VietTat_URL='https://vi.wikipedia.org/wiki/B%E1%BA%A3n_m%E1%BA%ABu:K%C3%BD_ki%E1%BB%87u_quy_%C6%B0%E1%BB%9Bc_c%C3%A1c_t%E1%BB%89nh_th%C3%A0nh_Vi%E1%BB%87t_Nam'

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

def lcs(X, Y): 
    m = len(X)
    n = len(Y)
    L = [[0 for x in range(n+1)] for y in range(m+1)] 
    res=0
    for i in range(m+1):
        for j in range(n+1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif (X[i-1] == Y[j-1]):
                L[i][j] = L[i-1][j-1] + 1
            else:
                L[i][j] = max(L[i-1][j],L[i][j-1])
    if(float(L[m][n]/n) >= 0.7):     #Tỉ lệ đúng 70%
        return L[m][n]
    else:
        return 0
    
def SearchData(province, date):
    try:
        fileName = os.getcwd() + '\data\\'+date+'.json'
        fi = open(fileName, "r", encoding="utf-8")
        data = fi.read()
        data = json.loads(data)
        fi.close()
        res=0
        lastres='Province not found!'
        province = convert_to_eng(formatText(province))
        percent_limit = float(75)       #Chính xác 75%
        for provinceData in data:
            provinceCheck=provinceData['province']
            result=lcs(province, convert_to_eng(provinceCheck))
            # print(provinceCheck, ' ', result)
            if (result > 0) and (result + 3 * int(len(provinceCheck) / 12)) / len(provinceCheck) >= percent_limit / 100:
                if ((result + 3 * int(len(provinceCheck) / 12)) / len(provinceCheck) > res):
                    res = (result + 3 * int(len(provinceCheck) / 12)) / len(provinceCheck)
                    lastres = provinceData
                elif (result == res) and (len(provinceCheck) > len(lastres['province'])):
                    res = result
                    lastres = provinceData
        print('Match percent: ', res * 100, '%')
        return lastres
    except:
        return "Date not found!"


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


def get_VietTat():  
    HTMLtext = requests.get(VietTat_URL).text
    soup = BeautifulSoup(HTMLtext, 'html.parser')
    table = soup.find('table', attrs={'class': 'wikitable'})
    data_table = table.tbody.find_all('tr')
    data_table = data_table[1:len(data_table)-1]
    viettat_data = []
    for row in data_table:
        row = row.find_all('td')
        province=row[0].contents[0].string
        if(province=='Thành phố Hồ Chí Minh'):
            province='TP. Hồ Chí Minh'
        viettat_data.append({
            'province': province,
            'abbreviation': row[1].string,
        })
    return viettat_data

def update_data():
    fileName = os.getcwd() + '/data/'+DateToString(date.today()) + '.json'
    json_string = json.dumps(get_API(), ensure_ascii=False)
    fo = open(fileName, "w", encoding="utf-8")
    fo.write(json_string)
    fo.close()
    return "Updated data successfully!" + str(datetime.today())
def vietTat_data():
    fileName = os.getcwd() + '/data/viettat.json'
    json_string = json.dumps(get_VietTat(), ensure_ascii=False)
    fo = open(fileName, "w", encoding="utf-8")
    fo.write(json_string)
    fo.close()

def checkAccounts(username):
    fi = open(os.getcwd() + '/data/accounts.json', "r", encoding="utf-8")
    accounts = fi.read()
    accounts = json.loads(accounts)
    fi.close()
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
    fileName = os.getcwd() + '/data/accounts.json'
    fi = open(fileName, "r", encoding="utf-8")
    accounts = fi.read()
    accounts = json.loads(accounts)
    fi.close()
    if (checkAccounts(username) == False):
        accounts.append({
            'username': username,
            'password': password
        })

        json_string = json.dumps(accounts, ensure_ascii=False)
        fo = open(fileName, "w", encoding="utf-8")
        fo.write(json_string)
        fo.close()

        return "Sign up successfully! (" + username + ")"
    return "Sign up unsuccessfully! (Username exists)"
