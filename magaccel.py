# Simple demo of the FXOS8700 accelerometer and magnetometer.
# Will print the acceleration and magnetometer values every second.
import time
from datetime import datetime

import board
import busio

import adafruit_fxos8700
import adafruit_fxas21002c

import csv

from Adafruit_BMP085 import BMP085

from datetime import datetime

import gpiozero
from gpiozero import LED

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the BMP085 and use STANDARD mode (default value)
# bmp = BMP085(0x77, debug=True)
bmp = BMP085(0x77)

# To specify a different operating mode, uncomment one of the following:
# bmp = BMP085(0x77, 0)  # ULTRALOWPOWER Mode
# bmp = BMP085(0x77, 1)  # STANDARD Mode
# bmp = BMP085(0x77, 2)  # HIRES Mode
# bmp = BMP085(0x77, 3)  # ULTRAHIRES Mode

# Initialize I2C bus and device.
i2c = busio.I2C(board.SCL, board.SDA)
# sensor = adafruit_fxos8700.FXOS8700(i2c)
# Optionally create the sensor with a different accelerometer range (the
# default is 2G, but you can use 4G or 8G values):
# sensor = adafruit_fxos8700.FXOS8700(i2c, accel_range=adafruit_fxos8700.ACCEL_RANGE_4G)
sensor = adafruit_fxos8700.FXOS8700(i2c, accel_range=adafruit_fxos8700.ACCEL_RANGE_8G)
sensor1 = adafruit_fxas21002c.FXAS21002C(i2c, gyro_range=adafruit_fxas21002c.GYRO_RANGE_2000DPS)

time_start = datetime.now()

file_name = 'rocket-data-' + str(datetime.now().hour) + '-' + str(datetime.now().minute) + '.csv'
with open(file_name, 'w', newline='') as datafile:
    datawriter = csv.writer(datafile, delimiter=';')

    # Main loop will read the acceleration and magnetometer values every second
    # and print them out.
    while True:
        # Read acceleration & magnetometer.
        accel_x, accel_y, accel_z = sensor.accelerometer
        mag_x, mag_y, mag_z = sensor.magnetometer

        # Read gyroscope.
        gyro_x, gyro_y, gyro_z = sensor1.gyroscope
        # Print values.

        temp = bmp.readTemperature()

        # Read the current barometric pressure level
        pressure = bmp.readPressure()

        # To calculate altitude based on an estimated mean sea level pressure
        # (1013.25 hPa) call the function as follows, but this won't be very accurate
        altitude = bmp.readAltitude()

        # To specify a more accurate altitude, enter the correct mean sea level
        # pressure level.  For example, if the current pressure level is 1023.50 hPa
        # enter 102350 since we include two decimal places in the integer value
        # altitude = bmp.readAltitude(102350)

        # write data to csv file
        datawriter.writerow([datetime.now(),
                             accel_x, accel_y, accel_z,
                             mag_x, mag_y, mag_z,
                             gyro_x, gyro_y, gyro_z,
                             temp, pressure, altitude
                            ])

        time_stop = datetime.now()
        time_elapsed = time_stop - time_start
        print(time_elapsed)
        if time_elapsed.seconds > 120:
            break 
