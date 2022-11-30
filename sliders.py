from functions import *
import os

def testing():
    count = 0
    lengths = "x"
    total_tubes = "x"
    hole_count = "x"
    hole_rads = [0.625,0.625]
    multi_hole_rad = False
    multi_width = False
    multi_length = False




    def holes_func(length,width,num_of_holes,x,num_of_tubes,rad):
        file.write('setCurrentLayer("Holes");\n')
        
        for tube in range(num_of_tubes):
            for hole in range(num_of_holes):
                
                if width == 2:
                    # If first hole
                    if hole == 0: 
                        if ((tube) % 2) == 0:
                            file.write(f"drawCircle({x+1.5},{6},{rad});\n")
                        else:
                            file.write(f"drawCircle({x+0.5},{6},{rad});\n")
                    # If last hole        
                    elif hole == num_of_holes-1:
                        if ((tube) % 2) == 0:
                            file.write(f"drawCircle({x+1.5},{length-6},{rad});\n")
                        else:
                            file.write(f"drawCircle({x+0.5},{length-6},{rad});\n")
                    # If middle Hole
                    elif hole+1.5 == num_of_holes/2:
                        if ((tube) % 2) == 0:
                            file.write(f"drawCircle({x+1.5},{length/2},{rad});\n")
                        else:
                            file.write(f"drawCircle({x+0.5},{length/2},{rad});\n")         
                    # Any other hole
                    else:
                        if ((tube) % 2) == 0:
                            file.write(f"drawCircle({x+1.5},{(length/(num_of_holes-1))*(hole)},{rad});\n")
                        else:
                            file.write(f"drawCircle({x+0.5},{(length/(num_of_holes-1))*(hole)},{rad});\n")   
                            
                if width == 1:
                    # If first hole
                    if hole == 0: 
                        file.write(f"drawCircle({x+.5},{4},{rad});\n")
                    # If last hole        
                    elif hole == num_of_holes-1:
                        file.write(f"drawCircle({x+.5},{length-8},{rad});\n")
                    # If middle Hole
                    elif hole+1.5 == num_of_holes/2:
                        file.write(f"drawCircle({x+.5},{length/2-2},{rad});\n")     
                    # Any other hole
                    else:
                        file.write(f"drawCircle({x+.5},{(length/(num_of_holes-1))*(hole)-2},{rad});\n") 
            x = x + width
            
            



    # # Holes Function
    # def holes_func(length,width,number,x,i,rad):
    #     file.write('setCurrentLayer("Holes");\n')
        
    #     # 2 inch tube
    #     if width == 2:
    #         while i > 0:
    #             location = length/(number+1)
    #             count = 1
    #             temp = number
    #             while temp > 0:
    #                 if i == 0: 
    #                     if (i % 2) == 0:
    #                         file.write(f"drawCircle({x+1.5},{6},{rad});\n")
    #                     else:
    #                         file.write(f"drawCircle({x+0.5},{6},{rad});\n")
    #                 elif i == number-1:
    #                     if (i % 2) == 0:
    #                         file.write(f"drawCircle({x+1.5},{length-6},{rad});\n")
    #                     else:
    #                         file.write(f"drawCircle({x+0.5},{length-6},{rad});\n")         
    #                 else:
    #                     if (i % 2) == 0:
    #                         file.write(f"drawCircle({x+1.5},{location*count},{rad});\n")
    #                     else:
    #                         file.write(f"drawCircle({x+0.5},{location*count},{rad});\n")            
                            
    #                 count+=1
    #                 temp-=1
               
    #             x = x + float(width)
    #             i-=1
        
    #     # 1 inch tube
    #     else: 
    #         while i > 0:
    #             location = length/(number+1)
    #             count = 1
    #             temp = number
    #             while temp > 0:
    #                 file.write(f"drawCircle({x+(width/2)},{location*count},{rad});\n")
    #                 count+=1
    #                 temp-=1
    #             x = x + float(width)
    #             i-=1

    #     return


    # Perimeter Function
    def parameter_func(length,width,x,i):
        file.write('setCurrentLayer("perimeter");\n')
        while i > 0:
            file.write(f"drawRectangle({width},{length},{x},0);\n")
            x = x + float(width)
            i-=1
        return



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


    hole_count = []
    # Ask how many holes per tube
    num_of_holes = int(input("Amount of holes in the sliders: "))
    hole_count.append(num_of_holes)
    hole_count.append(num_of_holes)
    refresh(2,lengths,[2,1],total_tubes,hole_rads,hole_count)


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
        parameter_func(lengths[0],2,0,int(amnt_one_width/2))
        holes_func(lengths[0],2,num_of_holes,0,int(amnt_one_width/2),0.625/2)

        x = 2.0 * int(amnt_one_width/2)

        # Draw second set of tube
        parameter_func(lengths[1],1,x,int(amnt_one_width/2))
        holes_func(lengths[0],1,num_of_holes,x,int(amnt_one_width/2),0.625/2)

        file.close