#!/usr/local/bin/python3
import urllib.request, json
from bs4 import BeautifulSoup

#######################################################
#	This function is to get everyday top news url
# from sina.com.
#	It only crawl news from 2008 to 2016, and before
# 2010 the page use static html and after 2010
# it use js to load the page. So handle them
# independently.
#						by DoubleZ
# 						2016.05.05
######################################################


# get title url from the specific page
def crawl(url, path):
	try:
		top = None
		while top is None:
			req = urllib.request.Request(url)
			response = urllib.request.urlopen(req)
			html = response.read()
			soup = BeautifulSoup(html, "lxml")
			top = soup.find(id='Con11')
		news = top.select('.ConsTi')
		file = open(path, 'w')
		for new in news:
			link = new.find('a')
			if link is None:
				continue
			file.write(link['href']+'\n')
		file.close()
	except urllib.error.HTTPError:
		print("get "+url+" failed")

# get title url from the specific js code
def crawljs	(url, path):
	try:
		req = urllib.request.Request(url)
		response = urllib.request.urlopen(req)
		js_str = response.read()
		json_str = str(js_str)[12:-4]
		data = json.loads(json_str)
		data = data['data']
		file = open(path, 'w')
		for item in data:
			itemurl = item['url'].replace('\\','')
			file.write(itemurl+'\n')
		file.close()
	except urllib.error.HTTPError:
		print("get "+url+" failed")
	except json.decoder.JSONDecodeError:
		print("decode error:"+url)


def start():
	for year in range(2008, 2010):
		for month in range(1, 13):
			for day in range(1, 32):
				syear = "%04d" % year
				smonth = "%02d" % month
				sday = "%02d" % day
				name = syear+smonth+sday
				url = "http://news.sina.com.cn/hotnews/%s.shtml" % name
				path = "title/%s" % name
				print("start "+name)
				print("start url:"+url)
				crawl(url, path)

	for year in range(2010, 2016):
		for month in range(1, 13):
			for day in range(1, 32):
				syear = "%04d" % year
				smonth = "%02d" % month
				sday = "%02d" % day
				name = syear+smonth+sday
				url = "http://top.news.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=www_all&top_time=%s&top_show_num=30&top_order=ASC&js_var=data" % name
				path = "title/%s" % name
				print("start "+name)
				print("start url:"+url)
				crawljs(url, path)	
	print("finish!")

if __name__ == "__main__":
	start()