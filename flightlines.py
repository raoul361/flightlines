#!/usr/bin/env python

import json
import time
import os
import sys
import itertools

from PIL import Image, ImageDraw, ImageOps, ImageFilter


__author__ = "Raoul Endresl"
__copyright__ = "Copyright 2017"
__license__ = "BSD"
__version__ = "0.1"
__status__ = "Prototype"

"""
flightlines.py

plot aircraft movements.
"""

# Directory for JSON files for historic ADS-B data from: http://history.adsbexchange.com/Aircraftlist.json/2017-XX-YY.zip
DataDir = ".\\2017-04-20"

# Lat/lon bounding box.
lonUpper = 180.5
lonLower = 166.5

latUpper = -32.0
latLower = -46.0

# Scaling factor - large areas may consume too much memory/image size. Lower numbers for larger areas.
imageSizeFactor = 1000

imageFileName = "flight_" + str(int(lonLower)) + "_" + str(int(lonUpper)) + "_" + str(int(latLower)) + "_" + str(int(latUpper)) + ".jpg"


GlobalWaypoints = []

def LoadFile( flightDataFile ):
	print "Loading : " + flightDataFile,
	
	try:
		data = json.loads(open(flightDataFile, 'r').read())
		print "   success",
	except:
		print "   failed - " + str(sys.exc_info()[0])
		
	aircraft = 0	
	waypointcount = 0
	
	for flights in data['acList']:
		if 'Cos' in flights:
			aircraft += 1
			waypoints = flights['Cos']
			if flights['TT']:
				
				if (flights['TT'] != "a" or flights['TT'] != "s"):
					for lat, lon, time, altspeed in zip(waypoints[0::4], waypoints[1::4], waypoints[2::4], waypoints[3::4]):
						if ( (lat > latLower and lat < latUpper) and (lon > lonLower and lon < lonUpper)):
							if (altspeed != 0):
								GlobalWaypoints.append( (lat, lon) )
								waypointcount += 1
				else:
					for lat, lon, time in zip(waypoints[0::3], waypoints[1::3], waypoints[2::3]):
					
						if ( (lat > latLower and lat < latUpper) and (lon > lonLower and lon < lonUpper)):
							GlobalWaypoints.append( (lat, lon) )
							waypointcount += 1

	print " loaded " + str(aircraft) + " flights with " + str(waypointcount) + " waypoints - " + str(len(GlobalWaypoints)) + " total waypoints            \r",
	
	
	
def LoadAllFiles():
	for filename in os.listdir(DataDir):
		if filename.endswith(".json"): 
			fileToLoad = DataDir + "\\" + filename
			LoadFile( fileToLoad )
			

def Map():

	if os.path.isfile( imageFileName ):
		os.remove( imageFileName )
		
	im = Image.new( mode="RGB", size=(int(abs((lonUpper-lonLower)*imageSizeFactor)), int(abs((latUpper-latLower)*imageSizeFactor))), color="white" )
	draw = ImageDraw.Draw(im)
		
	for waypoint in GlobalWaypoints:
		ypix = int(abs((waypoint[0] - latLower) *imageSizeFactor))
		xpix = int(abs((waypoint[1] - lonLower) *imageSizeFactor))
		
		draw.point((xpix,ypix), fill="Blue")
	
	#im2 = im.filter(ImageFilter.MinFilter(3))
	flip = ImageOps.flip(im)
	flip.save( imageFileName, "JPEG", quality=95)
	print "\nWrote " + imageFileName
			
			
if __name__ == "__main__":
	LoadAllFiles()
	Map()