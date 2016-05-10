#!/usr/local/bin/python3
import urllib.request, re, socket
from bs4 import BeautifulSoup

###########################################
#	This function is to get page content
# from the url and store it.
#						by DoubleZ
#						2016.05.8
###########################################


# crawl and store
def crawl(url, file):
	try:
		req = urllib.request.Request(url)
		response = urllib.request.urlopen(req)

	except urllib.error.HTTPError:
		print("404:"+url)

	except urllib.error.URLError:
		print("url not found:"+url)

	else:
		html = response.read()
		soup = BeautifulSoup(html, "lxml")
		article = soup.find(id="artibody")
		if article is not None:
			for child in article.children:
				if child.name == 'p':
					content = child.string
					if content is not None:
						file.write(content.strip()+'\n')
		else:
			print("get "+url+" failed")

# get url from file to crawl
def gettitle(path, savepath):
	try:
		file = open(path, 'r')
		savefile = open(savepath, 'w')

	except FileNotFoundError:
		print("get file failed:"+path)

	else:
		for line in file:
			url = line.rstrip('\n')
			crawl(url, savefile)
		savefile.close()
		file.close()

def start():
	timeout = 10
	socket.setdefaulttimeout(timeout)
	for year in range(2008, 2016):
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