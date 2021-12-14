patterns = {
    '[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
    '[đ]': 'd',
    '[èéẻẽẹêềếểễệ]': 'e',
    '[ìíỉĩị]': 'i',
    '[òóỏõọôồốổỗộơờớởỡợ]': 'o',
    '[ùúủũụưừứửữự]': 'u',
    '[ỳýỷỹỵ]': 'y'
}
import re
import json
import os
abspath = os.path.abspath(__file__) #Sửa lỗi path
dname = os.path.dirname(abspath)
os.chdir(dname)
def Upper(s): 
    if type(s) == type(u""):
        return s.upper()
    return unicode(s, "utf8").upper().encode("utf8")

def convert_to_eng(text):   #chuyển tiếng việt có dấu thành không giấu viết hoa
    output = text
    for regex, replace in patterns.items():
        output = re.sub(regex, replace, output)
        #Trường hợp viết hoa
        output = re.sub(regex.upper(), replace.upper(), output)
    return output.upper()

def check_del(token):
    for x in ['HUYEN', 'XA']:
        return True
    return False
def formatText(text):
    token=text.split()
    n=len(token)
    for i in range(n):
        if (check_del(token[i])):
            token[i] = ''
            break
        if (i > 0) and (convert_to_eng(token[i]) == 'PHO') and (convert_to_eng(token[i - 1]) == 'THANH'):
            token[i] = ''
            token[i - 1] = ''
            break
        if (convert_to_eng(token[i]) == 'HCM'):
            token[i] = 'TP. HỒ CHÍ MINH'
            break
        if(convert_to_eng(token[i])=='VN'):
            token[i]='CA NUOC'
            break
        if(i<len(token)-1 and convert_to_eng(token[i])=='VIET' and convert_to_eng(token[i+1])=='NAM'):
            token[i]='CA'
            token[i+1]='NUOC'
            break
        if(convert_to_eng(token[i])=='HUE'):
            token[i]='THUA THIEN HUE'
            break
        if(i<len(token)-1 and ((convert_to_eng(token[i])=='VUNG' and convert_to_eng(token[i+1])=='TAU') or (convert_to_eng(token[i])=='BA' and convert_to_eng(token[i+1])=='RIA'))):
            token[i]='BA RIA -'
            token[i+1]='VUNG TAU'
            break
    res=' '.join(token)
    fileViettat=os.getcwd() + '\data\\viettat.json'
    fii=open(fileViettat,"r",encoding="utf-8")
    data2=fii.read()
    data2=json.loads(data2)
    data2.sort(key = lambda x: len(x['abbreviation']), reverse=True)
    fii.close()
    for provinceData in data2:
        res=res.replace(provinceData['abbreviation'],provinceData['province'])
    return res
