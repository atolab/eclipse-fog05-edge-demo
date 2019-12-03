#!/usr/bin/env python
#
# GrovePi Example for using the Grove Ultrasonic Ranger (http://www.seeedstudio.com/wiki/Grove_-_Ultrasonic_Ranger)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#
'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import sys
import grovepi
import time
import math
import json
from yaks import Yaks, Value, Encoding


SENSOR_RESOURCE = '/turtlebot/sensors'


ultrasonic_ranger = 6
thum_sensor = 5
aq_sensor = 0
# temp_humidity_sensor_type
# Grove Base Kit comes with the blue sensor.
blue = 0    # The Blue colored sensor.
white = 1   # The White colored sensor.

threshold = 10

grovepi.pinMode(aq_sensor,"INPUT")

yaks = Yaks.login(locator=sys.argv[1])
ws = yaks.workspace('/')


while True:
    try:
        # Read distance value from Ultrasonic
        dist = grovepi.ultrasonicRead(ultrasonic_ranger)
        #print(dist)
        [temp,humidity] = grovepi.dht(thum_sensor,blue)
        if math.isnan(temp) == False and math.isnan(humidity) == False:
            temp = str("%.02f"%temp)
            humidity = str("%.02f"%humidity)
            #print("temp = %.02f C humidity =%.02f%%"%(temp, humidity))
        aq_sensor_value = grovepi.analogRead(aq_sensor)

        if aq_sensor_value > 700:
            #print ("High pollution")
            aq = "High pollution"
        elif aq_sensor_value > 300:
            #print ("Low pollution")
            aq = "Low pollution"
        else:
            #print ("Air fresh")
            aq = "Air fresh"
        #print("sensor_value =", aq_sensor_value)

        #print("sensor_value = %d resistance = %.2f" %(l_sensor_value,  resistance))
        d = {
            'distance':dist,
            'temperature': temp,
            'humidity': humidity,
            'air_quality_raw':aq_sensor_value,
            'air_quality': aq
        }
        print(json.dumps(d))
        ws.put(SENSOR_RESOURCE, Value(json.dumps(d), Encoding.STRING))
        time.sleep(1)

    except TypeError:
        print ("Error")
    except IOError:
        print ("Error")
