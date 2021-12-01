import json

def readDataByCountry(country_name):
    with open("dataAllCountry.json") as f_country:
        all_country_data = json.load(f_country)
    country_info = "None"
    for country in all_country_data:
        if(country_name.title() == country['country'].title()):
            country_info = "Country: "
            country_info += str(country['country']) + "\n"
            country_info += "Cases: "
            country_info += str(country['cases']) + "\n"
            country_info += "Cases today: "
            country_info += str(country['todayCases']) + "\n"
            country_info += "Deaths: "
            country_info += str(country['deaths']) + "\n"
            country_info += "Today deaths: "
            country_info += str(country['todayDeaths']) + "\n"
            country_info += "Recovered: "
            country_info += str(country['recovered']) + "\n"
            country_info += "Active: "
            country_info += str(country['active']) + "\n"
            country_info += "Critical: "
            country_info += str(country['critical']) + "\n"
            country_info += "Cases per one million: "
            country_info += str(country['casesPerOneMillion']) + "\n"
            country_info += "Deaths per one million: "
            country_info += str(country['deathsPerOneMillion']) + "\n"
            country_info += "Total test: "
            country_info += str(country['totalTests']) + "\n"
            country_info += "Test per one million: "
            country_info += str(country['testsPerOneMillion'])
    return country_info

def readDataInVN(province_name):
    with open("dataVN.json") as f_inVN:
        province_data = json.load(f_inVN)
    province_info = "None"
    for province in province_data:
        if province_name.title() == province['nameProvince']:
            province_info = "Province/City: "
            province_info += str(province['nameProvince']) + "\n"
            province_info += "Cases: "
            province_info += str(province['cases']) + "\n"
            province_info += "In progress treatment: "
            province_info += str(province['inProgress']) + "\n"
            province_info += "Another: "
            province_info += str(province['another'])+ "\n"
            province_info += "Recovered: "
            province_info += str(province['recovered']) + "\n"
            province_info += "Deaths: "
            province_info += str(province['deaths'])
    return province_info

def readNameProvinceInVN(name_short):
    with open("nameProvinceVN.json") as f_nameProvince:
        all_nameProvince_data = json.load(f_nameProvince)
    for nameProvince in all_nameProvince_data:
        if name_short.lower() == nameProvince["nameShort"].lower():
            if nameProvince["nameFull"].lower() == "thanh pho ho chi minh":
                return "TP. Ho Chi Minh"
            elif nameProvince["nameFull"].lower() == "thua thien hue":
                return "Thua Thien - Hue"
            else:
                return nameProvince["nameFull"]