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



# def get_img_detail(html):

#     soup = BeautifulSoup(html ,'html.parser')
#     items = soup.find_all('img' ,{'class':'zoom'})
#     for item in items:
#         imgurl = item.get('src')
# #        print imgurl
#         save_img_thread(imgurl)



def demo111():
    
    host = 'https://pb01-1257866695.cos.ap-hongkong.myqcloud.com'
    path = '/Euro/EvaR/Silverstar/Silver-Starlets - Eva '
    name = 'Metallicpink-1'
    max = 144

    for x in range(1,max+1):

        url = host + path + name + ' - g/' + str(x) + '.jpg'
        name2 = '/Users/lijiajian/Desktop/Candydoll/' + name + '_' + str(x) + '.jpg'
        save_img_thread(url ,name2)


def demo222():
    
    host = 'https://pb01-1257866695.cos.ap-hongkong.myqcloud.com'
    path = '/Euro/EvaR/Silverstar/Silver-Starlets - Eva_'
    name = 'Silverdress-1'
    max = 130

    for x in range(1,max+1):

        url = host + path + name + '/' + str(x) + '.jpg'
        name2 = '/Users/lijiajian/Desktop/Candydoll/' + name + '_' + str(x) + '.jpg'
        save_img_thread(url ,name2)

def demo333():

    host = 'https://pb01-1257866695.cos.ap-hongkong.myqcloud.com'
    path = '/Euro/EvaR/Candydoll/'
    name = 'EvaR44 - vip'
    max = 100

    for x in range(1,max+1):

        url = host + path + name + ' - s/' + str(x) + '.jpg'
        name2 = '/Users/lijiajian/Desktop/Candydoll/' + name + '_' + str(x) + '.jpg'
        save_img_thread(url ,name2)

def demo444():

    host = 'https://pb01-1257866695.cos.ap-hongkong.myqcloud.com'
    path = '/Euro/EvaR/TeenModeling/Candydoll_'
    name = 'EvaR_TMTV_Kittytee'
    max = 100

    for x in range(1,max+1):

        url = host + path + name + '/' + str(x) + '.jpg'
        name2 = '/Users/lijiajian/Desktop/Candydoll/' + name + '_' + str(x) + '.jpg'
        save_img_thread(url ,name2)


def main():
   
    demo333()

    # 'https://pb01-1257866695.cos.ap-hongkong.myqcloud.com/Euro/EvaR/Silverstar/Silver-Starlets%20-%20Eva_Blackstockings%20-%20g/1.jpg'
    # 'https://pb01-1257866695.cos.ap-hongkong.myqcloud.com/Euro/EvaR/Silverstar/Silver-Starlets%20-%20Eva_Blackstockings-1%20-%20g/1.jpg'



main()


# https://pb01-1257866695.cos.ap-hongkong.myqcloud.com/Euro/EvaR/Candydoll/EvaR37%20-%20vip%20-%20s/1.jpg
# https://pb01-1257866695.cos.ap-hongkong.myqcloud.com/Euro/EvaR/TeenModeling/Candydoll_EvaR_TMTV_Cestchicpt2/1.jpg
# https://pb01-1257866695.cos.ap-hongkong.myqcloud.com/Euro/EvaR/TeenModeling/Candydoll_EvaR_TMTV_C%E2%80%99estchic/1.jpg



