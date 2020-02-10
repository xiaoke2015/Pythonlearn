#!/usr/bin/python
# -*- coding:utf-8 -*-


import requests
import urllib
from bs4 import BeautifulSoup
import re

import threading
import time


# 线程锁
mutex = threading.Lock()
# 最大线程数
maxthreads = 10
# 线程管理数组
tlist = []
evnt=threading.Event() #用事件来让超过最大线程设置的并发程序等待


def get_html(url):
    '''
        get 请求获取 html 内容
        '''
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
    res = requests.get(url = url ,headers = headers)
    res.encoding = 'gbk'
#    print res.text
    return res.text





def save_img( imgurl , name):
    '''
        下载保存图片
        '''

#    urllib.urlretrieve(imgurl,name)

    # 这是一个图片的url
    response = requests.get(imgurl)
    # 获取的文本实际上是图片的二进制文本
    img = response.content
    # 将他拷贝到本地文件 w 写  b 二进制  wb代表写入二进制文本
    with open( name ,'wb' ) as f:
        f.write(img)

    # 线程移除
    mutex.acquire()
    th = threading.current_thread()
    tlist.remove(th)

    #如果线程今日等待状态 ，关闭等待
    if len(tlist)==maxthreads-1:
        evnt.set()
        evnt.clear()
    mutex.release()

x = 1

def save_img_thread(imgurl ,name):

    global x
    print x ,imgurl
    #            urllib.urlretrieve(imgurl,'/Users/lijiajian/Desktop/pic_url/%s.jpg' % x)
#    name = '/Users/lijiajian/Desktop/candydoll/LauraB18-%s.jpg' % x

        #            save_img(imgurl ,name)
    try:

        # 锁定
        mutex.acquire()
        # 判断当前线程数是否最大 ，如最大，等待
        if len(tlist) >= maxthreads:
            mutex.release()
            evnt.wait()
        else:
            mutex.release()

        # 创建新线程
        th = threading.Thread(target = save_img ,args = (imgurl.encode("UTF-8") ,name ,))
        th.start()
        # 添加线程管理
        tlist.append(th)
        x = x + 1

    except ZeroDivisionError,e:

        print e.message , "error"


def get_img_url(html):
    '''
        解析html 里的 图片链接
        '''
    soup = BeautifulSoup(html ,'html.parser')
#    print soup.text
    items = soup.find_all('li' ,{'class':'pbw'})
    for item in items:
        pass
        url = item.find('a').get('href')
        html = get_html(url)
        get_img_detail(html)



def get_img_detail(html):

    soup = BeautifulSoup(html ,'html.parser')
    items = soup.find_all('img' ,{'class':'zoom'})
    for item in items:
        imgurl = item.get('src')
#        print imgurl
        save_img_thread(imgurl)




def main():

    url = 'http://wx1.sinaimg.cn/mw690/006RPOIigy1fqd8aa6fn3j31hp2lyb29.jpg'
    name = '/Users/lijiajian/Desktop/script/scrapy/images/yangzi.jpg'
    save_img_thread(url ,name)

#http://a.51dtts.com/CD6/KatieM44/001.jpg
#http://b.abbbx.com/B5/CD2/AlissaP61/001.jpg
#http://b.abbbx.com/B4/Alissa%20TM/Alissa%20Bunnyears/001.jpg
#http://b.abbbx.com/B4/Alissa%20TM/Alissa%20Bunnyearspt2/001.jpg
    #
    # for i in range(1,10):
    #     url = 'http://wx1.sinaimg.cn/mw690/006RPOIigy1fqd8aa6fn3j31hp2lyb29.jpg'
    #     name = '/Users/lijiajian/Desktop/yangzi.jpg'
    #     save_img_thread(url)
    #
    #
    # for i in range(10,100):
    #     url = 'http://c.abbbx.com/CD20160303/LauraB18/0%s.jpg' % x
    #     save_img_thread(url)



main()
