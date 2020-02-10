#!/usr/bin/python
# -*- coding:utf-8 -*-

# requests 网络请求模块
import requests

#下载网络图片
import urllib

# html 解析模块
from bs4 import BeautifulSoup
import re



res = requests.get("http://www.cocoachina.com/ios/list_69_1.html");
res.encoding = 'utf-8'
#print res.text

soup = BeautifulSoup(res.text ,'html.parser')

# 获取标题
tag1 = soup.find_all('div',{'class':'clearfix newstitle'})

# 获取内容
tag2 = soup.find_all('div',{'class':'newsinfor'})

tag3 = soup.find_all('div',{'class':'float-r'})


for i in range(0,len(tag1)):
    tags4 = tag1[i].find('a')
    print tags4.text , tag2[i].text , tag3[i].text





