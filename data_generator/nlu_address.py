
from operator import itruediv, le
import re
import sqlite3
from sys import prefix
from matplotlib.pyplot import stem
from nltk.stem import SnowballStemmer
import textdistance

DB_NAME = 'krg_address.db'






        





patterns = [
            '[?a](address_name)',
            '[?a](address_name) [?d](house_number)',
            '[?a](address_name) [дом ?d](house_number)',
            '[?a](address_name) [дом ?d](house_number) [квартира ?p](apartment_number)',
            '[?a](address_name) [?d](house_number) [квартира ?p](apartment_number)',
            '[?a](address_name) [дом ?d](house_number) [?p квартира](apartment_number)',
            '[?a](address_name) [?d](house_number) [?p квартира](apartment_number)',
            '[?a](address_name) [?d](house_number) [?p](apartment_number)',
            '[?a](address_name) [?d дом](house_number) [?p](apartment_number)',
            '[?a](address_name) [?d дом](house_number) [?p квартира](apartment_number)',
            '[?a](address_name) [?d дом](house_number) [квартира ?p](apartment_number)',
  ]





patterns_apart = [
            '[квартира ?p](apartment_number)',
            '[?p квартира](apartment_number)',
            '[?p](apartment_number)'
  ]



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

def get_greet_from_nlu():
    res = read_data_from_txt('/Users/meirlen/Desktop/bot/y/data/nlu_address.yml')
    new_array = []
    for item in res:
        greet = item.split('[')[0].replace('-','').strip()
        if len(greet)>5 and greet!='переулок' and greet!='проспект' and greet!='квартира':
            new_array.append(greet)

    return new_array





from random import randint
import random


patterns_mkr_mkr = [
            '[?a](address_name) [дом ?d](house_number) [квартира ?p](apartment_number)',
            '[?a](address_name) [?d](house_number) [квартира ?p](apartment_number)',
            '[?a](address_name) [дом ?d](house_number) [?p квартира](apartment_number)',
            '[?a](address_name) [?d](house_number) [?p квартира](apartment_number)',
            '[?a](address_name) [?d](house_number) [?p](apartment_number)',
            '[?a](address_name) [?d дом](house_number) [?p](apartment_number)',
            '[?a](address_name) [?d дом](house_number) [?p квартира](apartment_number)',
            '[?a](address_name) [?d дом](house_number) [квартира ?p](apartment_number)',
            '[?a](address_name) [?d](house_number) [?p](apartment_number)',
            '[?a](address_name) [?d](house_number) [?p](apartment_number)',
            '[?a](address_name) [?d](house_number) [?p](apartment_number)',
            '[?a](address_name) [?d](house_number) [?p](apartment_number)',
            '[?a](address_name) [?d](house_number) [?p](apartment_number)',
            '[?a](address_name) [?d](house_number) [?p](apartment_number)',
            '[?a](address_name) [?d](house_number) [?p](apartment_number)',
            '[?a](address_name) [?d](house_number) [?p](apartment_number)',
            '[?a](address_name) [?d](house_number) [?p](apartment_number)',
            '[?a](address_name) [?d](house_number) [?p](apartment_number)',

  ]

patterns_mkr_mkr_to = [
            '[?a](address_name) [дом ?d](house_number) [квартира ?p](apartment_number)',
            '[?a](address_name) [?d](house_number) [квартира ?p](apartment_number)',
            '[?a](address_name) [дом ?d](house_number) [?p квартира](apartment_number)',
            '[?a](address_name) [?d](house_number) [?p квартира](apartment_number)',
            '[?a](address_name) [?d](house_number) [?p](apartment_number)',
            '[?a](address_name) [?d дом](house_number) [?p](apartment_number)',
            '[?a](address_name) [?d дом](house_number) [?p квартира](apartment_number)',
            '[?a](address_name) [?d дом](house_number) [квартира ?p](apartment_number)',
            '[?a](address_name)',
            '[?a](address_name)',
            '[?a](address_name)',
            '[?a](address_name)',
            '[?a](address_name)',
            '[?a](address_name)',
            '[?a](address_name)',
            '[?a](address_name) [?d](house_number)',
            '[?a](address_name) [?d](house_number)',
            '[?a](address_name) [?d](house_number)',

  ]



