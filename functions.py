from functions import *
import os
from tabulate import tabulate


def convert_to_float(frac_str):
    if "\'" in frac_str:
        temp = frac_str.replace("\'", '')
        return int(temp) * 12
    elif "\"" in frac_str:
        frac_str = frac_str.replace("\"", '')
    
    try:
        return float(frac_str)
    except ValueError:
        try:
            num, denom = frac_str.split('/')
        except ValueError:
            return None
        try:
            leading, num = num.split(' ')
        except ValueError:
            return float(num) / float(denom)        
        if float(leading) < 0:
            sign_mult = -1
        else:
            sign_mult = 1
        return float(leading) + sign_mult * (float(num) / float(denom))


#refresh table
def refresh(multi_number,lengths,widths,total_tubes,hole_rads,hole_count):
    os.system('clear -x')
    
    for i in range(multi_number):
        print("Tube      {i}".format(i=i+1))
        
        if type(lengths) == str:
            print("Length:   x")
        else:
            print("Length:   {length}".format(length=lengths[i]))
        
        if type(widths) == str:
            print("Width:    x")
        else:    
            print("Width:    {width}".format(width=widths[i]))
            
        if type(total_tubes) == str:
            print("Tubes:    x")
        else:
            print("Tubes:    {total_tubes}".format(total_tubes=total_tubes[i]))
    
        if type(hole_rads) == str:
            print("Diameter: x")
        else:
            print("Diameter: {hole_rad}".format(hole_rad=hole_rads[i]))

        if type(hole_count) == str:
            print("Holes:    x\n")
        else:
            print("Holes:    {hole_count}\n".format(hole_count=hole_count[i]))


# User Input Yes or No Function
def yesno_func(user_input):
    yesno = ""
    while yesno not in ["y","Y","n","N"]:
        yesno = input(user_input)
        if yesno in ["y","Y"]:
            return False
        elif yesno in ["n","N"]:
            return True
        else:
            print("Invalid input, please try again..")


# Constants Function
def constants(): 
    with open("box_maker.js","w") as file:
        # Create Javascript Perimeter function (boxes)
        file.write("function drawRectangle(width, height, x, y){\n \
        addLine(x, y, x, y + height);\n \
        addLine(x, y, x + width, y);\n \
        addLine(x + width, y, x + width, y + height);\n \
        addLine(x, y + height, x + width, y + height);\n}\n\n")

        # Create Javascript Holes function
        file.write("function drawCircle(x,y,size){\n \
        addCircle(x,y,size);\n}\n")
        

        # Add layers
        file.write('addLayer("Holes", "cyan", "CONTINUOUS", RLineweight.Weight025);\n')
        file.write('addLayer("Holes_Ref", "gray", "CONTINUOUS", RLineweight.Weight025);\n')
        file.write('addLayer("Perimeter", "red", "DASHED", RLineweight.Weight025);\n\n')
        

# Drawing Function
def draw_func(length,width,x,tubes,number,rad,tube_count,corners,manual_mode,y_offset):
    with open("box_maker.js","a") as file:
        excess = 0
        prior_excess = 0
        for i in range(tubes):

            # Draw Rectangle
            file.write('setCurrentLayer("Perimeter");\n')
            if manual_mode == True:
                excess = convert_to_float(input("What is the excess of tube {tube_count}?: ".format(tube_count=tube_count)))
                
                # If there was no change, do not add the excess
                if excess == prior_excess:
                    excess = 0

                # Remove excess from the previous exess, avoiding doubling up widths
                if excess > prior_excess:
                    excess = excess - prior_excess
                
            file.write("drawRectangle({width},{length},{x},0);\n".format(width=width,length=length,x=x+excess))


            # Draw Holes
            count = 0
            floor = 1
            roof = 1
            original_offset = y_offset
            file.write('setCurrentLayer("Holes");\n')
            for hole in range(number):
                location = length/(number+1)
                count+=1
                # If hole location exceeds plasma table length, set a different layer thats ignored in sheetcam
                if location*count > 118:
                    file.write('setCurrentLayer("Holes_Ref");\n')
                
                if corners == True:
                    current_width = x+1+excess
                else:
                    current_width = x+(width/2)+excess
                    
                    
                               
                # Odd number of holes per tube
                if (number % 2) != 0:
                    if hole == 0:
                        file.write("drawCircle({current_width},6,{rad});\n".format(current_width=current_width,rad=rad))
                    # Last row of holes end up 6 inches from the top
                    elif hole == number-1:
                        file.write("drawCircle({current_width},{length},{rad});\n".format(current_width=current_width,length=length-6,rad=rad))
                    # Middle of the tube
                    elif hole + .5 == number/2:
                        file.write("drawCircle({current_width},{length},{rad});\n".format(current_width=current_width,length=length/2,rad=rad))
                    # Lower half of the length
                    elif hole+1 < number/2:
                        file.write("drawCircle({current_width},{math},{rad});\n".format(current_width=current_width,math=(((length/2))/((number/2)-0.5)*floor-abs(y_offset)),rad=rad))
                        floor+=1
                    # Upper half of the length
                    elif count >= number/2:
                        file.write("drawCircle({current_width},{math},{rad});\n".format(current_width=current_width,math=((length/2))/((number/2)-0.5)*roof+length/2+abs(y_offset),rad=rad))
                        roof+=1


                # Even number of holes per tube
                else:
                    if count >= number/2:
                        y_offset = y_offset * -1
                    else:
                        y_offset = abs(y_offset)
                    
                    
                    
                    if hole == 0:
                        file.write("drawCircle({current_width},6,{rad});\n".format(current_width=current_width,rad=rad))
                    # Last row of holes end up 6 inches from the top
                    elif hole == number-1:
                        file.write("drawCircle({current_width},{length},{rad});\n".format(current_width=current_width,length=length-6,rad=rad))
                    # Draw Holes
                    else:
                        file.write("drawCircle({current_width},{math},{rad});\n".format(current_width=current_width,math=((length)/(number-1))*hole+y_offset,rad=rad))

            tube_count+=1
            x = x + float(width)
    return x, count



