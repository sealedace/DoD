# -*- coding: utf-8 -*-

#!/usr/bin/env python

__author__ = 'gaoqiangxu'

import os
import sys
import re
import mechanicalsoup
import urllib3
import requests

def real_path(file_name):
    return (os.path.dirname(os.path.realpath(__file__)) + '/' + file_name)

def makeRequest(url):
    r = requests.get(url)

    if r.status_code == 200:
        print('request ok:')
        return r.text
    else:
        print("request:" + url + " failed!")
        return None

def downloadMp3(baseUrl, url):
    print "Start download " + url

    fileName = os.path.basename(os.path.normpath(url))
    path = baseUrl + '/' + fileName
    print path 
    if (os.path.exists(path)):
        print '"' + fileName + '"' + " exists, skip."
        return

    data = makeRequest(url)
    if (data == None):
        print fileName + "download failed"
        return

    file = open(path, 'wb')
    file.write(data)
    file.flush()
    file.close()


def downloadByDetailUrl(baseUrl, browser, url):
    url = "http://dwellingofduels.net" + url
    browser.close()
    browser.open(url)
    
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
        print "Create folder: " + path
        os.makedirs(path)

    for i in range(1, 12):
        path1 = "{:}/{:0>2}".format(path, i)
        if not os.path.exists(path1):
            print "Create folder: " + path1
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
        print "Create folder: " + dir
        os.makedirs(dir)

    url = "http://dwellingofduels.net/duels/"
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(url)

    downloadByYear(dir, browser, 17)
    browser.close()



if __name__ == "__main__":
    main()
