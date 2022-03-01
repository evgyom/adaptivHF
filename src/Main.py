from Engine import *

engine = AdaptIOEngine("./gui/maps/base_field.txt",5,1.2,{"Teszt":"naivebot","Teszt1":"randombot","Teszt2":"randombot","Teszt3":"randombot"},5,"static")
for i in range(100):
    engine.tick()