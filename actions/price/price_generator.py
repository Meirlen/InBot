from actions.app_constans import *
from local_db_for_actions import *
from actions.price.zone import search_coordinates

price_dict = {
        C+' '+C: '600',
        C+' '+M3: '1200',
        C+' '+M2: '1300',
        C+' '+M1: '1400',
        C+' '+P: '1400',
        C+' '+U: '900',
        C+' '+MI1: '750',
        C+' '+MI2: '800',
        C+' '+MI3: '900',
        C+' '+F1: '1000',
        C+' '+F2: '1200',
        C+' '+F3: '1500',
        C+' '+S: '2600',
        C+' '+R: '800',
        M3+' '+C: '1200',
        M2+' '+C: '1300',
        M1+' '+C: '1400',
        M3+' '+R: '1200',
        M2+' '+R: '1300',
        M1+' '+R: '1400',
        M3+' '+U: '1200',
        M2+' '+U: '1300',
        M1+' '+U: '1400',
        M3+' '+MI1: '1300',
        M2+' '+MI1: '1400',
        M1+' '+MI1: '1500',
        M3+' '+MI2: '1400',
        M2+' '+MI2: '1500',
        M1+' '+MI2: '1600',
        M3+' '+MI3: '1500',
        M2+' '+MI3: '1600',
        M1+' '+MI3: '1800',
        M3+' '+F1: '1400',
        M2+' '+F1: '1500',
        M1+' '+F1: '1600',
        M3+' '+F2: '1500',
        M2+' '+F2: '1600',
        M1+' '+F2: '1800',
        M3+' '+F3: '1600',
        M2+' '+F3: '1700',
        M1+' '+F3: '1800',
        M3+' '+P: '1500',
        M2+' '+P: '1300',
        M1+' '+P: '1300',
        M3+' '+S: '1400',
        M2+' '+S: '1500',
        M1+' '+S: '1600',
        M3+' '+M3: '500',
        M3+' '+M2: '600',
        M3+' '+M1: '700-750',
        M2+' '+M2: '500',
        M2+' '+M1: '600',
        M1+' '+M1: '500',
        P+' '+MI1: '1600',
        P+' '+MI2: '1600',
        P+' '+MI2: '1700',
        P+' '+F: '1700-1800',
        P+' '+S: '1600',
        P+' '+T: '2000',
        U+' '+C: '900',
        U+' '+P: '1700-1800',
        U+' '+U: '600',
        U+' '+MI1: '1000',
        U+' '+MI2: '1100',
        U+' '+MI3: '1200',
        U+' '+F1: '1000',
        U+' '+F2: '1200',
        U+' '+F3: '1500',
        U+' '+S: '2600',
        U+' '+M3: '1200',
        U+' '+M2: '1300',
        U+' '+M1: '1400',
        U+' '+R: '800',
        R+' '+R: '650',
        R+' '+MI1: '900',
        R+' '+MI2: '1000',
        R+' '+MI3: '1100',
        R+' '+F1: '700',
        R+' '+F2: '1000',
        R+' '+F3: '1200',
        R+' '+P: '1600',
        R+' '+S: '2600',
        MI1+' '+F1: '900',
        MI1+' '+F2: '1000',
        MI1+' '+F3: '1200',
        MI2+' '+F2: '1200',
        MI2+' '+F3: '1300',
        MI3+' '+F3: '1400',
        MI1+' '+S: '2700',
        MI2+' '+S: '2700',
        MI3+' '+S: '2800',
        MI+' '+T: '2800',
        MI1+' '+MI1: '650',
        MI1+' '+MI2: '750',
        MI1+' '+MI3: '900',
        MI2+' '+MI2: '650',
        MI2+' '+MI3: '750',
        MI3+' '+MI3: '800',
        F+' '+S: '2800-3000',
        F+' '+T: '2700-3000',
        F1+' '+F1: '650',
        F1+' '+F2: '750',
        F1+' '+F3: '950',
        F2+' '+F2: '650',
        F2+' '+F3: '750',
        F3+' '+F3: '800',
        HMK+' '+C: '900',
        HMK+' '+P: '1700',
        HMK+' '+U: '900',
        HMK+' '+MI1: '1000',
        HMK+' '+MI2: '1100',
        HMK+' '+MI3: '1200',
        HMK+' '+F1: '1000',
        HMK+' '+F2: '1200',
        HMK+' '+F3: '1400',
        HMK+' '+S: '2600',
        HMK+' '+M3: '1200',
        HMK+' '+M2: '1300',
        HMK+' '+M1: '1400',
        HMK+' '+R: '800',
        T+' '+M3: '3000',
        T+' '+M2: '3000',
        T+' '+M1: '3000',
        T+' '+P: '2000',
        T+' '+U: '3000',
        T+' '+MI1: '2600',
        T+' '+MI2: '2600',
        T+' '+MI3: '2600',
        T+' '+F1: '3000',
        T+' '+F2: '3000',
        T+' '+F3: '3000',
        T+' '+C: '2600',
        T+' '+S: '4000',
        T+' '+R: '2800',
        T+' '+HMK: '3000',
}



def calculate_price(from_address,from_house_number,to_address,to_house_number):
        print('calculate_price',from_address,' ', to_address)

        from_zone = search_coordinates(from_address,from_house_number)
        print(from_zone)
        if from_zone == None:
           return None 
        to_zone = search_coordinates(to_address,to_house_number)
        if to_zone == None:
           return None 

        print(from_zone,'  ',to_zone)



        price = None
        
        try:
            price = price_dict[from_zone+" "+to_zone]
            price = price + '₸ ('+from_zone +' → '+to_zone+')'
            return price
        except:
            price = None

        try:
            price = price_dict[to_zone+" "+from_zone]
            price = price + '₸ ('+from_zone +' → '+to_zone+')'
            return price
        except:
            price = None


        return price



# def calculate_price_by_coord(from_zone,to_zone):

#         if from_zone == None:
#            return None 
#         if to_zone == None:
#            return None 

#         price = None

        
#         try:
#             price = price_dict[from_zone+" "+to_zone]
#             price = price + '₸ ('+from_zone +' → '+to_zone+')'
#             return price
#         except:
#             price = None

#         try:
#             price = price_dict[to_zone+" "+from_zone]
#             price = price + '₸ ('+from_zone +' → '+to_zone+')'
#             return price
#         except:
#             price = None

#         return price




    
    


 
 


# print(calculate_price(''+M1,''+C))
