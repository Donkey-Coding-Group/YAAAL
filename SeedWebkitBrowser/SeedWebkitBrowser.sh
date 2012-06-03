#!/bin/bash

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>. 


clear && clear


COMMAND="seed seedbrws.js"


function helpandexit() {
	echo -e "SeedWebkitBrowser"
	echo -e ""
	echo -e "Available options:"
	echo -e "\t--source=local\t<link>\t(relative/absolute link to"
	echo -e "\t\t\t\tdirectory with index.html)"
	echo -e ""
	echo -e "\t--source=http\t<link>\t(URI format only!)"
	echo -e ""
	echo -e "Examples:"
	echo -e "\t./SeedWebkitBrowser.sh --source=http http://www.google.com"
	echo -e "\t./SeedWebkitBrowser.sh --source=local ."
	echo -e "\t./SeedWebkitBrowser.sh --source=local ../../res/html/"
	echo -e "\t./SeedWebkitBrowser.sh --source=local /var/www/"

	echo -e ""
	exit
}




#=========	Check if two arguments are given	=========#
if [ "$#" != 2 ]; then
	helpandexit
else
	true
fi
#========================================================#




if [ "$1" == "--source=http" ]; then
	echo ""
	$COMMAND $2
elif [ "$1" == "--source=local" ]; then
	
	APPPATH=$(pwd)
	cd $2
	FILEPATH=$(pwd)
	
	echo $APPPATH
	echo $FILEPATH
	
	cd $APPPATH
	
	echo ""
	$COMMAND file:/$FILEPATH/index.html
else
	helpandexit
fi


