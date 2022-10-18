from re import L
from shapely.geometry import Point, Polygon


# Let’s first create a Polygon using a list of coordinate-tuples and a couple of Point objects

def get_district(lat,lng):

   # Create Point objects
   p1 = Point(lat,lng)

    # Create a Polygon for Maikuduk
   coords_ma = [(49.92147, 73.16404), (49.90396, 73.25494), (49.80978, 73.21923), (49.841193, 73.133194)]
   poly_ma = Polygon(coords_ma)


   # Create a Polygon for Prishahtynsk
   coords_p = [(49.93322, 73.13826), (49.84818, 73.10986), (49.83427, 72.92002), (49.95961, 72.98207)]
   poly_p = Polygon(coords_p)


   # Create a Polygon for Ugo-vostok
   coords_u = [(49.767627, 73.118957),
            (49.769205, 73.120588),
            (49.777274, 73.120821),
            (49.778480, 73.118492),
            (49.785039, 73.127109),
            (49.782778, 73.130486),
            (49.804562, 73.163088),
            (49.796271, 73.175547),
            (49.789412, 73.169958),
            (49.784512, 73.177410),
            (49.782401, 73.178225),
            (49.781571, 73.170307),
            (49.775464, 73.155753),
            (49.754723, 73.164253),
            (49.752988, 73.141664)]
   poly_u = Polygon(coords_u)



   # Create a Polygon for Mihailovka
   coords_mi = [(49.829507, 73.068889),
            (49.814781, 73.079505),
            (49.812733, 73.073687),
            (49.809695, 73.072768),
            (49.792187, 73.066746),
            (49.792187, 73.066746),
            (49.787363, 73.035308),
            (49.823564, 73.038268)]

   poly_mi = Polygon(coords_mi)



   # Create a Polygon for Fedorovka
   coords_f = [(49.771792, 73.069155),
            (49.778079, 73.076156),
            (49.780384, 73.086676),
            (49.774247, 73.099672),
            (49.775550, 73.103269),
            (49.772821, 73.106892),
            (49.763405, 73.081938)]
            
   poly_f = Polygon(coords_f)



   # Create a Polygon for parent city
   coords_city = [(49.807536, 73.185469),
            (49.755344, 73.114428),
            (49.834348, 72.989652),
            (49.845245, 73.107597)]
            
   poly_city = Polygon(coords_city)

   
   if p1.within(poly_ma):
       return "майкудук"
   elif  p1.within(poly_p):
       return "пришахтинск"  
   elif  p1.within(poly_u):
       return "юг"  
   elif  p1.within(poly_ma):
       return "михайловка"  
   elif  p1.within(poly_f):
       return "федоровка"  
   elif  p1.within(poly_city):
       return "город"  
   else:
       return "город"  







    