def auto_holes_func(lengths):
    hole_count = []
    for length in lengths:
        if length < 108:
            hole_count.append(2)
        elif length < 168:
            hole_count.append(3)
        elif length < 216:
            hole_count.append(4)
        elif length < 230:
            hole_count.append(5)
        else: 
            hole_count.append(6)
    return hole_count




def dry_run_func(length,width,number,rad,tube_count):
    y_offset = 0
    offsets = []
    prev_offset = 0

    hole_location = []
    count = 0
    floor = 1
    roof = 1

    
    for hole in range(number):
        count+=1
            
        # Odd number of holes per tube
        if (number % 2) != 0:
            if hole == 0:
                hole_location.append(6)
            elif hole == number-1:
                hole_location.append(length-6)
            elif hole + .5 == number/2:
                hole_location.append(length/2)
            elif hole+1 < number/2:
                hole_location.append((length/2)/((number/2)-0.5)*floor-abs(y_offset))
                floor+=1
            # Upper half of the length
            elif count >= number/2:
                hole_location.append((length/2)/((number/2)-0.5)*roof+length/2+abs(y_offset))
                roof+=1


        # Even number of holes per tube
        else:
            
            if hole == 0:
                hole_location.append(6)
            # Last row of holes end up 6 inches from the top
            elif hole == number-1:
                hole_location.append(length-6)
            # Draw Holes
            else:
                if count >= number/2:
                    temp = y_offset * -1
                else:
                    temp = abs(y_offset)
                                                        
                hole_location.append((length/(number-1))*hole+temp)
                    
         
    y_offset = hole_check_func(hole_location, rad)
    
    
    if y_offset != 0:
        print("The holes were offset, so that they are not touching the 4ft centers:\
            \n43-49\n91-97\n139-145\n189-193\n235-241\
            \nYou should double check that holes are not touching these numbers, and are spaced well..")
        print("Current Offset:",y_offset)
        
    return y_offset
            
 
    



def hole_check_func(numbers,rad):
    pos_offset = 0
    neg_offset = 0
    temp_offset = 0
    finished = False
    
    count = 0
    while count != len(numbers):
        count = 0
        for number in numbers:
            
            if count < len(numbers)/2:
                temp_offset = abs(neg_offset) 
            else:
                temp_offset = neg_offset
            
            # If hole lands on a 4 foot center, or close to it, return a relocation value, where it'll be clear
            if 43-(rad/2) <= number+temp_offset <= 49+(rad/2) or \
                91-(rad/2) <= number+temp_offset  <= 97+(rad/2) or \
                139-(rad/2) <= number+temp_offset  <= 145+(rad/2) or \
                189-(rad/2) <= number+temp_offset  <= 193+(rad/2) or \
                235-(rad/2) <= number+temp_offset  <= 241+(rad/2):
                    # If 4 ft center collision occurs on the middle hole, exit
                    if len(numbers) % 2 != 0 and count+0.5 == len(numbers):
                        print("Impossible to use an odd number for this length tube.. Exiting")
                        exit()
                    else:
                        neg_offset-=1
                        continue
            else:
                count+=1

            

    count = 0
    while count != len(numbers):
        count = 0
        for number in numbers:

            if count < len(numbers)/2:
                temp_offset = pos_offset * -1
            else:
                temp_offset = abs(pos_offset) 
            
            # If hole lands on a 4 foot center, or close to it, return a relocation value, where it'll be clear
            if 43-(rad/2) <= number+temp_offset <= 49+(rad/2) or \
                91-(rad/2) <= number+temp_offset  <= 97+(rad/2) or \
                139-(rad/2) <= number+temp_offset  <= 145+(rad/2) or \
                189-(rad/2) <= number+temp_offset  <= 193+(rad/2) or \
                235-(rad/2) <= number+temp_offset  <= 241+(rad/2):
                    # If 4 ft center collision occurs on the middle hole, exit
                    if len(numbers) % 2 != 0 and count+0.5 == len(numbers):
                        print("Impossible to use an odd number for this length tube.. Exiting")
                        exit()
                    else:
                        pos_offset+=1
                        continue
            else:
                count+=1
                 
             
    # Return whichever value is lowest, ensuring the least amount of deviation possible
    if abs(neg_offset) > abs(pos_offset):
        return pos_offset
    else:
        return neg_offset
        
        
        
        
