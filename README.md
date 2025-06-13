# ColorDataProcess
Code for collecting data from the RPi Pico w from UART and converting the data from txt file to csv.

## Hardware
The Circuit contains MCU (RPi Pico W), Colour sensor, Multiplexer and Amplifier.
Picture

## Software
MATLAB, Thonny and Visual Studio

## Code Description
Below follows a breif description of each file for program and code

main.py - written in thonny. Collects data from the ADC and converts the input to range [0,255] to describe each primary colour RED, GREEN and BLUE. Transmit the values through UART to PC as string.

data_to_csv.py - written in Visual Studio. Collects the data RPi pico by reading the selected port. Sorts the data into each colour txt file for later use. Converts the sortet txt file into one csv file (excludes values above the minimum length of the txt files).

data_process.py - written in Visual Studio. Retrives the csv file and combine the values for each colours into a 3 coordinate system (this results in a time shift, 3*t). Cleans the data using Sliding Window Maximum and displays using MATLAB library Scatter and Bar plot.

### Appendix codes
Some selected codes are only evaluated and discarded as feasable for this colour data process system.
Even if both system are highly functional and somewhat prefereabvle in some cases, both illustrations model was not suited for the basic construct of the circuit.

#### K-Means Cluster

K_Means.py - written in Visuals Studio. Apply K-Means clustering with Euclidean distance as parameter, and display in a 3D plot. Some Calculation of the center of centroid and optimal center can be done by manually insert the coordinates.

#### XY CIE - system

cieSystem.py - written in Visual Studio. Calcule the x and y coordinates by the CIE 1963 system, x= X/(X+Y+Y), and y = Y/(X+Y+Z), and stores the coordinates in txt files.

kexXY.m - written in MATLAB. Displays the coordinates in a CIE diagram.





