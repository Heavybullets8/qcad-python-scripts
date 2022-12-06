from functions import *
import os

def sliders():
    count = 0
    lengths = "x"
    total_tubes = "x"
    hole_count = "x"
    hole_rads = [0.625,0.625]
    multi_hole_rad = False
    multi_width = False
    multi_length = False


    # Holes Function
    def draw_func_slider(length,width,hole_count,x,num_of_tubes,rad):
        excess = 0
        prior_excess = 0
        for tube in range(num_of_tubes):

            # Draw Rectangle
            file.write('setCurrentLayer("Perimeter");\n')
            if manual_mode == True:
                excess = convert_to_float(input("What is the excess of tube {tube_count}?: ".format(tube_count=tube+1)))
                
            # If there was no change, do not add the excess
            if excess == prior_excess:
                excess = 0

            # Remove excess from the previous exess, avoiding doubling up widths
            if excess > prior_excess:
                excess = excess - prior_excess
                
            if width == 1:
                file.write("drawRectangle({width},{length},{x},0);\n".format(width=width,length=length-4,x=x+excess))
            else:
                file.write("drawRectangle({width},{length},{x},0);\n".format(width=width,length=length,x=x+excess))

            
            file.write('setCurrentLayer("Holes");\n')
            for hole in range(hole_count):
                if width == 2:
                    # If first hole
                    if hole == 0: 
                        if ((tube) % 2) == 0:
                            file.write("drawCircle({x},6,{rad});\n".format(x=x+1.5+excess, rad=rad))
                        else:
                            file.write("drawCircle({x},6,{rad});\n".format(x=x+0.5+excess, rad=rad))
                    # If last hole        
                    elif hole == hole_count-1:
                        if ((tube) % 2) == 0:
                            file.write("drawCircle({x},{location},{rad});\n".format(x=x+1.5+excess,location=length-6,rad=rad))
                        else:
                            file.write("drawCircle({x},{location},{rad});\n".format(x=x+0.5+excess,location=length-6,rad=rad))
                    # If middle Hole
                    elif hole+1.5 == hole_count/2:
                        if ((tube) % 2) == 0:
                            file.write("drawCircle({x},{location},{rad});\n".format(x=x+1.5+excess,location=length/2,rad=rad))
                        else:
                            file.write("drawCircle({x},{location},{rad});\n".format(x=x+0.5+excess,location=length/2,rad=rad))         
                    # Any other hole
                    else:
                        if ((tube) % 2) == 0:
                            file.write("drawCircle({x},{location},{rad});\n".format(x=x+1.5+excess,location=((length/(hole_count-1))*(hole)),rad=rad))
                        else:
                            file.write("drawCircle({x},{location},{rad});\n".format(x=x+0.5+excess,location=((length/(hole_count-1))*(hole)),rad=rad))   
                            
                if width == 1:
                    # If first hole
                    if hole == 0: 
                        file.write("drawCircle({x},4,{rad});\n".format(x=x+.5+excess, rad=rad))
                    # If last hole        
                    elif hole == hole_count-1:
                        file.write("drawCircle({x},{location},{rad});\n".format(x=x+.5+excess, location=length-8, rad=rad))
                    # If middle Hole
                    elif hole+1.5 == hole_count/2:
                        file.write("drawCircle({x},{location},{rad});\n".format(x=x+.5+excess, location=length/2-2, rad=rad))     
                    # Any other hole
                    else:
                        file.write("drawCircle({x},{location},{rad});\n".format(x=x+.5+excess, location=((length/(hole_count-1))*(hole)-2), rad=rad)) 
            x = x + width
            


    lengths = []
    # Grab the length(s) of the sliders
    temp = convert_to_float(input("Length of tube: "))
    temp1 = temp - 4
    lengths.append(temp)
    lengths.append(temp1)
    refresh(2,lengths,[2,1],total_tubes,hole_rads,hole_count)


    # Ask how many tubes there are
    total_tubes = []
    amnt_one_width = int(input("How many tubes are there in total?: "))
    total_tubes.append(amnt_one_width/2)
    total_tubes.append(amnt_one_width/2)
    refresh(2,lengths,[2,1],total_tubes,hole_rads,hole_count)


    # Ask if we should Automatically set hole count based on length
    auto_holes = yesno_func("Set # of holes automically?(Y/n): ")
    if auto_holes ==  False:
        hole_count = auto_holes_func(lengths)
    else:
        hole_count = [int(input("Amount of holes per tube: "))]



    # Ask if we should offset 
    if yesno_func("Automatically place tube perimeters?(Y/n): ") == True:
        manual_mode = True
    else:
        manual_mode = False


    with open("box_maker.js","a") as file:
        
        # Create Javascript parameter function (boxes)
        constants()


        ##############################
        ###########Drawing############
        ##############################

    

        # Draw first set of tube
        draw_func_slider(lengths[0],2,hole_count[0],0,int(amnt_one_width/2),0.625/2)

        x = 2.0 * int(amnt_one_width/2)

        # Draw second set of tube
        draw_func_slider(lengths[0],1,hole_count[0],x,int(amnt_one_width/2),0.625/2)

        file.close