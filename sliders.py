from functions import *
import os

def sliders():
    lengths = "x"
    total_tubes = "x"
    hole_count = "x"
    hole_rads = [0.625,0.625]



    # Holes Function
    def draw_func_slider(length,width,hole_count,x,num_of_tubes,rad,count):
        excess = 0
        prior_excess = 0
        for tube in range(num_of_tubes):

            # Draw Rectangle
            file.write('setCurrentLayer("Perimeter");\n')
            if manual_mode == True:
                excess = convert_to_float(input("What is the excess (to the left) of tube {tube_count}?: ".format(tube_count=tube+1+count)))
                if excess == None:
                    excess = prior_excess
                
                # If there was no change, do not add the excess
                if excess == prior_excess:
                    excess = 0

                # Remove excess from the previous exess, avoiding doubling up widths
                if excess > prior_excess:
                    excess = excess - prior_excess
                    prior_excess = excess
                
            if width == 1:
                file.write("drawRectangle({width},{length},{x},0);\n".format(width=width,length=length-4,x=x+excess))
            else:
                file.write("drawRectangle({width},{length},{x},0);\n".format(width=width,length=length,x=x+excess))

            
            file.write('setCurrentLayer("Holes");\n')
            for hole in range(hole_count):

                # If first hole
                if hole == 0: 
                    math = 6
                # If last hole        
                elif hole == hole_count-1:
                    math = length-6
                # If middle Hole
                elif hole+1.5 == hole_count/2:
                    math = length/2
    
                # Any other hole
                else:
                    math = (length/(hole_count-1))*(hole)
                                    
                # Minus 2 from each 1 inch width slider
                if width == 1:
                    math = math - 2
                
                # if even number tube and width is 2, add 1.5
                if ((tube) % 2) == 0 and width == 2:
                    file.write("drawCircle({x},{math},{rad});\n".format(x=x+1.5+excess, math=math, rad=rad))
                else:
                     file.write("drawCircle({x},{math},{rad});\n".format(x=x+0.5+excess, math=math, rad=rad))
            
            x = x + width + excess
        return x


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
        x = draw_func_slider(lengths[0],2,hole_count[0],0,int(amnt_one_width/2),0.625/2,0)


        # Draw second set of tube
        draw_func_slider(lengths[0],1,hole_count[0],x,int(amnt_one_width/2),0.625/2,int(amnt_one_width/2))

