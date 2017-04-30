import requests
from bs4 import BeautifulSoup
import xlrd
import csv
import pickle
import logging
import os
import pygame

def GetDict(word):
	url = "http://dict.youdao.com/w/%s/" % word
	html = requests.get(url).content
	soup = BeautifulSoup(html, "html.parser")
	GE=GetExample(soup)
	GEX=GetExplanation(soup)
	if GE is None:
		d[word] = [[], [], GEX]
	elif len(GE)>3:
		d[word]=[[GE[0],GE[3]],[GE[1],GE[4]],GEX]
	elif len(GE)<=3:
		d[word] = [[GE[0]], [GE[1]], GEX]
	print(word,GEX,GE)

def GetExplanation(soup):
	try:
		return_list=soup.find("div",attrs={"class":"results-content","id":"results-contents"})
		return_list2=return_list.find("div",attrs={"class":"trans-container"})
		return_list3=return_list2.find_all("li")
	except AttributeError:
		return None
	l=[]
	for li in return_list3:
		dic=li.get_text().strip()
		l.append(dic)
	return l

def GetExample(soup):
	try:
		return_list=soup.find("div",attrs={"id":"examples","class":"trans-wrapper"})
		return_list2=return_list.find("div",attrs={"class":"trans-container tab-content","id":"bilingual"})
		return_list3=return_list2.find_all("p")
	except AttributeError:
		return None
	l=[]
	for p in return_list3:
			dic=p.get_text().strip()
			l.append(dic)
	return l

def download_word(word,type=1):
    if os.path.exists("sounds/%s-%d.mp3"%(word,type)):
        pass
    else:
        r = requests.get("http://dict.youdao.com/dictvoice?audio=%s&type=%d"%(word,type))
        html = r.content

        with open("sounds/%s-%d.mp3"%(word,type), "wb") as f:
            f.write(html)

def xls_to_list(address):
	data=xlrd.open_workbook(address)
	table=data.sheets()[0]
	col=table.col_values(0)
	l=[]
	for i in col:
		l.append(i)
	return l

d={}

l=xls_to_list("init data file\\六级单词表.xlsx")
'''
#下载单词信息
try:
	for word in l:
		GetDict(word)
		print(str(word)+" is OK")
except Exception as e:
	logging.exception(e)
finally:
	with open("C:\\Users\\Helios\\Desktop\\CET6_detail.pkl","wb") as f:
		pickle.dump(d,f)
#下载单词发音
try:
	for word in l:
		download_word(word)
		print(str(word) + " is OK")
except Exception as e:
	logging.exception(e)
'''
