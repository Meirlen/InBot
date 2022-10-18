from local_db import select

areas = ['майкудук','город','пришахтинск','майкудук','майкудук','майкудук',]




def handle_2_address(address_1,address_2):
    print(address_1 +'  '+ address_2)

    # Найти тип To-do добавить ассинхронность и реализовать поиск через левенштейн расстояние
    print(select(address_1))
    print(select(address_2))


handle_2_address("корзина","юг")    