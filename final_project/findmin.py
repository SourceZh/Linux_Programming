#!/usr/local/bin/python3

############################################
#				findmin.py
#		This program provides a interactive
#	interpreter to: 
#		1. query line info
#		2. query station info
#		3. find min road between two stations
#	Enter the program and type help to get
#	the usage.
#									ZTY
#									2016.06.23
############################################

import sys

lines = {}			# struct:line_name->line_number
lines_info = {}		# save station's info group by line. struct:line_name->[(station_number, station_name)]
station = {}		# struct:station_number->station_name
stations = set()	# save all station's name
station_attr = {}	# save station's attr. struct:line_name->class STATION
station_map = {}	# save station's distance map.struct:station_map[station1_name][station2_name]=distance

# this class is used to maintain station attr
class STATION:
	def __init__(self):
		self.line = []
		self.num = []
		self.exchange = False
		self.direction = []

# read line and station info from data file
# crawled by crawldata.py
def init():
	linefile = open('data/line_name', 'r')
	for line in linefile:
		# read line info
		[number, name] = line.split()
		lines[name] = number
		lines_info[name] = []
		# read station name info
		sfile = open("data/"+number+"_station_name", 'r')
		for sline in sfile:
			[snum, sname] = sline.split()
			lines_info[name].append((snum, sname))
			station[snum] = sname
			if sname not in station_map:
				station_map[sname] = {}
			stations.add(sname)
			if sname not in station_attr:
				station_attr[sname] = STATION()
			station_attr[sname].line.append(name)
			if len(station_attr[sname].line)>1:
				station_attr[sname].exchange = True
			station_attr[sname].num.append(snum)
		sfile.close()
		# read station distance info
		dfile = open("data/"+number+"_station_distance", 'r')
		for dline in dfile:
			[station1, station2, distance, twoway] = dline.split()
			station_map[station1][station2] = int(distance)
			station_attr[station1].direction.append(station2)
			if twoway == 'True':
				station_map[station2][station1] = int(distance)
				station_attr[station2].direction.append(station1)
		dfile.close()
	linefile.close()

# find min distance road. Algorithm:dijkstra
def dijkstra(s1, s2):
	dis = {}		# save other station's min distance to s1
	dis[s1] = {}
	dis[s1][s1] = 0
	before = {}		# save raod. struct: before[station1]=station2, the road is station2->station1
	# init
	for key in station_map[s1]:
		dis[s1][key] = station_map[s1][key]
		before[key] = s1
	S = {s1}		# S: station in S has got min road to s1
	Q = stations-S	# Q: station in Q has not got min road
	# find station min road to s1 until s2 is added in S
	while s2 in Q:
		mindis = 1000000000
		u = s1
		# find a station in Q is closest to s1
		for key in dis[s1]:
			if key not in S:
				if mindis > dis[s1][key]:
					mindis = dis[s1][key]
					u = key
		# add it into S
		S.add(u)
		Q.remove(u)
		# adjust distance to s1
		for key in station_map[u]:
			if key in dis[s1]:
				if dis[s1][key] > dis[s1][u] + station_map[u][key]:
					dis[s1][key] = dis[s1][u] + station_map[u][key]
					before[key] = u
			else:
				dis[s1][key] = dis[s1][u] + station_map[u][key]
				before[key] = u

	p = s2
	road = [s2]
	# backtrack road s1->s2
	while p != s1:
		p = before[p]
		road.insert(0, p)

	return [road, dis[s1][s2]]

# print help information
def help():
	print("Usage: [OPTION]...[STATION|LINE]...")
	print("[OPTION]")
	print("\tq, query [STATION] \t\t query the information about")
	print("\t\t\t\t\t [STATION]")
	print("\tr, road  [STATION1] [STATION2] \t find the min distance road")
	print("\t\t\t\t\t between [STATION1] and [STATION2]")
	print("\ts, station  [LINE] \t\t display this line's staiton information")
	print("\tl, line \t\t\t display lines information")
	print("\te, exit \t\t\t exit")
	print("\th, help \t\t\t display this information")
	print()
	print("[STATION]")
	print("\tstation can be station number or station name")
	print("[LINE]")
	print("\tline can be line number or line name")

# find two neighbor station in which line
def findline(s1, s2):
	for l1 in station_attr[s1].line:
		for l2 in station_attr[s2].line:
			if l1 == l2:
				return l1

def main():
	# wait user input to interact
	help()
	while True:
		text = input(">>>>>>")
		cmd = text.split()[0]
		if cmd == "query" or cmd == "q":
			# display the station's info
			# include: station name,
			# whether a exchange sgtation,
			# station in line, station number
			if len(text.split())<2:
				print("!!!INPUT ERROR!!!")
				help()
				continue				
			sta = text.split()[1]
			if sta.isdigit() and sta in station:	
				sta = station[sta]
			if sta not in stations:
				print("!!!INPUT ERROR!!!")
				help()
			else:
				print("车站名称："+sta)
				if station_attr[sta].exchange:
					print("换乘车站")
				linetext = "线路："
				for l in station_attr[sta].line:
					linetext = linetext+l+' '
				print(linetext)
				stationtext = "站号："
				for s in station_attr[sta].num:
					stationtext = stationtext+s+' '
				print(stationtext)
				dirtext = "方向："
				for d in station_attr[sta].direction:
					dirtext = dirtext+d+' '
				print(dirtext)
		elif cmd == "road" or cmd == "r":
			# find the min distance road
			# display road distance and the road
			if len(text.split())<3:
				print("!!!INPUT ERROR!!!")
				help()
				continue				
			s1 = text.split()[1]
			s2 = text.split()[2]
			if s1.isdigit() and s1 in station:
				s1 = station[s1]
			if s2.isdigit() and s2 in station:
				s2 = station[s2]
			if s1 not in stations or s2 not in stations or s1 == s2:
				print("!!!INPUT ERROR!!!")
				help()
			else:
				[road, distance] = dijkstra(s1, s2)
				print("最短路线推荐(长度："+str(distance)+")")
				roadline = road[0]+"->"+road[1]
				linename = findline(road[0], road[1])
				for i in range(2, len(road)):
					if linename not in station_attr[road[i]].line:
						linename = findline(road[i-1], road[i])
						roadline = roadline+"(换乘"+linename+")->"+road[i]
					else:
						roadline = roadline+"->"+road[i]
				print(roadline)
		elif cmd == "station" or cmd == "s":
			# display all stations in line
			# include: staiton number and 
			# staion name
			if len(text.split())<2:
				print("!!!INPUT ERROR!!!")
				help()
				continue
			line = text.split()[1]
			if line.isdigit() and line in lines.values():
				for (k, v) in lines.items():
					if line == v:
						line = k
			if line not in lines_info:
				print("!!!INPUT ERROR!!!")
				help()
			else:
				print("车站："+lines[line]+'\t'+line)
				for (snum, sname) in lines_info[line]:
					linetext = snum+'\t'+sname
					if station_attr[sname].exchange:
						linetext = linetext+"(换乘"
						for l in station_attr[sname].line:
							if l != line:
								linetext = linetext+" "+l
						linetext = linetext+")"
					print(linetext)
		elif cmd == "line" or cmd == "l":
			# display all lines information
			for key in sorted(lines, key=lines.get):
				print(lines[key]+'\t'+key)
		elif cmd == "exit" or cmd == "e":
			sys.exit(0)
		elif cmd == "help" or cmd == "h":
			# display help info
			help()
		else:
			print("!!!INPUT ERROR!!!")
			help()
				
if __name__ == '__main__':
	init()
	main()
