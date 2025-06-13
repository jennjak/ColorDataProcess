# Retrieve and handle data from ARD readings

red_data = open("C:/your file path/t8_red_data_clean.txt", "r")

green_data = open("C:/your file path/t8_green_data_clean.txt", "r")

blue_data = open("C:/your file path/t8_blue_data_clean.txt", "r")

red = []
green = []
blue = []

# Saving every string in text that correspont to a digit(float type)
for line_r in red_data:
    red = [float(num) for num in line_r.split()]

for line_g in green_data:    
    green = [float(num) for num in line_g.split()]
    

for line_b in blue_data:
    blue = [float(num) for num in line_b.split()]

# Close files
red_data.close()
green_data.close()
blue_data.close()

### Removes zeros
red_z = []
green_z = []
blue_z = []

a = 0

for elem in red:
    if elem != 0:
        red_z.append(elem)
    else:
        a = a + 1

for elem in green:
    if elem != 0:
        green_z.append(elem)

for elem in blue:
    if elem != 0:
        blue_z.append(elem)
    
print(a)


### Color Calculations
""" Calculation of the corrdinate systme of the light colcor is based on the 
CIE 1963 system, x= X/(X+Y+Y), and y = Y/(X+Y+Z)"""

# sRGB to XYZ conversion matrix

M = [
    [0.4124, 0.3576, 0.1805],
    [0.2126, 0.7152, 0.0722],
    [0.0193, 0.1192, 0.9505]
]

M1 = [[0.631, 0.434, 0.143],
     [0.172, 0.820, 0.060],
     [0.004, 0.050, 0.645]]



##Coordinate

x_coord = []
y_coord = []
z_coord = []

for i in range(0,10000):

    if red_z[i] > 0 or green_z[i] > 0 or blue_z[i] > 0:
        R_lin, G_lin, B_lin = (red_z[i])/255, (green_z[i])/255, (blue_z[i])/255 # Assume RGB values normalized to 0–1


        X = M[0][0]*R_lin + M[0][1]*G_lin + M[0][2]*B_lin
        Y = M[1][0]*R_lin + M[1][1]*G_lin + M[1][2]*B_lin
        Z = M[2][0]*R_lin + M[2][1]*G_lin + M[2][2]*B_lin

        x = X / (X + Y + Z)
        y = Y / (X + Y + Z)
        z = x-y
        
        
        x_coord.append(x)
        y_coord.append(y)
        z_coord.append(z)

x_coord_str = str(x_coord)
y_coord_str = str(y_coord)
z_coord_str = str(z_coord)
 
xcoord = open("C:/Users/jakob/KTH/KEXjob/Communication/data_handler/xcoord.txt", "w")  
ycoord = open("C:/Users/jakob/KTH/KEXjob/Communication/data_handler/ycoord.txt", "w")  
zcoord = open("C:/Users/jakob/KTH/KEXjob/Communication/data_handler/zcoord.txt", "w")  

xcoord.write(x_coord_str)
ycoord.write(y_coord_str)
zcoord.write(z_coord_str)

xcoord.close()
ycoord.close()
zcoord.close()

