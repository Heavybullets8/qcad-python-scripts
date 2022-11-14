def sliders():
    import os
    from tabulate import tabulate
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
        head = [" ", "Slider 1", "Slider 2"]
        my_data = [
            ["Length", first_length,second_length],
            ["Width", 2,1],
            ["# of Tubes", first_type_am,second_type_am],
            ["Diameter", 0.625,0.625],
            ["Holes #", first_holes,second_holes]
        ]
        print(tabulate(my_data, headers=head, tablefmt="grid"))


    # Holes Function
    def holes_func(length,width,number,x,i,rad):
        file.write('setCurrentLayer("Holes");\n')
        if width == 2:
            while i > 0:
                location = length/(number+1)
                count = 1
                temp = number
                while temp > 0:
                    if (i % 2) == 0:
                        file.write(f"drawCircle({x+1.5},{location*count},{rad});\n")
                    else:
                        file.write(f"drawCircle({x+0.5},{location*count},{rad});\n")
                    count+=1
                    temp-=1
               
                x = x + float(width)
                i-=1
        else: 
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





    # Perimeter Function
    def parameter_func(length,width,x,i):
        file.write('setCurrentLayer("perimeter");\n')
        while i > 0:
            file.write(f"drawRectangle({width},{length},{x},0);\n")
            x = x + float(width)
            i-=1
        return


    # Grab the length(s) of the sliders
    first_length = convert_to_float(input("Length of the longer tube: "))
    second_length = first_length - 4
    refresh()


    # Ask how many tubes there are
    first_type_am = int(input("How many tubes are there in total?: "))/2
    second_type_am = first_type_am
    refresh()


    # Ask how many holes per tube
    first_holes = int(input("Amount of holes in the sliders: "))
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
        file.write('addLayer("perimeter", "red", "DASHED", RLineweight.Weight025);\n\n')


        ##############################
        ###########Drawing############
        ##############################

    

        # Draw first set of tube
        parameter_func(first_length,2,0,first_type_am)
        holes_func(first_length,2,first_holes,0,first_type_am,0.625/2)

        x = 2.0 * first_type_am

        # Draw second set of tube
        parameter_func(second_length,1,x,second_type_am)
        holes_func(second_length,1,second_holes,x,second_type_am,0.625/2)

        file.close