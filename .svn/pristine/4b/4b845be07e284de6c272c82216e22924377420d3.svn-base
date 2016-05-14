__author__ = 'zhangxa'

import sys
sys.path.append("../..")

from tornado import gen
from tornado.ioloop import IOLoop

from log4Spider.log4s import Log4Spider
from app.env import SpiderEnv
from urlHandler.urlHandler import UrlBaseHandler

class JdBookUrlHandler(UrlBaseHandler):
    def realWork(self):
        bsObj = self.env['soup']
        items = bsObj.findAll("div",{"class":"p-name"})
        for item in items:
            a = item.a
            print(a.get_text())
        prices = bsObj.findAll("div",{"class":"p-market"})
        for price in prices:
            print(price.find("del").string)

if __name__ == "__main__": #this test case just parse one html page
   base_url = "http://search.jd.com/search?keyword=python&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&offset=1&cid3=3806#J_crumbsBar"

   @gen.coroutine
   def main():
       env_obj = SpiderEnv(base_url)
       env = yield env_obj.gen_env()
       urlSeek = JdBookUrlHandler(env)
       urlSeek.work()
       for url in urlSeek.urlLists:
           Log4Spider.infoLog(url)
       Log4Spider.infoLog(len(urlSeek.urlLists))

   IOLoop.current().instance().run_sync(main)
