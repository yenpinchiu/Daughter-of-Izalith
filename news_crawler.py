# encoding=utf-8
# Python 3.4
import os
import sys
import math
import urllib.request
from bs4 import BeautifulSoup
from html.parser import HTMLParser

Calender = {1:'01',2:'02',3:'03',4:'04',5:'05',6:'06',7:'07',8:'08',9:'09',10:'10',11:'11', \
			12:'12',13:'13',14:'14',15:'15',16:'16',17:'17',18:'18',19:'19',20:'20',21:'21',22:'22',\
			23:'23',24:'24',25:'25',26:'26',27:'27',28:'28',29:'29',30:'30',31:'31'}
Month = {6:'06',7:'07',8:'08',9:'09',10:'10',11:'11',12:'12',1:'01',2:'02',3:'03',4:'04',5:'05'}
ID = '00000000'
Type = {'focus':'FOS','politics':'POL','society':'SOC','business':'BUS'}
CTS_Type = {'focus':'260102','politics':'260106','society':'260110','business':'260109'}
APD_Type = {'focus':'頭條','focus_2':'要聞','politics':'政治','society':'社會','society_2':'生活','business':'熱門話題','business_2':'國際財經'}
APD_File_Type = {'focus':'FOS','focus_2':'FOS','politics':'POL','society':'SOC','society_2':'SOC','business':'BUS','business_2':'BUS'}

def CrawingWebEachPageLTN(url,aspect,idCount):
	webURL = url
	NewsType = Type[aspect]
	u = urllib.request.urlopen(webURL)
	buffer_1 = u.read()
	soup = BeautifulSoup(buffer_1)
	candidates = soup.find("div", attrs={"id": "newstext"})
	text = candidates.find_all('p', recursive=False)
	date = candidates.find('span')
	# print(len(candidates.contents))   
	temp = idCount
	strNumber = str(temp)
	idNumber = ID[0:8-len(strNumber)] + strNumber 
	id = 'LTN_'+NewsType+'_'+idNumber
	idCount += 1
	filename = id+'.xml'
	rawtitle = soup.find("title")
	rawtitle = rawtitle.contents[0]
	title = rawtitle.split('-')[0]
	title = title[:-1]
	outputFile = open(filename,'w',encoding = 'utf-8')
	outputFile.write('<?xml version="1.0" encoding="UTF-8"?>\n<xml>\n<doc>\n<id>')
	outputFile.write(id)
	outputFile.write('</id>\n<date>')
	outputFile.write(str(date.contents[0]))
	outputFile.write("</date>\n<title>")
	title = title.replace('','')
	outputFile.write(title.replace('&','&amp;'))
	outputFile.write("</title>\n<text>\n")
	for word in text:
		word = str(word)
		word = word.replace('','')
		word = word.replace('▼','')
		word = word.replace('■','')
		outputFile.write(word.replace('&','&amp;'))
		outputFile.write('\n')
	outputFile.write("</text>\n</doc>\n</xml>")
	outputFile.close()
	return idCount

def CrawingWebEachPageCTS(url,aspect,idCount):
	webURL = url
	NewsType = Type[aspect]
	u = urllib.request.urlopen(webURL)
	buffer_1 = u.read()
	soup = BeautifulSoup(buffer_1)
	candidates = soup.find("article", attrs={"class": "clear-fix"})
	text = candidates.find_all('p', recursive=True)
	times = soup.find("div", attrs={"class": "reporter"})
	times = times.find('time')
	datetime = times["datetime"]
	time = datetime.split(' ')[0].split('/')
	date = time[0]+'-'+time[1]+'-'+time[2]
	# print(len(candidates.contents))
	temp = idCount
	strNumber = str(temp)
	idNumber = ID[0:8-len(strNumber)] + strNumber 
	id = 'CTS_'+NewsType+'_'+idNumber
	idCount += 1
	filename = id+'.xml'
	rawtitle = soup.find("title")
	rawtitle = rawtitle.contents[0]
	title = rawtitle.split('-')[0]
	title = title[:-1]
	outputFile = open(filename,'w',encoding = 'utf-8')
	outputFile.write('<?xml version="1.0" encoding="UTF-8"?>\n<xml>\n<doc>\n<id>')
	outputFile.write(id)
	outputFile.write('</id>\n<date>')
	outputFile.write(date)
	outputFile.write("</date>\n<title>")
	outputFile.write(title.replace('&','&amp;'))
	outputFile.write("</title>\n<text>\n")
	for word in text:
		word = str(word)
		outputFile.write(word.replace('&','&amp;'))
		outputFile.write('\n')
	outputFile.write("</text>\n</doc>\n</xml>")
	outputFile.close()
	return idCount

