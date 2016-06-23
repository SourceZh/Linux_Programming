#!/usr/local/bin/python3

#########################################
#			crawldata.py
#		This program is used to get
#	station name and their distance
#	by resolve html.
#		Data is saved at dirctory 'data/'
#
#							ZTY
#							2016.06.21
#########################################

import urllib.request, bs4
from bs4 import BeautifulSoup

line = {}

# read station's name and it's number from data file
# line_name file is edited manually
def getline():
	linefile = open('data/line_name', 'r')
	for l in linefile:
		[val, name] = l.split()
		line[name] = val
	linefile.close()

# get station's info from http://www.bjsubway.com/station/zjgls/
def getstationdistance():
	url = "http://www.bjsubway.com/station/zjgls/"
	req = urllib.request.Request(url)
	response = urllib.request.urlopen(req)
	html = response.read()
	# use BeautifulSoup to resolve the html
	soup = BeautifulSoup(html, "html5lib")
	# get each line station's distance info
	topul = soup.find('div', class_='history_top_c').ul
	for child in topul.children:
		if isinstance(child, bs4.element.Tag):
			# get this line's name
			line_name = child.string
			identity = child['id']
			# station's name info is saved at data/[linenum]_station_name
			# station's diatance info is saved at data/[linenum]_station_distance
			filen = open("data/"+str(line[line_name])+"_station_name", 'w')
			filed = open("data/"+str(line[line_name])+"_station_distance", 'w')
			for line_place in soup.find('div', id="sub"+identity).find_all('tbody'):
				index = 1
				stations = set()
				for tr in line_place.children:
					if isinstance(tr, bs4.element.Tag):
						# get distace map
						# save station's distance map into file
						[station1, station2] = tr.th.string.split('——')
						[distance, direction]= tr.find_all('td')
						two = direction.string == "上行/下行"
						filed.write(station1+'\t'+station2+'\t'+distance.string+'\t'+str(two)+'\n')
						# use station's order in distance map to set their number
						for s in [station1, station2]:
							if s not in stations:
								istation = "%02d%02d" % (int(line[line_name]), int(index))
								filen.write(istation+'\t'+s+'\n')
								index = index+1
								stations.add(s)
			filen.close()
			filed.close()


if __name__ == '__main__':
	getline()
	getstationdistance()