# 13 14 12 поедем , в на 15 15 15 bi_direct
# 13 14 12 поедем , в на 15 15  bi_direct
# 13 14 12 поедем , в на 15  bi_direct


greet_array = get_greet_from_nlu()
prefix_array = ['на','в','','','','','','','','','','','','едем','поеду','поедем']
mkr_array = ['11','11а','12','13','14','15','16','17','18','19','21','22','21','1','2']
prefix_mkr_array = [' микрорайон',' мкрн',' мкр',' мик',' район',' микрарайон',' квартал','','','','','','','','','','','','','','','','','','']
prefix_house_array = ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','а','б','в','г','д','',]

# for i in range(100):
#     from_mkr = random.choice(mkr_array)+random.choice(prefix_mkr_array)
#     to_mkr = random.choice(mkr_array)
#     prefix = random.choice(prefix_array)

#     house_number = str(randint(0, 50))+random.choice(prefix_house_array)
#     apart_number = str(randint(0, 200))


#     to_house_number = str(randint(0, 50))+random.choice(prefix_house_array)
#     to_apart_number = str(randint(0, 200))

#     greet = random.choice(greet_array)

#     if from_mkr != to_mkr:
#         from_pattern = random.choice(patterns_mkr_mkr)
#         from_addr = from_pattern.replace('?a',from_mkr).replace('?d', house_number).replace('?p', apart_number)
#         from_addr = from_addr.replace('(address_name)','{"entity": "address_name", "role": "from"}')

#         to_pattern = random.choice(patterns_mkr_mkr_to)
#         to_addr = to_pattern.replace('?a',to_mkr).replace('?d', to_house_number).replace('?p', to_apart_number)
#         to_addr = to_addr.replace('(address_name)','{"entity": "address_name", "role": "to"}')
#         # sentence = greet +' '+from_addr+' '+prefix+' ' +to_addr
#         sentence = from_addr+' '+prefix+' ' +to_addr
#         # add_data_to_txt('    - '+sentence,'/Users/meirlen/Desktop/bot/y/data_generator/new_data/nlu_mkr_mkr.yml')

#         # print(sentence)



# # 12 13 поеду на 16"
# # 12 13 45 на 16




patterns_mkr_mkr_2 = [
            '[?a](address_name) [дом ?d](house_number) ',
            '[?a](address_name) [?d](house_number) ',
            '[?a](address_name) [дом ?d](house_number) ',
            '[?a](address_name) [?d](house_number) ',
            '[?a](address_name) [?d](house_number)',
            '[?a](address_name) [?d дом](house_number)',
            '[?a](address_name) [?d дом](house_number) ',
            '[?a](address_name) [?d дом](house_number) ',
      

  ]

patterns_mkr_mkr_to_2 = [
            '[?a](address_name) '
 

  ]


for i in range(150):
    from_mkr = random.choice(mkr_array)+random.choice(prefix_mkr_array)
    to_mkr = random.choice(mkr_array)
    prefix_array = ["поеду","едем","еду","нужно на","надо в"]

    house_number = str(randint(0, 50))+random.choice(prefix_house_array)
    apart_number = str(randint(0, 200))


    to_house_number = str(randint(0, 50))+random.choice(prefix_house_array)
    to_apart_number = str(randint(0, 200))

    if from_mkr != to_mkr:
        from_pattern = random.choice(patterns_mkr_mkr_2)
        from_addr = from_pattern.replace('?a',from_mkr).replace('?d', house_number).replace('?p', apart_number)
        from_addr = from_addr.replace('(address_name)','{"entity": "address_name", "role": "from"}')
        prefix = random.choice(prefix_array)
        to_pattern = random.choice(patterns_mkr_mkr_to_2)
        to_addr = to_pattern.replace('?a',to_mkr).replace('?d', to_house_number).replace('?p', to_apart_number)
        to_addr = to_addr.replace('(address_name)','{"entity": "address_name", "role": "to"}')

        greet = random.choice(greet_array)
        
        sentence = greet +' '+from_addr+' '+prefix+' ' +to_addr

        # print(sentence)
        add_data_to_txt('    - '+sentence,'/Users/meirlen/Desktop/bot/y/data_generator/new_data/nlu_mkr_mkr.yml')




