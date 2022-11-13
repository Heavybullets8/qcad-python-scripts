import os
from general_tubes import *
from sliders import *


print("1) General Tubes")
print("2) Sliders")
print()

tube_type = ""
while tube_type not in [1,2]:
    tube_type = int(input("What type of blueprint are you making?(1 or 2): "))
    if tube_type == 1:
        general_tubes()
    elif tube_type == 2:
        sliders()
    else: 
        print("Error: "+str(tube_type)+" was not an option, try again..")


os.system('qcad -exec '+f"{os.getcwd()}"+'/box_maker.js')
