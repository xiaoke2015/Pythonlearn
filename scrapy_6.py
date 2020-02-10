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
    print res.text.replace('\\', '')
    return res.text.replace('\\', '')

x = 1

# 为线程定义一个函数
def print_time( threadName, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print "%s: %s" % ( threadName, time.ctime(time.time()) )

def save_img( imgurl , name):
    '''
        下载保存图片
        '''
    
    urllib.urlretrieve(imgurl,name)
    
    # 线程移除
    mutex.acquire()
    th = threading.current_thread()
    tlist.remove(th)
    
    #如果线程今日等待状态 ，关闭等待
    if len(tlist)==maxthreads-1:
        evnt.set()
        evnt.clear()
    mutex.release()

def get_img_url(html):
    '''
        解析html 里的 图片链接
        '''
    soup = BeautifulSoup(html ,'html.parser')
#    write_word(html)
    items = soup.find_all('li',attr = {'class':'WB_pic S_bg2 bigcursor'})
    
    print items;
    global x
    return
    
    for item in items:
        imgurl = item.get('src')
        is_img = re.match('http:.*?.jpg' ,imgurl)
        if is_img != None :
            print x
            #            urllib.urlretrieve(imgurl,'/Users/lijiajian/Desktop/pic_url/%s.jpg' % x)
            name = '/Users/lijiajian/Desktop/pic_url/yangzi_%s.jpg' % x
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
                th = threading.Thread(target = save_img ,args = (imgurl ,name ,))
                th.start()
                # 添加线程管理
                tlist.append(th)
                x = x + 1
            
            except ZeroDivisionError,e:
                save_img(imgurl ,name)
                print e.message , "error"


def main():
    
    url = "https://s.weibo.com/weibo/%25E4%25B8%25AD%25E5%259B%25BD?topnav=1&wvr=6&b=1#_loginLayer_1522145051334"
#    for i in range(5,10):
    html = get_html(url)
    get_img_url(html)

#    uid = "1618051664"
#    mid = "4222216058460932"
#    pid = "60718250ly1fprfn9xu91j20gq0ou4qp"
#    get_largr_image_url(uid,mid,pid)


def write_word(word):
    with open("/Users/lijiajian/Desktop/weibo.txt","w") as f:
        f.write(word)


def get_largr_image_url(uid ,mid ,pid):

    url = "http://photo.weibo.com/" + uid + "/wbphotos/large/mid/" + mid + "/pid" + pid
    url = "http://photo.weibo.com/1618051664/wbphotos/large/mid/4222216058460932/pid/60718250ly1fprfn9xu91j20gq0ou4qp"
    html = get_html(url)
    print html
    soup = BeautifulSoup(html ,'html.parser')
    items = soup.find_all('img')
    print items


main()