def CrawingWebEachPageAPD(url,aspect,idCount):
	webURL = url
	NewsType = APD_File_Type[aspect]
	u = urllib.request.urlopen(webURL)
	buffer_1 = u.read()
	soup = BeautifulSoup(buffer_1)
	rawtitle = soup.find("title")
	rawtitle = rawtitle.contents[0]
	title = rawtitle.split('|')[0]
	title = title[:-1]
	times = soup.find("div", attrs={"class": "gggs"})
	times = times.find("time")
	if times:
		pass
	else:
		print('Time fail title is',title)
		return idCount
	datetime = times["datetime"]
	time = datetime.split(' ')[0].split('/')
	date = time[0]+'-'+time[1]+'-'+time[2]
	candidates = soup.find("div", attrs={"class": "articulum"})
	text = candidates.find_all('p', recursive=False)
	temp = idCount
	strNumber = str(temp)
	idNumber = ID[0:8-len(strNumber)] + strNumber 
	id = 'APD_'+NewsType+'_'+idNumber
	idCount += 1
	filename = id+'.xml'
	outputFile = open(filename,'w',encoding = 'utf-8')
	outputFile.write('<?xml version="1.0" encoding="UTF-8"?>\n<xml>\n<doc>\n<id>')
	outputFile.write(id)
	outputFile.write('</id>\n<date>')
	outputFile.write(date)
	outputFile.write("</date>\n<title>")
	outputFile.write(title.replace('&','&amp;'))
	outputFile.write("</title>\n<text>\n")
	for word in text:
		word = str(word.get_text())
		outputFile.write('<p>\n')
		outputFile.write(word.replace('&','&amp;'))
		# outputFile.write(str(word))
		outputFile.write('</p>\n')
	outputFile.write("</text>\n</doc>\n</xml>")
	outputFile.close()
	return idCount

def CrawingWebIndexPageLTN(month,day,year,idCount):
	time = Month[month] + Calender[day+1]
	aspectList = ['focus','politics','society','business']
	for eachAspect in aspectList:
		webURL = 'http://news.ltn.com.tw/newspaper/'+eachAspect+'/'+year+time
		u = urllib.request.urlopen(webURL)
		buffer_1 = u.read()
		soup = BeautifulSoup(buffer_1)
		candidates = soup.find("ul", attrs={"id": "newslistul"})
		text = candidates.find_all('a')
		for every in text:
			url = str(every['href'])
			url = 'http://news.ltn.com.tw/'+ url
			idCount = CrawingWebEachPageLTN(url,eachAspect,idCount)
		candidates = soup.find("div", attrs={"id": "page"})
		text = candidates.find_all('a')
		for every in text:
			url_2 = str(every['href'])
			u_2 = urllib.request.urlopen(webURL+url_2)
			buffer_2 = u_2.read()
			soup_2 = BeautifulSoup(buffer_2)
			candidates_2 = soup_2.find("ul", attrs={"id": "newslistul"})
			text_2 = candidates_2.find_all('a')
			for every_2 in text_2:
				url = str(every_2['href'])
				url = 'http://news.ltn.com.tw/'+ url
				idCount = CrawingWebEachPageLTN(url,eachAspect,idCount)
	return idCount

