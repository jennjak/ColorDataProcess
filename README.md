# ColorDataProcess
Code for collecting data from the RPi Pico w from UART and converting the data from txt file to csv

## Hardware
The Circuit contains MCU (RPi Pico W), Colour sensor, Multiplexer and Amplifier.
Picture

## Software
Thonny and Visual Studio

## Code Description
Below follows a breif description of each file for program and code

main.py - written in thonny. Collects data from the ADC and converts the input to range [0,255] to describe each primary colour RED, GREEN and BLUE. Transmit the values through UART to PC as string.

data_to_csv.py - written in Visual Studio. Collects the data RPi pico by reading the selected port. Sorts the data into each colour txt file for later use. Converts the sortet txt file into one csv file (excludes values above the minimum length of the txt files).

data_process.py - written in Visual Studio. Retrives the csv file and combine the values for each colours into a 3 coordinate system (this results in a time shift, 3*t). Cleans the data using Sliding Window Maximum and displays using MATLAB library Scatter and Bar plot.





