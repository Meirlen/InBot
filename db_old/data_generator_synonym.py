from os import replace
import sqlite3
import itertools
from itertools import combinations
from random import randrange

from random import randint
import random
from street_table import select_has_synonym
from data_generator_str import generate_adress_nlu
from data_generator_str import select
from data_generator_str import get_street
from data_generator_org import generate_org_key_loc
from data_generator_org import generate_org
from data_generator_str import patterns_street
from data_generator_str import change_entity_key_name
from data_generator_org import change_entity_key_name_for_org
from data_generator_street_info import generate_street_info_intent
DB_NAME = 'krg_address.db'


def add_data_to_txt(synonyms,name,file_path):
    file = open(file_path,"a")
    file.write("\n")
    file.write('- synonym: '+name+''+"\n")
    file.write('  examples: |'+"\n")
    file.writelines(synonyms)
    file.close()


result = select_has_synonym()
for item in result:
    name = item.split('^^')[0]
    synonyms = item.split('^^')[1].split(',')
    synonyms_array = []
    for s in synonyms:
        res = '    - '+s.strip()+"\n"
        synonyms_array.append(res)

    add_data_to_txt(synonyms_array,name,'/Users/meirlen/Desktop/bot/dataset/synonyms.txt')






