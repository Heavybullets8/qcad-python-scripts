def testing():
    import os, threading
    x = 0
    count = 0
    lengths = "x"
    widths = "x"
    total_tubes = "x"
    hole_count = "x"
    hole_rads = "x"

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
    def refresh():
        os.system('clear -x')
        
        for i in range(multi_number):
            print(f"Tube      {i+1}")
            
            if type(lengths) == str:
                print(f"Length:   x")
            else:
                print(f"Length:   {lengths[i]}")
            
            if type(widths) == str:
                print(f"Width:    x")
            else:    
                print(f"Width:    {widths[i]}")
                
            if type(total_tubes) == str:
                print(f"Tubes:    x")
            else:
                print(f"Tubes:    {total_tubes[i]}")
        
            if type(hole_rads) == str:
                print(f"Diameter: x")
            else:
                print(f"Diameter: {hole_rads[i]}")

            if type(hole_count) == str:
                print(f"Holes:    x\n")
            else:
                print(f"Holes:    {hole_count[i]}\n")


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


    # Drawing Function
    def draw_func(length,width,x,tubes,number,rad,tube_count,corners):
        excess = 0
        prior_excess = 0
        for i in range(tubes):

            # Draw Rectangle
            file.write('setCurrentLayer("Perimeter");\n')
            if manual_mode == True:
                excess = convert_to_float(input(f"What is the excess of tube {tube_count}?: "))
                
                # If there was no change, do not add the excess
                if excess == prior_excess:
                    excess = 0

                # Remove excess from the previous exess, avoiding doubling up widths
                if excess > prior_excess:
                    excess = excess - prior_excess
                
            file.write(f"drawRectangle({width},{length},{x+excess},0);\n")

            # Draw Holes
            count = 0
            floor = 1
            roof = 1
            file.write('setCurrentLayer("Holes");\n')
            for hole in range(number):
                location = length/(number+1)
                count+=1
                # If hole location exceeds plasma table length, set a different layer thats ignored in sheetcam
                if location*count > 118:
                    file.write('setCurrentLayer("Holes_Ref");\n')
                
                # print("number",number)
                # print("hole", hole)
                # print("count", count)

                if corners == True:
                    # file.write(f"drawCircle({x+1+excess},{location*count},{rad});\n")
                    current_width = x+1+excess
                else:
                    current_width = x+(width/2)+excess
                    


                # Even number of holes per tube
                if (number % 2) != 0:
                    if hole == 0:
                        file.write(f"drawCircle({current_width},{6},{rad});\n")
                    # Last row of holes end up 6 inches from the top
                    elif hole == number-1:
                        file.write(f"drawCircle({current_width},{length-6},{rad});\n")
                    # Middle of the tube
                    elif hole + .5 == number/2:
                        file.write(f"drawCircle({current_width},{length/2},{rad});\n")
                    # Lower half of the length
                    elif hole+1 < number/2:
                        file.write(f"drawCircle({current_width},{((length/2))/((number/2)-0.5)*floor},{rad});\n")
                        floor+=1
                    # Upper half of the length
                    elif count >= number/2:
                        file.write(f"drawCircle({current_width},{((length/2))/((number/2)-0.5)*roof+length/2},{rad});\n")
                        roof+=1
                    else:
                        print(f"\nNo Trigger:\nHole: {hole+1}\nNumber:{number/2}")


                # Odd number of holes per tube
                else:
                    if hole == 0:
                        file.write(f"drawCircle({current_width},{6},{rad});\n")
                    # Last row of holes end up 6 inches from the top
                    elif hole == number-1:
                        file.write(f"drawCircle({current_width},{length-6},{rad});\n")
                    # Draw Holes
                    else:
                        if ((length)/(number-1))*(hole) > length/2:
                            file.write(f"drawCircle({current_width},{((length)/(number-1))*(hole)},{rad});\n")
                        else:
                            file.write(f"drawCircle({current_width},{((length)/(number-1))*(hole)},{rad});\n")
                        



            tube_count+=1
            x = x + float(width)
        return x, count


    os.system('clear -x')
    # Ask how many different types of tubes there are
    print("Note - Differences in tube is any change in width, or length of a tube")
    multi_number = int(input("How many different type of tube is there?: "))   
    refresh()


    lengths = []
    # Grab the length(s) of the tubes
    if multi_number > 1:
        for i in range(multi_number):
            temp = convert_to_float(input(f"Length of tube type #{i+1}: "))
            lengths.append(temp)
    else:
        temp = convert_to_float(input(f"Length of tube: "))
        lengths.append(temp)
    refresh()


    widths = []
    # Grab the width(s) of the tubes
    if multi_number > 1:
        for i in range(multi_number):
            temp = convert_to_float(input(f"Width of tube type #{i+1}: "))
            widths.append(temp)
    else:
        temp = convert_to_float(input(f"Width of tube?: "))
        widths.append(temp)
    refresh()


    # Ask how many tubes there are
    total_tubes = []
    for i in range(multi_number):
        temp = int(input(f"Number of tubes for #{i+1}: "))
        total_tubes.append(temp)
    refresh()
    
    
    # Ask if tubes will have the same hole size
    if multi_number > 1:
        hole_rads = []
        if yesno_func("Do the all of the tubes have the same hole size?(Y/n): ") == True:
            for i in range(multi_number):
                temp = convert_to_float(input(f"Hole size for tube #{i+1}: "))
                hole_rads.append(temp)
        else:
            temp = convert_to_float(input("Hole diameter: "))
            for i in range(multi_number):
                hole_rads.append(temp)
    else:
        hole_rads = [convert_to_float(input("Hole diameter: "))]
    refresh()


    # Ask how many holes per tube
    hole_count = []
    if multi_number > 1:
        holes = []
        for i in range(multi_number):
            temp = int(input(f"Amount of holes for tube #{i+1}: "))
            hole_count.append(temp)
    else:
        hole_count = [int(input("Amount of holes per tube: "))]
    refresh()


    corners = []
    # Ask if these are corners if the width is 3
    for i in range(multi_number):
        if widths[i] == 3 and yesno_func(f"Is Tube {i+1} a corner(offsets)(Y/n)?: ") == False:
            corners.append(True)
        else:
            corners.append(False)
    refresh()


    # Ask if we should offset 
    if yesno_func("Automatically place tube perimeters?(Y/n): ") == True:
        manual_mode = True
    else:
        manual_mode = False


    # # Ask if we should auto map holes
    # if yesno_func("Automatically place hole locations(Y/n)") == True:
    #     manual_holes = True
    # else:
    #     manual_holes = False
    # refresh()


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


        ##############################
        ###########Drawing############
        ##############################
        
        count = 1
        if multi_number == 1:
            draw_func(lengths[0],widths[0],0,total_tubes[0],hole_count[0],hole_rads[0]/2,count,corners[0])
        else:
            for i in range(multi_number):
                x, count = draw_func(lengths[i],widths[i],x,total_tubes[i],hole_count[i],hole_rads[i]/2,count,corners[i])              

        file.close