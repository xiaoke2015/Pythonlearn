#!/usr/bin/python
# -*- coding:utf-8 -*-

import urllib2
import urllib
import re

import requests



header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}

#url = 'http://pic15.nipic.com/20110803/7180732_211822337168_2.jpg'

url = 'http://c.51dtts.com/c2/AlissaP45等/AlissaP57/001.jpg'
path = '/Users/lijiajian/Desktop/1111.jpg'



# 这是一个图片的url
response = requests.get(url)
# 获取的文本实际上是图片的二进制文本
img = response.content
# 将他拷贝到本地文件 w 写  b 二进制  wb代表写入二进制文本
with open( path ,'wb' ) as f:
    f.write(img)



