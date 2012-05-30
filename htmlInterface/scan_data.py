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


import os
import ConfigParser
import json

path = '/usr/share/applications/'
filelist = os.listdir(path)
templist = []



###################################################
# Get all .desktop files in /usr/share/applications
###################################################

for file in filelist:
	if file[-8:] == ".desktop":
		templist.append( path + file )

filelist = templist



###################################################
# Read all config-files
###################################################

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
