
import random

for i in xrange(100):
    color = hex(int(random.random() * 255))[2:] + \
            hex(int(random.random() * 255))[2:] + \
            hex(int(random.random() * 255))[2:]

    print "<div style='background-color: #%s; width: 100\037; height: 20px;"% color
    print "text-align: center; vertical-align: middle; line-height: 20px; center; font-family: Courier; font-size: 12px; color: white;'>" 
    print color
    print "</div>"