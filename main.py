#coding=utf-8
__author__ = 'zhangxa'

import sys
from curl import Curl
import pycurl

from htmlParser.htmlParser import UrlHtmlParser
from download.downFile import DownFile
from urlHandler.urlHandler import UrlBaseHandler
from urlQueue.urlQueue import LockUrlQueue
from workers.worker import BaseUrlWorker
import yaml
import pymongo
"""
start_url = "http://www.pcgames.com.cn/"

urlQ = UrlQueue()
urlQ.addUrl(start_url)
urlHandler = UrlBaseHandler(urlQ)
urlHandler.loop()
"""

config = {}
try:
    with open("config.yaml","r") as fin:
        config = yaml.load(fin)
except:
    print("can't find config.yaml file")
    sys.exit(0)

client = pymongo.MongoClient()
database = client[config["database"]["spiderQueue"]]

print(client,database)
"""
info = {'words': '9345', 'name': '我行我素的兔', 'articles': '6', 'beliked': '594', 'follows': '34', 'fans': '204'}
print(database)
database.jianshu_users.insert(info)

doc = database.jianshu_users.find_one()
print(doc)
"""
"""
urlQ = LockUrlQueue()
urlQ.addUrl("http://www.jianshu.com")
workers = []
nums = int(config["workers_num"])
for _ in range(nums):
    work = BaseUrlWorker(urlQ,database)
    work.start()
    workers.append(work)

for worker in workers:
    worker.join()
    print("work exit",worker)
"""
