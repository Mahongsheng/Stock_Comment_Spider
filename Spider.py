# -*- coding: utf-8 -*-
#  476已完成 476-486
from bs4 import BeautifulSoup
import requests
from LogFile import logger
import csv
from urllib import error
import time

# 传入一个东方财富网股吧单个帖子的URL，即可爬取帖子的时间和评论内容。也可取消注释来爬取用户名
def getAllContent(url):
    allRow = [[]]
    newRow = []
    html = requests.get(url)
    html.encoding = 'utf-8'
    bsObj = BeautifulSoup(html.text, 'lxml')
    # Name = bsObj.find('div', {'id': 'zwconttbn'}).find('a').getText()  # Done
    Time = bsObj.find('div', {'class': 'zwfbtime'}).getText()[4:14]  # Done
    Content = bsObj.find('div', {'id': 'zwconttbt'}).getText()
    newRow.append(Time)
    newRow.append(Content[4:len(Content) - 3].strip())
    allRow.append(newRow)
    save(allRow)

    pageNum = 1
    while True:
        try:
            allRow = [[]]
            TimeList = []
            ContentList = []

            logger.info(u'爬取第' + str(pageNum) + '页...')
            newUrl = url[0:len(url) - 5] + '_' + str(pageNum) + '.html'
            pageNum = pageNum + 1
            html = requests.get(newUrl)
            html.encoding = 'utf-8'
            bsObj = BeautifulSoup(html.text, 'lxml')
            # Name = bsObj.find('div', {'id': 'zwlist'}).findAll('span', {'class': 'zwnick'})  # Done
            Time = bsObj.find('div', {'id': 'zwlist'}).findAll('div', {'class': 'zwlitime'})  # Done
            Content = bsObj.find('div', {'id': 'zwlist'}).findAll('div', {'class': 'zwlitext stockcodec'})
            YasuoContent = bsObj.find('div',{'id':'zwlist'}).findAll('div',{'class':'zwlitext yasuo stockcodec'})

            for i in range(0,len(Time)-len(YasuoContent)):
                TimeList.append(Time[i].getText()[4:14])

            for content in Content:
                newContent = content.find('div', {'class': 'short_text'}).getText().strip()
                ContentList.append(newContent)

            if(len(ContentList) == 0):

                break;
            for i in range(0, len(TimeList)):
                newRow = []
                newRow.append(TimeList[i])
                newRow.append(ContentList[i])
                allRow.append(newRow)
            save(allRow)
        except error.HTTPError as e:
            break
        except error.URLError as reason:
            break

# 传入一个东方财富网股吧xxx股吧的URl，即可返还在该页面下的所有帖子的链接。（含有“问董秘”的链接除外，爬起来会报错）
def getAllLink(url):
    allLinks = []
    html = requests.get(url)
    html.encoding = 'utf-8'
    bsObj = BeautifulSoup(html.text, 'lxml')
    listOdd = bsObj.findAll('div', {'class': 'articleh normal_post odd'})
    listEven = bsObj.findAll('div', {'class': 'articleh normal_post'})
    for div in listOdd:
        span = div.find('span', {'class': 'l3'})
        link = span.find('a')
        allLinks.append('http://guba.eastmoney.com' + link.get('href'))
    for div in listEven:
        span = div.find('span', {'class': 'l3'})
        link = span.find('a')
        allLinks.append('http://guba.eastmoney.com' + link.get('href'))
    return allLinks

# 将结果写入csv文件中
def save(result):
    csvFile = open("StockComments.csv", "a", newline="", encoding='utf-8')
    wr = csv.writer(csvFile)
    wr.writerows(result)
# 传入xxx股吧首页面即可进行爬取
def beginNow(url):
    postPage = 476 # 该参数为页面号，可观察网站URL得出
    allPage = []
    for i in range(0,10):
        newUrl = url[0:len(url) - 5] + '_' + str(postPage - i) + '.html'
        allPage.append(newUrl)
    # print(allPage)
    for i in range(0,len(allPage)):
        logger.info(u'爬取第' + str(postPage) + "页界面的所有帖子")
        allLinks = getAllLink(allPage[i])
        postPage = postPage - 1
        postNum = 1
        for url in allLinks:
            logger.info(u'爬取第' + str(postNum) + '个帖子的发帖者...')
            getAllContent(url)
            # time.sleep(1)
            postNum = postNum + 1;

# 传入断点的序号+1，即可从断的地方继续
def continueGet(num):
    url = 'http://guba.eastmoney.com/list,000725_476.html'
    allLink = getAllLink(url)
    postNum = num -2
    print(allLink[num])
    # print(allLink)
    for i in range(num,len(allLink)):
        logger.info(u'爬取第' + str(postNum) + '个帖子的发帖者...')
        getAllContent(allLink[i])
        postNum = postNum + 1


if __name__ == '__main__':
    # getAllContent('http://guba.eastmoney.com/news,000725,809545418.html')
    # beginNow('http://guba.eastmoney.com/list,000725.html')
    continueGet(8)