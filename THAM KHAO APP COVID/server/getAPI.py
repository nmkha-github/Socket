import requests, json # can tai 
import schedule
import pandas as pd #can tai
from bs4 import BeautifulSoup #can tai
from unidecode import unidecode #can tai pip install unicode
import time
from datetime import datetime

all_country_url = "https://coronavirus-19-api.herokuapp.com/countries"
wiki_url = "https://vi.wikipedia.org/wiki/B%E1%BA%A3n_m%E1%BA%ABu:D%E1%BB%AF_li%E1%BB%87u_%C4%91%E1%BA%A1i_d%E1%BB%8Bch_COVID-19/S%E1%BB%91_ca_nhi%E1%BB%85m_theo_t%E1%BB%89nh_th%C3%A0nh_t%E1%BA%A1i_Vi%E1%BB%87t_Nam#cite_note-1"

def getDataFromAllCountryURL():
    all_country_info = json.loads(requests.get(all_country_url).text)
    all_country_info_string = json.dumps(all_country_info, sort_keys=True)
    all_country_info_file = open('dataAllCountry.json', 'w', encoding="utf-8")
    all_country_info_file.write(all_country_info_string)
    all_country_info_file.close()

def getDataFromWikiURL():
    response = requests.get(wiki_url)
    wiki_text = response.text
    soup = BeautifulSoup(wiki_text, 'html.parser')
    required_table = soup.find('table', attrs={'class':"wikitable"})
    header_tags = required_table.find_all('th')
    filtered_header_tags = [header_tag for header_tag in header_tags]
    headers = [header.text.strip() for header in header_tags]
    rows = []
    data_rows = required_table.find_all('tr')

    for row in data_rows:
        value = row.find_all('td')
        beautified_value = [dp.text.strip() for dp in value]
        if len(beautified_value) < 6:
            continue
        rows.append({
            'nameProvince': unidecode(beautified_value[0]).title(), # chuyen tu tieng viet co dau thanh ko dau va viet hoa chu dau
            'cases': beautified_value[1],
            'inProgress': beautified_value[2],
            'another': beautified_value[3],
            'recovered': beautified_value[4],
            'deaths': beautified_value[5]
        })

    vietnam_info_string = json.dumps(rows)
    vietnam_info_file = open("dataVN.json", "w", encoding="utf-8")
    vietnam_info_file.write(vietnam_info_string)
    vietnam_info_file.close()

def printTimeUpdateDatabase():
    date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("Database updated at: ", date_time)

def getData():
    printTimeUpdateDatabase()
    getDataFromAllCountryURL()
    getDataFromWikiURL()

# def getNameProvinceInVN():
#     wiki_nameProvince_url = "https://vi.wikipedia.org/wiki/B%E1%BA%A3n_m%E1%BA%ABu:K%C3%BD_ki%E1%BB%87u_quy_%C6%B0%E1%BB%9Bc_c%C3%A1c_t%E1%BB%89nh_th%C3%A0nh_Vi%E1%BB%87t_Nam"
#     response = requests.get(wiki_nameProvince_url)
#     wiki_text = response.text
#     soup = BeautifulSoup(wiki_text, 'html.parser')
#     required_table = soup.find('table', attrs={'class':"wikitable"})
#     header_tags = required_table.find_all('th')
#     filtered_header_tags = [header_tag for header_tag in header_tags]
#     headers = [header.text.strip() for header in header_tags]
#     rows = []
#     data_rows = required_table.find_all('tr')

#     for row in data_rows:
#         value = row.find_all('td')
#         beautified_value = [dp.text.strip() for dp in value]
#         if len(beautified_value) == 5:
#             rows.append({
#                 'nameFull': unidecode(beautified_value[0]).title(), # chuyen tu tieng viet co dau thanh ko dau va viet hoa chu dau
#                 'nameShort': unidecode(beautified_value[1]),
#             })
#     province_name_string = json.dumps(rows)
#     province_name_file = open("nameProvinceVN.json", "w", encoding="utf-8")
#     province_name_file.write(province_name_string)
#     province_name_file.close()



