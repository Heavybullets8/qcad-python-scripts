def general_tubes():
    import os
    from tabulate import tabulate
    x = 0
    count = 0
    yesno = ""
    second_holes = "x"
    second_width = "x"
    second_length = "x"
    second_diameter = "x"
    second_type_am = "x"
    first_type_am = "x"
    first_holes = "x"
    first_width = "x"
    first_length = "x"
    first_diameter = "x"
    multi_hole_rad = False
    multi_width = False
    multi_length = False

    # TODO: add offset for sliders


    def convert_to_float(frac_str):
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


    # refresh table
    def refresh():
        os.system('cls||clear -x')
        if multi_length == False and multi_width == False:
            head = [" ", "Tube"]
            my_data = [
                ["Length", first_length],
                ["Width", first_width],
                ["Tubes #", first_type_am],
                ["Diameter", first_diameter],
                ["Holes #", first_holes]
            ]
        else:
            head = [" ", "Tube 1", "Tube 2"]
            my_data = [
                ["Length", first_length,second_length],
                ["Width", first_width,second_width],
                ["# of Tubes", first_type_am,second_type_am],
                ["Diameter", first_diameter,second_diameter],
                ["Holes #", first_holes,second_holes]
            ]
        print(tabulate(my_data, headers=head, tablefmt="grid"))


    # Hole radius function
    def rad_hole(measurement1,measurement2,type):
        yesno = ""
        while yesno not in ["y","Y","n","N"]:
                yesno = input(f"Do the {measurement1} and the {measurement2} {type} tube have the same size holes?(Y/n): ")
                if yesno in ["y","Y"]:
                    return False
                elif yesno in ["n","N"]:
                    return True
                else:
                    print("Invalid input, please try again..")


    # Holes Function
    def holes_func(length,width,number,x,i,rad):
        file.write('setCurrentLayer("Holes");\n')
        while i > 0:
            location = length/(number+1)
            count = 1
            temp = number
            while temp > 0:
                file.write(f"drawCircle({x+(width/2)},{location*count},{rad});\n")
                count+=1
                temp-=1
            x = x + float(width)
            i-=1
        return


    # Parameter Function
    def parameter_func(length,width,x,i):
        file.write('setCurrentLayer("Perimeter");\n')
        while i > 0:
            file.write(f"drawRectangle({width},{length},{x},0);\n")
            x = x + float(width)
            i-=1
        return


    # Ask if there are multiple lengths of tube
    while yesno not in ["y","Y","n","N"]:
        yesno = input("Are all of the tubes the same length?(Y/n): ")
        if yesno in ["y","Y"]:
            multi_length = False
        elif yesno in ["n","N"]:
            multi_length = True
        else:
            print("Invalid input, please try again..")
    yesno = ""


    # Ask if there are multiple widths of tube
    while yesno not in ["y","Y","n","N"]:
        yesno = input("Are all of the tubes the same width?(Y/n): ")
        if yesno in ["y","Y"]:
            multi_width = False
        elif yesno in ["n","N"]:
            multi_width = True
        else:
            print("Invalid input, please try again..")
    yesno = ""
    refresh()


    # Grab the length(s) of the tubes
    if multi_length == True:
        first_length = convert_to_float(input("Length of the first tube: "))
        second_length = convert_to_float(input("Length of the other tube: "))
    else:
        first_length = convert_to_float(input("Length of the tube: "))
        second_length = first_length
    refresh()


    # Grab the width(s) of the tubes
    if multi_width == True:
        first_width = convert_to_float(input("Width of the first tube: "))
        second_width = convert_to_float(input("Width of the other tube: "))
    else:
        first_width = convert_to_float(input("Width of the tube: "))
        second_width = first_width
    refresh()


    # Ask how many tubes there are
    if multi_width == True or multi_length == True:
        total_am = int(input("How many tubes are there in total?: "))
        first_type_am = int(input(f"How many tubes are {first_width} in width?: "))
        second_type_am = total_am - first_type_am
    else:
        first_type_am = int(input("How many tubes are there in total?: "))
    refresh()


    # Ask if tubes will have the same hole size
    if multi_width == True:
            multi_hole_rad = rad_hole(first_width, second_width,"width")
    elif multi_length == True:
            multi_hole_rad = rad_hole(first_length, second_length,"length")
    refresh()


    # Ask hole(s) diameter
    if multi_hole_rad == True:
        first_diameter = convert_to_float(input("Tube 1 hole diameter: "))
        second_diameter = convert_to_float(input("Tube 2 hole diameter: "))
    else:
        first_diameter = convert_to_float(input("Hole diameter: "))
        second_diameter = first_diameter
    refresh()


    # Ask how many holes per tube
    if multi_length == True:
        first_holes = int(input(f"Amount of holes in the {first_length} in. ?: "))
        second_holes = int(input(f"Amount of holes in the {second_length} in. ?: "))
    else:
        first_holes = int(input(f"Amount of holes in the {first_length} in. ?: "))
        second_holes = first_holes
    refresh()


    with open("box_maker.js","w") as file:
        
        # Create Javascript parameter function (boxes)
        file.write("function drawRectangle(width, height, x, y){\n \
        addLine(x, y, x, y + height);\n \
        addLine(x, y, x + width, y);\n \
        addLine(x + width, y, x + width, y + height);\n \
        addLine(x, y + height, x + width, y + height);\n}\n\n")

        # Create Javascript circle function
        file.write("function drawCircle(x,y,size){\n \
        addCircle(x,y,size);\n}\n")

        # Add layers
        file.write('addLayer("Holes", "cyan", "CONTINUOUS", RLineweight.Weight025);\n')
        file.write('addLayer("Perimeter", "red", "DASHED", RLineweight.Weight025);\n\n')




        ##############################
        ###########Drawing############
        ##############################

        if multi_length == False and multi_width == False:
            parameter_func(first_length,first_width,0,first_type_am)
            holes_func(first_length,first_width,first_holes,0,first_type_am,first_diameter/2)


        if multi_length == True and multi_width == False:

            # Draw first set of tube
            parameter_func(first_length,first_width,x,first_type_am)
            holes_func(first_length,first_width,first_holes,x,first_type_am,first_diameter/2)

            x = first_width * first_type_am

            # Draw second set of tube
            parameter_func(second_length,first_width,x,second_type_am)
            holes_func(second_length,first_width,second_holes,x,second_type_am,second_diameter/2)


        if multi_length == True and multi_width == True:

            # Draw first set of tube
            parameter_func(first_length,first_width,x,first_type_am)
            holes_func(first_length,first_width,first_holes,x,first_type_am,first_diameter/2)

            x = first_width * first_type_am
            
            # Draw second set of tube
            parameter_func(second_length,second_width,x,second_type_am)
            holes_func(second_length,second_width,second_holes,x,second_type_am,second_diameter/2)


        if multi_length == False and multi_width == True:

            # Draw first set of tube
            parameter_func(first_length,first_width,x,first_type_am)
            holes_func(first_length,first_width,first_holes,x,first_type_am,first_diameter/2)

            x = first_width * first_type_am
            
            # Draw second set of tube
            parameter_func(first_length,second_width,x,second_type_am)
            holes_func(first_length,second_width,first_holes,x,second_type_am,first_diameter/2)
    
        file.close