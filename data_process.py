############################################################################
# From csv file collects data and prepare it for plotting.
# Apply SWM algoritm for minimizing false negative values due to duty cycle.
# Defining each color by calibrated thresholds for each primary color.
# 
# Output from code is two scatter plots, one before SWM and one after. 
# And one Bar plot for color evaluation.
#
# Requirements: csv file must have been created by data_to_csv file 
# for correct alignment. User must manually define the color being 
# evaluated for correct title in plots.
############################################################################

# Import of libraries
from sklearn.cluster import KMeans
from sklearn import metrics
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Set manually your file path and color on the LED during test
file_path = 'YOURFILEPATH/t38_data_KNN.csv'
color = 'green' #'red' 'green' 'blue' 'white' 'yellow' 'dark'

# Step 0: Load your data
data = pd.read_csv(file_path)

# Step 1: Extract RGB columns
R = data.iloc[:, 0].values  # R values
G = data.iloc[:, 1].values  # G values
B = data.iloc[:, 2].values  # B values

# Step 3.0: Find shortest length
min_len = min(len(R), len(G), len(B))

# Step 3.1: Truncate all arrays to same length
c1 = R[:min_len]
c2 = G[:min_len]
c3 = B[:min_len]

# Step 4: Create new time factor array
time = [0]
pretime = 0
for i in range(1,len(c1)):
    time.append(pretime+0.000750)   # time = 0.000750 = 3*measurment_time
    pretime = pretime + 0.000750
    i = i + 1

# Step 5: Plot data before SWM
plt.plot()
plt.ylim([100,270])
plt.scatter(time, c1, color = 'red')

plt.plot()
plt.ylim([100,270])
plt.scatter(time, c2, color = 'green')

plt.plot()
plt.ylim([100,270])
plt.scatter(time, c3, color = 'blue')
plt.title('Color differentiation before SWM - '+ color + ' light')
plt.xlabel('Time [s]')
plt.ylabel('Samples value')
plt.show()

# Summerize the colors, each cycle creates 2000 values at fs = 4kHz
sum_c1 = []
sum_c2 = []
sum_c3 = []

# Step 6: Removes unactive value '0' and outliers above 260
for i in range(1, len(c1)):
    if c1[i] != 0 and c1[i] < 260:
        sum_c1.append(c1[i])
    if c2[i] != 0 and c2[i] < 260 :
        sum_c2.append(c2[i])
    if c3[i] != 0 and c3[i] < 260:
        sum_c3.append(c3[i])

# Step 7: Truncate all arrays to the minimal size
min_len1 = min(len(sum_c1), len(sum_c2), len(sum_c3))

c11 = sum_c1[:min_len1]
c21 = sum_c2[:min_len1]
c31 = sum_c3[:min_len1]

# Step 8: SWM metod, to minimize duty cycle effect (t = 4)
c111 = []
c211 = []
c311 = []

max1 = []
max2 = []
max3 = []
for i in range(1,len(c11)):
    if len(c111) != 4:
        c111.append(c11[i])
        c211.append(c21[i])
        c311.append(c31[i])
    else:
        max1.append(max(c111))
        c111 = []
        max2.append(max(c211))
        c211 = []
        max3.append(max(c311))
        c311 = []

c11 = max1
c21 = max2
c31 = max3

# Step 9: New timing reference due to SWM
time1 = [0]
pretime1 = 0
for i in range(0,len(c11)-1):
    time1.append(pretime1+ (0.000750)*15)
    pretime1 = (pretime1 + (0.000750)*15)
    i = i + 1

# Step 10: Plot data after SWM
plt.plot()
plt.ylim([100,255])
plt.scatter(time1, c11, color = 'red')

plt.plot()
plt.ylim([100,255])
plt.scatter(time1, c21, color = 'green')

plt.plot()
plt.ylim([100,255])
plt.scatter(time1, c31, color = 'blue')
plt.title('Color differentiation after SWM - '+ color + ' light')
plt.xlabel('Time [s]')
plt.ylabel('Samples value')
plt.show()

# Step 10: Check color differentiation after calibrated thresholds
colors = []
for i in range(1, len(c11)):
    if c11[i] >= 140 and c21[i] >= 180 and c31[i] >= 180:
        colors.append('white')
    elif c11[i] >= 170 and c21[i] >= 180:
        colors.append('yellow')
    elif c11[i] >= 170 :
        colors.append('red')
    elif c21[i] >= 180 :
        colors.append('green')
    elif c31[i] >= 180:
        colors.append('blue')
    elif c11[i] <= 160 and c21[i] <= 160 and c31[i] <= 160:
        colors.append('dark')

# Step 11: Calculate each color evaluation
TW = 0
TD = 0
TY = 0
TR = 0
TG = 0
TB = 0

for i in colors:
    if i == 'white':
        TW = TW + 1
    elif i == 'dark':
        TD = TD +1 
    elif i == 'yellow':
        TY =TY + 1
    elif i == 'red':
        TR = TR +1
    elif i == 'blue':
        TB = TB+1
    elif i == 'green':
        TG = TG +1

# Set x,y values for plot
colours = ['Red', 'Green', 'Blue', 'White', 'Yellow', 'Dark']
values = [TR, TG, TB, TW, TY, TD]

# Step 12: Plot in bar color evaluation
plt.bar(colours, values)
plt.title('Color differentiation - '+ color + ' light')
plt.xlabel('Color')
plt.ylabel('Samples')
plt.show()
