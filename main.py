# -*- coding: utf-8 -*-

#!/usr/bin/env python

__author__ = 'gaoqiangxu'

import os
# import time
import sys
import re
import mechanicalsoup
import urllib3

http = urllib3.PoolManager()

def real_path(file_name):
    return (os.path.dirname(os.path.realpath(__file__)) + '/' + file_name)

def makeRequest(url):
    r = http.request('GET', url)

    if r.status == 200:
        print('request ok:')
        return r.data
    else:
        print("request:" + url + "failed!")
        return None

def downloadMp3(baseUrl, url):
    path = baseUrl + '/' + os.path.basename(os.path.normpath(url))
    print path 
    if (os.path.exists(path)):
        return

    file = open(path, 'wb')
    data = makeRequest(url)
    if (data == None):
        return

    file.write(data)
    file.flush()
    file.close()


def downloadByDetailUrl(baseUrl, browser, url):
    url = "http://dwellingofduels.net" + url
    browser.close()
    browser.open(url)
    # regex = "*.mp3"
    
    links = browser.links()

    for link in links:
        hrefString = link.attrs["href"]
        pattern1 = re.compile('^http.*mp3$')
        result = pattern1.findall(hrefString)
        if result != None and len(result) > 0:
            downloadMp3(baseUrl, hrefString)


def downloadByYear(baseUrl, browser, year=17):
    
    path = "{:}/{:0>2}".format(baseUrl, year)
    if not os.path.exists(path):
            os.makedirs(path)

    for i in range(1, 12):
        path1 = "{:}/{:0>2}".format(path, i)
        if not os.path.exists(path1):
            os.makedirs(path1)

        regex = "duels/{:0>2}-{:0>2}-*".format(year, i)
        links = browser.links(regex)

        link = ""
        try:
            link = links[0]
        except:
            pass
        else:
            downloadByDetailUrl(path1, browser, link.attrs["href"])
        
            

def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')

    dir = real_path("DoD")
    if not os.path.exists(dir):
            os.makedirs(dir)

    url = "http://dwellingofduels.net/duels/"
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(url)

    downloadByYear(dir, browser, 17)
    
    browser.close()



if __name__ == "__main__":
    main()