def CrawingWebIndexPageCTS(month,day,year,idCount):
	time = Month[month] + Calender[day+1]
	aspectList = ['focus','politics','society','business']
	for eachAspect in aspectList:
		CTS_code = CTS_Type[eachAspect]
		webURL = 'http://www.chinatimes.com/history-by-date/'
		webURL = webURL+year+'-'+Month[month]+'-'+Calender[day+1]+'-'+CTS_code
		u = urllib.request.urlopen(webURL)
		buffer_1 = u.read()
		soup = BeautifulSoup(buffer_1)
		candidates = soup.find("div", attrs={"class": "listRight"})
		text = candidates.find_all('h2')
		for every in text:
			temptext = every.find('a')
			url = str(temptext['href'])
			url = 'http://www.chinatimes.com'+ url
			idCount = CrawingWebEachPageCTS(url,eachAspect,idCount)
		candidates = soup.find("div", attrs={"class": "pagination clear-fix"})
		text = candidates.find_all('a')
		for every in text:
			url_2 = str(every['href'])
			url_2 = 'http://www.chinatimes.com'+ url_2
			u_2 = urllib.request.urlopen(url_2)
			buffer_2 = u_2.read()
			soup_2 = BeautifulSoup(buffer_2)
			candidates_2 = soup_2.find("div", attrs={"class": "listRight"})
			text_2 = candidates_2.find_all('h2')
			for every_2 in text_2:
				temptext = every_2.find('a')
				url = str(temptext['href'])
				url = 'http://www.chinatimes.com'+ url
				idCount = CrawingWebEachPageCTS(url,eachAspect,idCount)
	return idCount

def CrawingWebIndexPageAPD(month,day,year,idCount):
	time = Month[month] + Calender[day+1]
	aspectList = ['focus','focus_2','politics','society','society_2','business','business_2']
	prefix = 'http://www.appledaily.com.tw/appledaily/archive/'
	webURL = prefix + year + time
	u = urllib.request.urlopen(webURL)
	buffer_1 = u.read()
	soup = BeautifulSoup(buffer_1)
	# print(aspectList)
	for eachAspect in aspectList:
		# print(eachAspect)
		APD_code = APD_Type[eachAspect]
		soup = BeautifulSoup(buffer_1)
		candidates = soup.find("h2", attrs={"class": "nust clearmen"}, text = APD_code)
		if candidates:
			newcandidates = candidates
			newcandidates = newcandidates.find_next_siblings()
			urls = newcandidates[0].find_all("a", attrs={"target": "_blank"})
			for url_candidate in urls:
				word = url_candidate["href"]
				urladdress = 'http://www.appledaily.com.tw'+ str(word)
				temp = urladdress.split('/')
				temp_2 = temp[8:]
				url_candidate = temp[0]
				for x in range(1, 8):
					url_candidate = url_candidate + '/' + temp[x]
				# url_candidate = url_candidate + '/'
				for old in temp_2:
					new = urllib.parse.quote_plus(old)
					url_candidate = url_candidate + '/' + new 
				url_visit = url_candidate
				idCount = CrawingWebEachPageAPD(url_visit,eachAspect,idCount)
				# print(url_visit)
				# u_2 = urllib.request.urlopen(url_visit)
				# buffer_2 = u_2.read()
				# soup_2 = BeautifulSoup(buffer_2)
				# rawtitle = soup_2.find("title")
				# rawtitle = rawtitle.contents[0]
				# title = rawtitle.split('|')[0]
				# title = title[:-1]
				# print(title)
		else:
			print('fail happens!',APD_code,time)
	return idCount

def CrawingMain(argv):
	idCount = 25000
	Large = [1,3,5,7,8,10,12]
	List = [6,7,8]
	year = '2014'
	for month in List:
		if month == 2:
			upperbound = 28
		elif month in Large:
			upperbound = 31
		else:
			upperbound = 30
		for day in range(0,upperbound):
			idCount = CrawingWebIndexPageAPD(month,day,year,idCount)
			# idCount = CrawingWebIndexPageCTS(month,day,year,idCount)
			# idCount = CrawingWebIndexPageLTN(month,day,year,idCount)

if __name__ == '__main__':
	CrawingMain(sys.argv[1:])