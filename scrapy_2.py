#!/usr/bin/python
# -*- coding:utf-8 -*-

# requests 网络请求模块
import requests

#下载网络图片
import urllib

# html 解析模块
from bs4 import BeautifulSoup
import re


def get_img(url):
    res = requests.get(url)
    res.encoding = 'gbk' #gbk
    soup = BeautifulSoup(res.text,'html.parser')
    
    x = 0
    arr = soup.find_all(re.compile("dl"))
   
#    print arr[0].find_all("dd")[0]
    for tag in soup.find_all(re.compile("dl")):
        img = tag.find_all("dd")[0];
#        print img.text
#        imgurl = img.text
#        urllib.urlretrieve(imgurl,'/Users/lijiajian/Desktop/pic_url/%s.jpg' % x)
#        x = x+1

#    for tag in soup.find_all(re.compile("dl")):
#        print(tag)


res = requests.get('http://slide.ent.sina.com.cn/')
#print(res.encoding)

# 设置文字编码
res.encoding = 'gbk' #gbk

#创建 beautifulsoup 对象
soup = BeautifulSoup(res.text,'html.parser')

#print soup.title.text

#正则匹配，名字中带有b的标签
arr = soup.find_all(re.compile("dl"))
url = arr[0].a.get('href')
get_img(url)


#for tag in soup.find_all(re.compile("dl")):
#    url = tag.a.get('href')
#    get_img(url)



