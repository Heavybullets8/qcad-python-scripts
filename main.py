import os
from general_tubes import *
from sliders import *
from test import *


print("1) General Tubes")
print("2) Sliders")
print("3) Testing")
print()

tube_type = ""
while tube_type not in [1,2,3]:
    tube_type = int(input("What type of blueprint are you making?(1 or 2): "))
    if tube_type == 1:
        general_tubes()
    elif tube_type == 2:
        sliders()
    elif tube_type == 3:
        testing()
    else: 
        print("Error: {tube_type} was not an option, try again..".format(tube_type=tube_type))


os.system('qcad -exec {pwd}/box_maker.js 1>/dev/null'.format(pwd=os.getcwd()))
