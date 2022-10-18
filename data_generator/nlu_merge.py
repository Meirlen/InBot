
from operator import add, itruediv, le
import re
import sqlite3
from sys import prefix
from matplotlib.pyplot import stem
from nltk.stem import SnowballStemmer
import textdistance

DB_NAME = 'krg_address.db'

def read_data_from_txt2(file_path):
     with open(file_path) as f:
           lines = f.readlines()
     result = []
     for line in lines:
        if str(line).startswith("    - "):
            result.append(line.strip())
     print(len(result)) 
     return  result        

def read_data_from_txt(file_path):
     with open(file_path) as f:
           lines = f.readlines()
     result = []
     for line in lines:
         result.append(line.strip())
     print(len(result)) 
     return  result  


def add_data_to_txt(contents,file_path):
        file = open(file_path,"a")
        file.writelines(contents+'\n')
        file.close()  

def get_order_res_from_nlu(path):
    res = read_data_from_txt(path)
    new_array = []
    for item in res:
        new_array.append(item)

    return new_array

def read_nlu(path):
    res = read_data_from_txt2(path)
    new_array = []
    for item in res:
         new_array.append(item)

    return new_array



from random import randint
import random



def nlu_parser(name_nlu, nlu_type_txt,repeat_count = 3):

    order_res_examples = get_order_res_from_nlu('/Users/meirlen/Desktop/bot/y/data_generator/new_data/'+nlu_type_txt)

    for i in range(repeat_count):
        
      address_examples = read_nlu('/Users/meirlen/Desktop/bot/y/data/'+name_nlu)

      for end in order_res_examples:
          start = random.choice(address_examples).replace('- ','')
          end = end.replace('- ','')
          if i == 1:
             sentence = start + ' '+end
          else:
             sentence = end+ ' '+start  
          add_data_to_txt('    - '+sentence,'/Users/meirlen/Desktop/bot/y/data_generator/new_data/'+name_nlu)


# # Order reservation
# nlu_parser("nlu_address.yml", "order_reservation_ents.txt")  # order reservation + address  
# nlu_parser("nlu_bi_direct.yml", "order_reservation_ents.txt")  # order reservation + bi address  
# nlu_parser("nlu_address_undefined.yml", "order_reservation_ents.txt")  # order reservation + address_undefined  


# Preferences
nlu_parser("nlu_address.yml", "prefernces.txt",5)  # prefernces + address  
nlu_parser("nlu_bi_direct.yml", "prefernces.txt",5)  # prefernces + bi address  
nlu_parser("nlu_address_undefined.yml", "prefernces.txt",5)  # prefernces + address_undefined  


# Preferences
