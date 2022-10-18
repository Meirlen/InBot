


from os import name
from local_db import insert

class DataItem:
  def __init__(self, name, area):
    self.name = name
    self.area = area

# READ FILE
# with open('/Users/meirlen/Desktop/bot/dataset/HELPER.txt') as f:
#      lines = f.readlines()


# adress_array = []
# for line in lines:
#    adress_array.append(line.replace("    -","").strip()+"\n")

# print(len(adress_array))        
# print(adress_array)

def generate_data_items():
      with open('/Users/meirlen/Desktop/bot/dataset/clear_data.txt') as f:
           lines = f.readlines()

      items = []

      for line in lines:
          parts = line.split("-")
          items.append(DataItem(parts[0],parts[1]))
                
      return items



def add_data_to_txt(contents,file_path):
    file = open(file_path,"a")
    file.writelines(contents)
    file.close()

#add_data_to_txt(adress_array,'/Users/meirlen/Desktop/bot/dataset/clear_data.txt')    


def add_items_to_db(items):
    
    for item in items:
        insert(item.name,0,item.area)
        print("Name "+item.name," Area "+item.area)


def add_items_to_nlu(items):
    
    for item in items:
        print("    - "+item.name)        



import re
def read_data():
    # READ FILE
    with open('/Users/meirlen/Desktop/bot/dataset/gas_station_data.txt') as f:
         lines = f.readlines()


    for line in lines:

        address = re.sub(r'[^\w]', ' ', line.strip().lower())
        print("    - "+ address)        

         #print("   ",line.lower().strip())  



#read_data()
# add_items_to_nlu(generate_data_items())
# print(len(generate_data_items()))
add_items_to_db(generate_data_items())