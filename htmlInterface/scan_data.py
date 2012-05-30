#!/usr/bin/env python

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.




PATH = '/usr/share/applications/'




###################################################
# Get all .desktop files in /usr/share/applications
###################################################

#import os
#filelist = os.listdir(path)

import glob
filelist = glob.glob(PATH+"/*.desktop")


###################################################
# Read all config-files
###################################################

#import ConfigParser
#import json

#cfgparser = ConfigParser.RawConfigParser()

#filelist = cfgparser.read( filelist )		#discard all non-readable files
#cfgparser.readfp( open(filelist[7]) )
#print cfgparser.items("Desktop Entry")
#print cfgparser.get("Desktop Entry", "Name")


#for desktopfile in filelist:
#	cfgparser.readfp( open(desktopfile) )
#	i = cfgparser.get("Desktop Entry", "Name")



###################################################
# Write to XML-File
###################################################

from xml.dom.minidom import Document
doc = Document()

top = doc.createElement("ApplicationList")
doc.appendChild(top)

for desktopfile in filelist:
	appTag = doc.createElement("app")
	top.appendChild(appTag)
	
	appTag.appendChild( doc.createTextNode(desktopfile) )
	

print doc.toprettyxml()


f = open('LOCAL_appdata.xml', 'w')
f.write(doc.toprettyxml())
