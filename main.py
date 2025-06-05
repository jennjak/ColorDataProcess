""" Using ADC to retrieve sensor data and converts it into a range in [0,255].
Data is locally stored in list and sent in specific intervalls
to the computer via UART, using the print function."""

from machine import Pin, ADC, PWM, Timer	#import pin and adc class
import time
from picozero import pico_led

pin_27 = Pin(27, Pin.IN)

light_color = ADC(pin_27)

led_red = PWM(Pin(21, Pin.OUT))
led_green = PWM(Pin(20, Pin.OUT))
led_blue = PWM(Pin(19, Pin.OUT))

mux_s0 = Pin(10, Pin.OUT)
mux_s1 = Pin(11, Pin.OUT)
mux_s2 = Pin(12, Pin.OUT)

start_time = time.time()

value_color = 0 #start value for ADC-reading

state = 0b00

state_led = 0b00
nextstate_led = 0b01

state_led3 = 0b000
nextstate_led3 = 0b001

mux_s0.value(0)
mux_s1.value(0)
mux_s2.value(0)

#set frequency range 8 Hz - 62.5 MHz (mikrocontroller runs on 125 MHz)
FREQUENCY = 1000

led_red.freq(FREQUENCY)
led_green.freq(FREQUENCY)
led_blue.freq(FREQUENCY)

#set duty cycle, range 0 - 65535 (16 bit)
DUTY_CYCLE = 16383 # approx 25%

led_red.duty_u16(0)
led_green.duty_u16(0)
led_blue.duty_u16(0)

def ReadColor(timer):
    global value_color
    value_color = light_color.read_u16() >> 4 # shift 4 bits from 16 to 12 bit
    value_color = value_color / 4096
    value_color = int(value_color*255)

# Cahnges state between emitting red, green and blue
def LedSM(timer):
    global state_led
    global nextstate_led
    
    if state_led == 0b00:
        led_green.duty_u16(0)
        led_red.duty_u16(0)
        led_blue.duty_u16(0)    
    elif state_led == 0b01:
        led_green.duty_u16(0)
        led_red.duty_u16(DUTY_CYCLE)
        led_blue.duty_u16(0)
    
    elif state_led == 0b10:
        led_green.duty_u16(DUTY_CYCLE)
        led_red.duty_u16(0)
        led_blue.duty_u16(0)
        
    elif state_led == 0b11:
        led_green.duty_u16(0)
        led_red.duty_u16(0)
        led_blue.duty_u16(DUTY_CYCLE)
    
    if state_led == 0b00:
        state_led = nextstate_led
    else :
        nextstate_led = (state_led + 1) % 4
        if nextstate_led == 0b00:
            nextstate_led = 0b01 
        state_led = 0b00
        
# Changes only one color, for singular colour blinking
def LedSM1(timer):
    global state_led
    global nextstate_led
    
    if state_led == 0b00:
        led_green.duty_u16(0)
        led_red.duty_u16(0)
        led_blue.duty_u16(0)
        
        nextstate_led = 0b01
    elif state_led == 0b01:
        led_green.duty_u16(DUTY_CYCLE)
        led_red.duty_u16(DUTY_CYCLE)
        led_blue.duty_u16(DUTY_CYCLE)
        
        nextstate_led = 0b00
    
    state_led = nextstate_led
    
# Includes more colour, yellow, white, purple and cyan
def LedSM2(timer):
    global state_led3
    global nextstate_led3
    
    if state_led3 == 0b000:
        led_green.duty_u16(0)
        led_red.duty_u16(0)
        led_blue.duty_u16(0)    
    elif state_led3 == 0b01:
        led_green.duty_u16(0)
        led_red.duty_u16(DUTY_CYCLE)
        led_blue.duty_u16(0)
    
    elif state_led3 == 0b010:
        led_green.duty_u16(DUTY_CYCLE)
        led_red.duty_u16(0)
        led_blue.duty_u16(0)
        
    elif state_led3 == 0b011:
        led_green.duty_u16(0)
        led_red.duty_u16(0)
        led_blue.duty_u16(DUTY_CYCLE)
        
    elif state_led3 == 0b100:
        led_green.duty_u16(DUTY_CYCLE)
        led_red.duty_u16(DUTY_CYCLE)
        led_blue.duty_u16(DUTY_CYCLE)
    
    elif state_led3 == 0b101:
        led_green.duty_u16(DUTY_CYCLE)
        led_red.duty_u16(DUTY_CYCLE)
        led_blue.duty_u16(0)
    
    elif state_led3 == 0b110:
        led_green.duty_u16(DUTY_CYCLE)
        led_red.duty_u16(0)
        led_blue.duty_u16(DUTY_CYCLE)
    
    elif state_led3 == 0b111:
        led_green.duty_u16(0)
        led_red.duty_u16(DUTY_CYCLE)
        led_blue.duty_u16(DUTY_CYCLE)
    
    if state_led3 == 0b000:
        state_led3 = nextstate_led3
    else :
        nextstate_led3 = (state_led3 + 1) % 8
        if nextstate_led3 == 0b000:
            nextstate_led3 = 0b001 
        state_led3 = 0b000
    
    
def MuxSM(timer):
    global state
    if state == 0b01:
        mux_s0.value(1) #1
        mux_s1.value(0) #0
        mux_s2.value(0)
    elif state == 0b10:
        mux_s0.value(0)
        mux_s1.value(1)
        mux_s2.value(0)
    else :
        mux_s0.value(0)
        mux_s1.value(0) #0
        mux_s2.value(0)
    
    state = (state + 1) % 3
        
# Set up a timer that trigger interrupt every 500 ms
timer = Timer()
timer.init(freq=4000, mode=Timer.PERIODIC, callback=ReadColor)

mux_timer = Timer()
#mux_timer.init(period=500, mode=Timer.PERIODIC, callback=MuxSM)
mux_timer.init(period = 500, mode=Timer.PERIODIC, callback=MuxSM)

#led_timer = Timer(2)
#led_timer.init(period=500, mode=Timer.PERIODIC, callback=LedSM)

listRED = []
listGREEN = []
listBLUE = []

listRGB = []

last_led_time = time.ticks_ms()

while True:

    now = time.ticks_ms()
    
    if time.ticks_diff(now, last_led_time) >= 500:
        LedSM1(None)
        last_led_time = now

        
    if mux_s0.value() == 1:
        listRED.append(0)
        listGREEN.append(value_color)
        listBLUE.append(0)
    elif mux_s1.value() == 1:
        listRED.append(0)
        listGREEN.append(0)
        listBLUE.append(value_color)
    else :
        listRED.append(value_color)
        listGREEN.append(0)
        listBLUE.append(0)
        
    if len(listRED) > 300:
        listRGB.append('red')
        listRGB.append(listRED)
        listRGB.append('green')
        listRGB.append(listGREEN)
        listRGB.append('blue')
        listRGB.append(listBLUE)
        
        print(listRGB)
        
        listRGB.clear()
        listRED.clear()
        listGREEN.clear()
        listBLUE.clear()
        
        
    
    

    
        
    
        
            
    







