__author__ = 'zhangxa'

import sys
sys.path.append("../..")

from tornado import gen
from tornado.ioloop import IOLoop

from log4Spider.log4s import Log4Spider
from app.env import SpiderEnv
from urlHandler.urlHandler import UrlSeekHandler
if __name__ == "__main__": #this test case just parse one html page
   base_url = "http://www.jianshu.com"

   @gen.coroutine
   def main():
       env_obj = SpiderEnv(base_url)
       env = yield env_obj.gen_env()
       urlSeek = UrlSeekHandler(env)
       urlSeek.work()
       for url in urlSeek.urlLists:
           Log4Spider.infoLog(url)
       Log4Spider.infoLog(len(urlSeek.urlLists))

   IOLoop.current().instance().run_sync(main)
