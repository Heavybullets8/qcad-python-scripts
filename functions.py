import os
import re


def convert_to_float(frac_str):
    while True:
        # Check for inches or feet
        if "\'" in frac_str:
            return int(frac_str.replace("\'", '')) * 12
        elif "\"" in frac_str:
            return int(frac_str.replace("\"", ''))
        
        # Check for mixed numbers
        mixed_number_pattern = r"(-?\d+)\s(-?\d+)/(-?\d+)"
        mixed_number_match = re.fullmatch(mixed_number_pattern, frac_str)
        if mixed_number_match:
            whole, num, denom = map(int, mixed_number_match.groups())
            return whole + num / denom
        
        # Check for fractions
        fraction_pattern = r"(-?\d+)/(-?\d+)"
        fraction_match = re.fullmatch(fraction_pattern, frac_str)
        if fraction_match:
            num, denom = map(int, fraction_match.groups())
            return num / denom
        
        # Try to parse as float or integer
        try:
            return float(frac_str)
        except ValueError:
            try:
                return int(frac_str)
            except ValueError:
                frac_str = input("Invalid input, please enter a whole number, mixed number, fraction, or decimal: ")
                continue



# Int Check
def int_check(user_input):
    while True:
        try:
            return int(user_input)
        except ValueError:
            print("Please type a whole number..")
            user_input = input("Input: ")




def refresh(multi_number, lengths, widths, total_tubes, hole_rads, hole_count):
    os.system('clear -x')

    for i in range(multi_number):
        print("Tube      {}".format(i + 1))
        
        if isinstance(lengths, list):
            print("Length:   {}".format(lengths[i]))
        else:
            print("Length:   x")
        
        if isinstance(widths, list):
            print("Width:    {}".format(widths[i]))
        else:
            print("Width:    x")
        
        if isinstance(total_tubes, list):
            print("Tubes:    {}".format(total_tubes[i]))
        else:
            print("Tubes:    x")
        
        if isinstance(hole_rads, list):
            print("Diameter: {}".format(hole_rads[i]))
        else:
            print("Diameter: x")
        
        if isinstance(hole_count, list):
            print("Holes:    {}\n".format(hole_count[i]))
        else:
            print("Holes:    x\n")


