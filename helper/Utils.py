

import re
import string
# this fun used for telegram,whatsapp input channel
def pre_proccess_text(text):
    x =  re.search("\d{1,2}\/\d{1,2}", text)
    if x:
        text = text.replace('/',' дробь ')
    text = re.sub(r"([0-9]+(\.[0-9]+)?)",r" \1 ", text).strip().replace(' , ',',') # add space after digit. For instance:  16мкр 8дом = 16 мкр 8 дом
    text = text.lower()
    translator = str.maketrans(string.punctuation, ' '*len(string.punctuation)) #map punctuation to space
    text = text.translate(translator)
    return text.replace('  ',' ')
    

def add_data_to_txt(contents,file_path):
        file = open(file_path,"a")
        file.writelines(contents+'\n')
        file.close()  


def read_data_from_txt(file_path):
     with open(file_path) as f:
           lines = f.readlines()
     result = []
     for line in lines:
         result.append(line.strip())
     print(len(result)) 
     return  result        


def phone_number_validate(number):
    # if number == None:
    #    return
    # number = str(number)
    number = re.sub('\D', '', number.lower())
    number = number.replace(' ', '').strip()
    result = re.match(
        r'^^(\+7|7|8)?7(\d{9})$', number)

    if bool(result):
        if number.startswith('8')  or number.startswith('7'):
           number = '+7'+  number[1:]
        if len(number) == 12: 
          return number
        else:
          return None  
    else:
        return None

def address_text_pre_proccess(text):

    word_count = len(text.split())
    
    if word_count == 2:
        text = text.strip()
        text = text.translate(str.maketrans('', '', string.punctuation))
        case_1 = re.search("\d{1,4}", text)
        if bool(case_1):
            text = re.sub('микрорайон|мкрн|мкр|мик|район|микрарайон|ый|квартал', '', text)

        
    return text.strip()


from actions.app_constans import *

def is_template_message(text):
    return text.startswith(TEMPLATE_START_TEXT.lower())

def get_position_from_template_message(text):
    try:
       return text.split("№")[1].strip()   
    except:    
       return None