# # Street
# res = read_data_from_txt('/Users/meirlen/Desktop/bot/y/data_generator/new_data/nlu_address_undefined.yml')
# for item in res:
#     if "house_number" in item:
#         first_part,second_part = item.split('(house_number)')
#         second_part = second_part.replace('{"entity": "address_name" , "role": "org"}','{"entity": "address_name" , "role": "to"}')
#         first_part = first_part.replace('{"entity": "address_name" , "role": "street"}','{"entity": "address_name" , "role": "from"}')
#         first_part = first_part+'(house_number)'

#         apart_pattern = random.choice(patterns_apart)
#         apart_number = str(randint(0, 500))

#         apart_number = apart_pattern.replace('?p',str(apart_number))
#         sentence = first_part+' '+apart_number+' '+second_part


#         add_data_to_txt('    '+sentence,'/Users/meirlen/Desktop/bot/y/data_generator/new_data/nlu_street_org.yml')


# #-------------------



# Street
# res = read_data_from_txt('/Users/meirlen/Desktop/bot/y/data_generator/new_data/street.txt')
# res_street = read_data_from_txt('/Users/meirlen/Desktop/bot/y/data_generator/new_data/nlu_address.yml')
# street_clear_res = []
# for item in res_street:
#     if "house_number" in item or "apartment_number" in item:
#         street_clear_res.append(item)
#         # print(item)


from random import randint

# def generate_adress(address, pattern):

#       house_number = str(randint(0, 200))
#       apart_number = str(randint(0, 500))
#       address = pattern.replace('?a', address).replace('?d', house_number).replace('?p', apart_number)

#       return address.strip()

# import random



# for street in res:
#     street_clear_res.append("- ["+street+'](address_name)')

# # street_clear_res = res + street_clear_res

# prefix_array = ['на','в','','едем','поеду']

# for i in range(2000):
#     from_a =  random.choice(street_clear_res).replace('(address_name)','{"entity": "address_name", "role": "from"}')
#     to_a = random.choice(res)
#     prefix = random.choice(prefix_array)

#     pattern = random.choice(patterns)
#     to_a = generate_adress(to_a,pattern).replace('(address_name)','{"entity": "address_name", "role": "to"}')
#     # print(from_a + ' '+prefix+" " +to_a)
#     sentence = from_a + ' '+prefix+" " +to_a

#     add_data_to_txt('    '+sentence,'/Users/meirlen/Desktop/bot/y/data_generator/new_data/nlu_street_street.yml')









# for item in res:
#     if "org" in item:
#         add_data_to_txt('    '+item,'/Users/meirlen/Desktop/bot/y/data_generator/new_data/nlu_address_undefined2.yml')



# for item in res:
#     if "street" in item and "org" in item:
#         add_data_to_txt('    '+item,'/Users/meirlen/Desktop/bot/y/data_generator/new_data/nlu_address_undefined.yml')
#     else:
#         if 'macro_area' not in  item and 'street' not in item and 'org' not in item:   
#             add_data_to_txt('    '+item,'/Users/meirlen/Desktop/bot/y/data_generator/new_data/nlu_address.yml')


# street = []
# for item in res:
#     if  "house_number" in item:
#         print(item ) 




#     local_results = (search_by_levenshtein_distance(
#             address_name, total_res))
#     if len(local_results) == 0:
#        not_found_addrs.append(address_name)
#     if len(local_results) == 1:
#        found_1_addrs.append(address_name+'  $$  '+str(local_results[0]))
#     if len(local_results) == 2:
#        found_2_addrs.append(address_name+'  $$  '+str(local_results[0])+'  $$  '+str(local_results[1]))



# path = '/Users/meirlen/Desktop/bot/dataset/test/alem_data/orgs_result_street.txt'
# add_data_to_txt('Not found',path)
# for item in not_found_addrs:
#     add_data_to_txt(item,path)


# print('FOUND 1 ADDRESS',len(found_1_addrs)) 
# add_data_to_txt('\nFOUND 1 ADDRESS',path)
# for item in found_1_addrs:
#     add_data_to_txt(item,path)


# print('FOUND 2 ADDRESS',len(found_2_addrs)) 
# add_data_to_txt('\nFOUND 2 ADDRESS',path)
# for item in found_2_addrs:
#     add_data_to_txt(item,path)


# print('NOT FOUND',len(not_found_addrs)) 
# print('1 found',len(found_1_addrs))  
# print('2 found',len(found_2_addrs))      