def yesno_func(user_input):
    while True:
        response = input(user_input).lower()
        if response == 'y':
            return False
        elif response == 'n':
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

    # Reverse the list
    reversed_list = list(reversed(y_offset))

    # Negate each element in the reversed list
    inverse_list = [-x for x in reversed_list]

    # Append the inverse list to y_offset
    y_offset.extend(inverse_list)

    if number % 2 == 1:  # Check if number is odd
        y_offset.insert(len(y_offset) // 2, 0)  # Insert 0 at the middle of the list


    print("y_offset: {}".format(y_offset))
    with open("box_maker.js","a") as file:
        excess = 0
        prior_excess = 0
        for i in range(tubes):

            # Draw Rectangle
            file.write('setCurrentLayer("Perimeter");\n')
            if manual_mode == True:
                excess = convert_to_float(input("What is the excess (to the left) of tube {tube_count}?: ".format(tube_count=tube_count)))
                if excess == None:
                    excess = prior_excess
                
                # If there was no change, do not add the excess
                if excess == prior_excess:
                    excess = 0

                # Remove excess from the previous exess, avoiding doubling up widths
                if excess > prior_excess:
                    excess = excess - prior_excess
                    prior_excess = excess
                
                
            file.write("drawRectangle({width},{length},{x},0);\n".format(width=width,length=length,x=x+excess))


            # Draw Holes
            count = 0
            floor = 1
            roof = 1
            y_offset_count = 0
            print (range(number))
            for hole in range(number):
                y_offset1 = y_offset[y_offset_count]
                print("y_offset1: {}".format(y_offset1))
                count+=1
                # If hole location exceeds plasma table length, set a different layer thats ignored in sheetcam
                
                if corners == True:
                    current_width = x+1+excess
                else:
                    current_width = x+(width/2)+excess
                    
                               
                # Odd number of holes per tube
                if (number % 2) != 0:
                    if hole == 0:
                        math = 6
                    # Last row of holes end up 6 inches from the top
                    elif hole == number-1:
                        math = length-6
                    # Middle of the tube
                    elif hole + .5 == number/2:
                        math = length/2
                    # Lower half of the length
                    elif hole+1 < number/2:
                        math = (((length/2))/((number/2)-0.5)*floor-abs(y_offset1))
                        floor+=1
                    # Upper half of the length
                    elif count >= number/2:
                        math = ((length/2))/((number/2)-0.5)*roof+length/2+abs(y_offset1)
                        roof+=1
                    
                    
                # Even number of holes per tube
                else:

                    if hole == 0:
                        math = 6
                    # Last row of holes end up 6 inches from the top
                    elif hole == number-1:
                        math = length-6
                    # Draw Holes between the two 6 inch hard coded holes
                    else:
                        math = ((length)/(number-1))*hole+y_offset1
                
                # If target hole exceeds limits of plasma table, mark them for reference, so theyre not cut out
                if math > 118:
                    file.write('setCurrentLayer("Holes_Ref");\n')
                else:
                    file.write('setCurrentLayer("Holes");\n')
                
                file.write("drawCircle({current_width},{math},{rad});\n".format(current_width=current_width,math=math,rad=rad))
                
                y_offset_count+=1  # Increment the counter


                
            tube_count+=1
            x = x + float(width) + excess
    return x, count



def auto_holes_func(lengths):
    hole_count = []
    for length in lengths:
        if length < 108:
            holes = 2
        elif length < 168:
            holes = 3
        elif length < 216:
            holes = 4
        elif length < 230:
            holes = 5
        else:
            holes = 6
        hole_count.append(holes)
    return hole_count




def dry_run_func(length,number,rad):
    y_offset = 0
    hole_location = []
    count = 0
    floor = 1
    roof = 1

    
    for hole in range(number):
        count+=1
            
        # Odd number of holes per tube
        if (number % 2) != 0:
            if hole == 0 or hole == number-1:
                continue
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
            
            if hole == 0 or hole == number-1:
                continue
            # Draw Holes
            else:
                if count >= number/2:
                    temp = y_offset * -1
                else:
                    temp = abs(y_offset)
                                                        
                hole_location.append((length/(number-1))*hole+temp)


    y_offset = [0]
    # Set the counter variables to 0 and the length of the list minus 1
    counter_a = 0
    counter_b = len(hole_location) - 1

    # Loop until the two counter variables meet in the middle of the list
    while counter_a < counter_b:
        print(hole_location[counter_a])
        print(hole_location[counter_b])
        y_offset.append(hole_check_func([hole_location[counter_a], hole_location[counter_b]], rad))


        print("Current Offset:",y_offset)
        # Increment the first counter variable and decrement the second one
        counter_a += 1
        counter_b -= 1

    # If the list has an odd number of elements, print the element in the middle
    if len(hole_location) % 2 != 0:
        print(hole_location[len(hole_location) // 2])
         

    return y_offset
            
 
    


def hole_check_func(numbers, rad):
    def check_collision(numbers):
        for number in numbers:
            # If hole lands on a 4 foot center, or close to it, return a relocation value, where it'll be clear
            if 43 - (rad / 2) <= number <= 49 + (rad / 2) or \
            91 - (rad / 2) <= number  <= 97 + (rad / 2) or \
            139 - (rad / 2) <= number  <= 145 + (rad / 2) or \
            189 - (rad / 2) <= number <= 193 + (rad / 2) or \
            235 - (rad / 2) <= number  <= 241 + (rad / 2):
                # If 4 ft center collision occurs on the middle hole, exit
                if len(numbers) % 2 != 0 and count + 0.5 == len(numbers) / 2:
                    print("Impossible to use an odd number for this length tube.. Exiting")
                    exit()
                else:
                    return True
        return False


    neg_offset = 0
    pos_offset = 0
    number1 = numbers[0]
    number2 = numbers[1]
    print("Checking:",number1,number2)


    print("positive")
    offset=0
    while check_collision([number1+offset, number2-offset]) == True:
        offset += 1
        print ([number1+offset, number2-offset])


    pos_offset = offset

    offset=0
    print("negaitve")
    while check_collision([number1-offset, number2+offset]) == True:
        offset += 1
        print ([number1-offset, number2+offset])
    neg_offset = offset



    print ("Positive Offset:",pos_offset)
    print ("Negative Offset:",neg_offset)


    # neg_offset = 0
    # pos_offset = 0
    # while True:
    #     count = 0
    #     for i, number in enumerate(numbers):
    #         if i < len(numbers) / 2:
    #             temp_offset = abs(neg_offset)
    #         else:
    #             temp_offset = neg_offset
    #         if not check_collision(number, temp_offset):
    #             count += 1
    #     if count == len(numbers):
    #         break
    #     neg_offset -= 1

    # while True:
    #     count = 0
    #     for i, number in enumerate(numbers):
    #         if i < len(numbers) / 2:
    #             temp_offset = pos_offset * -1
    #         else:
    #             temp_offset = abs(pos_offset)
    #         if not check_collision(number, temp_offset):
    #             count += 1
    #     if count == len(numbers):
    #         break
    #     pos_offset += 1
        
    # Return whichever value is lowest, ensuring the least amount of deviation possible
    if abs(neg_offset) > abs(pos_offset):
        return pos_offset
    else:
        return neg_offset
        
        
        
        
