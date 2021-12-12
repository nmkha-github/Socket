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
def convert_to_eng(text):   #chuyển tiếng việt có dấu thành không giấu viết hoa
    output = text
    for regex, replace in patterns.items():
        output = re.sub(regex, replace, output)
        #Trường hợp viết hoa
        output = re.sub(regex.upper(), replace.upper(), output)
    return output.upper()

# print(convert_to_eng('Thành phố Hồ chí Minh'))
#output: THANH PHO HO CHI MINH
