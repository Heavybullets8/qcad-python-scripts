from functions import *
import os

def general_tubes():
    x = 0
    count = 0
    lengths = "x"
    widths = "x"
    total_tubes = "x"
    hole_count = "x"
    hole_rads = "x"

    os.system('clear -x')
    # Ask how many different types of tubes there are
    print("Note - Differences in tube is any change in width, or length of a tube")
    multi_number = int_check(input("How many different type of tube is there?: "))   
    refresh(multi_number,lengths,widths,total_tubes,hole_rads,hole_count)


    lengths = []
    # Grab the length(s) of the tubes
    if multi_number > 1:
        for i in range(multi_number):
            temp = convert_to_float(input("Length of tube type #{i}: ".format(i=i+1)))
            lengths.append(temp)
    else:
        temp = convert_to_float(input("Length of tube: "))
        lengths.append(temp)
    refresh(multi_number,lengths,widths,total_tubes,hole_rads,hole_count)


    widths = []
    # Grab the width(s) of the tubes
    if multi_number > 1:
        for i in range(multi_number):
            temp = convert_to_float(input("Width of tube type #{i}: ".format(i=i+1)))
            widths.append(temp)
    else:
        temp = convert_to_float(input("Width of tube?: "))
        widths.append(temp)
    refresh(multi_number,lengths,widths,total_tubes,hole_rads,hole_count)


    total_tubes = []
    # Ask how many tubes there are
    for i in range(multi_number):
        temp = int_check(input("Number of tubes for #{i}: ".format(i=i+1)))
        total_tubes.append(temp)
    refresh(multi_number,lengths,widths,total_tubes,hole_rads,hole_count)
    
    
    # Ask if tubes will have the same hole size
    if multi_number > 1:
        hole_rads = []
        if yesno_func("Do the all of the tubes have the same hole size?(Y/n): ") == True:
            for i in range(multi_number):
                temp = convert_to_float(input("Hole size for tube #{i}: ".format(i=i+1)))
                hole_rads.append(temp)
        else:
            temp = convert_to_float(input("Hole diameter: "))
            for i in range(multi_number):
                hole_rads.append(temp)
    else:
        hole_rads = [convert_to_float(input("Hole diameter: "))]
    refresh(multi_number,lengths,widths,total_tubes,hole_rads,hole_count)



    # Ask if we should Automatically set hole count based on length
    auto_holes = yesno_func("Set # of holes automically?(Y/n): ")
    if auto_holes ==  False:
        hole_count = auto_holes_func(lengths)
    else:
        hole_count = []
        # Ask how many holes per tube
        if multi_number > 1:
            holes = []
            for i in range(multi_number):
                temp = int_check(input("Amount of holes for tube #{i}: ".format(i=i+1)))
                hole_count.append(temp)
        else:
            hole_count = [int_check(input("Amount of holes per tube: "))]
        refresh(multi_number,lengths,widths,total_tubes,hole_rads,hole_count)



    corners = []
    # Ask if these are corners if the width is 3
    for i in range(multi_number):
        if widths[i] == 3 and yesno_func("Is Tube {i} a corner(offsets)(Y/n)?: ".format(i=i+1)) == False:
            corners.append(True)
        else:
            corners.append(False)
    refresh(multi_number,lengths,widths,total_tubes,hole_rads,hole_count)


    # Ask if we should offset 
    if yesno_func("Automatically place tube perimeters?(Y/n): ") == True:
        manual_mode = True
    else:
        manual_mode = False




    # Place drawing constants
    constants()


    ##############################
    ###########Drawing############
    ##############################
    
    refresh(multi_number,lengths,widths,total_tubes,hole_rads,hole_count)
    count = 1
    offset = []
    for i in range(multi_number):
        offset.append(dry_run_func(lengths[i], hole_count[i], hole_rads[i]/2))
    
    if multi_number == 1:
        draw_func(lengths[0],widths[0],0,total_tubes[0],hole_count[0],hole_rads[0]/2,count,corners[0],manual_mode,offset[i])
    else:
        for i in range(multi_number):
            x, count = draw_func(lengths[i],widths[i],x,total_tubes[i],hole_count[i],hole_rads[i]/2,count,corners[i],manual_mode,offset[i])              


