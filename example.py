#!/usr/bin/python3
from hx711 import HX711		# import the class HX711
import RPi.GPIO as GPIO		# import GPIO
import time

try:
	########## Change the pin values below to the pins you are using ###################
	DataPin = 21
	ClockPin = 20
	NumReadings = 10

	print("Reading HX711")
	# Create an object hx which represents your real hx711 chip
	# Required input parameters are only 'dout_pin' (data) and 'pd_sck_pin' (clock)
	# If you do not pass any argument 'gain_channel_A' then the default value is 128
	# If you do not pass any argument 'set_channel' then the default value is 'A'
	# you can set a gain for channel A even though you want to currently select channel B
	hx = HX711(dout_pin=DataPin, pd_sck_pin=ClockPin, gain=128, channel='A')
	
	print("Reset")
	result = hx.reset()		# Before we start, reset the hx711 ( not necessary)
	if result:			# you can check if the reset was successful
		print('Ready to use')
	else:
		print('not ready')
		
	# Read data several, or only one, time and return mean value
	# it just returns exactly the number which hx711 sends
	# argument times is not required default value is 1
	data = hx.get_raw_data(NumReadings)
	
	if data != False:	# always check if you get correct value or only False
		print('Raw data: ' + str(data))
	else:
		print('invalid data')

except (KeyboardInterrupt, SystemExit):
	print('Bye :)')
	
finally:
	GPIO.cleanup()

