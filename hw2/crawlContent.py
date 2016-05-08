#!/usr/local/bin/python3
import urllib.request, re
from bs4 import BeautifulSoup
from threading import Thread

def crawl(url, file):
	cnt = 10
	try:
		article = None
		while article is None and cnt > 0:
			req = urllib.request.Request(url)
			response = urllib.request.urlopen(req)
			html = response.read()
			soup = BeautifulSoup(html, "lxml")
			article = soup.find(id="artibody")
			cnt = cnt-1
		if cnt > 0:
			for child in article.children:
				if child.name == 'p':
					content = child.string
					if content is not None:
						file.write(content.strip()+'\n')
		else:
			print("get "+url+" failed")
	except urllib.error.HTTPError:
		print("404:"+url)
	except urllib.error.URLError:
		print("url not found:"+url)

		

def gettitle(path, savepath):
	try:
		file = open(path, 'r')
		savefile = open(savepath, 'w')
		for line in file:
			url = line.rstrip('\n')
			crawl(url, savefile)
		savefile.close()
		file.close()
	except FileNotFoundError:
		print("get file failed:"+path)

# def crawlyear(year):
# 	for month in range(1, 13):
# 		for day in range(1, 32):
# 			syear = "%04d" % year
# 			smonth = "%02d" % month
# 			sday = "%02d" % day
# 			name = syear+smonth+sday
# 			titlepath = "title/%s" % name
# 			contentpath = "content/%s" % name
# 			print("start "+name)
# 			gettitle(titlepath, contentpath)

# class mythread (Thread):
# 	def __init__(self, year):
# 		Thread.__init__(self)
# 		self.year = year
# 	def run(self):
# 		crawlyear(self.year)

def start():
	# threads = []
	for year in range(2008, 2016):
	# 	crawlThread = mythread(year)
	# 	crawlThread.start()
	# 	threads.append(crawlThread)
	# for thread in threads:
	# 	thread.join()
		for month in range(1, 13):
			for day in range(1, 32):
				syear = "%04d" % year
				smonth = "%02d" % month
				sday = "%02d" % day
				name = syear+smonth+sday
				titlepath = "title/%s" % name
				contentpath = "content/%s" % name
				print("start "+name)
				gettitle(titlepath, contentpath)
	print("finish!")



if __name__ == '__main__':
	start()
	gettitle("title/20100314", "content/20100314")