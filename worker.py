__author__ = 'zhangxa'

import sys

from tornado.ioloop import IOLoop
from tornado.web import _unquote_or_none
from tornado import gen

from anger6Spider.spiders.spider import BaseSpider
from anger6Spider.log4s import Log4Spider
from anger6Spider.application import Application
from datetime import timedelta
from anger6Spider.env import SpiderEnv
from anger6Spider.spiderQueue.redisqueue import RedisQueue

import motor

"""
A Worker doing the main logic in a spider,do things below:
1.fetch a url from a spiderQueue
2.dispatch an url to a urlHandler
"""
class Worker:
    def __init__(self,application,queue):
        self.queue = queue
        self.application = application
        self.handler_class = None
        self.handler_kwargs = None
        self.path_args = []
        self.path_kwargs = {}

    def info(self):
            return '%s(handler_class=%s, kwargs%s, path_wargs=%r, path_kwargs=%r)' % \
                (self.__class__.__name__, self.handler_class,
                 self.handler_kwargs, self.path_args, self.path_kwargs)

    def getHandlerByUrl(self,url):
        return BaseSpider

    def _find_url_handler(self,url):
        app = self.application
        handlers = app._get_url_handler(url)
        if not handlers:
            self.handler_class = BaseSpider
            self.handler_kwargs = {}
            return
        for spec in handlers:
            match = spec.regex.match(url)
            if match:
                self.handler_class = spec.handler_class
                self.handler_kwargs = spec.kwargs
                #self.handler_kwargs.update({"app":app})
                if spec.regex.groups:
                    # Pass matched groups to the handler.  Since
                    # match.groups() includes both named and
                    # unnamed groups, we want to use either groups
                    # or groupdict but not both.
                    if spec.regex.groupindex:
                        self.path_kwargs = dict(
                            (str(k), _unquote_or_none(v))
                            for (k, v) in match.groupdict().items())
                    else:
                        self.path_args = [_unquote_or_none(s)
                                          for s in match.groups()]
                return

    @gen.coroutine
    def run(self):
        while True:
            url = yield self.queue.get()
            Log4Spider.debugLog(self,"get url:",url)
            try:
                env = yield SpiderEnv(url).gen_env()
            except Exception as e:
                Log4Spider.errLog(self,"spider env failed url:",url,"exception:",e)
                continue

            self._find_url_handler(url)
            Log4Spider.infoLog(self,"url: ",url," --- class: ",self.handler_class)
            spider = self.handler_class(env,self.application,**self.handler_kwargs)
            yield spider.work()
            for url in spider.urlLists:
                    Log4Spider.debugLog(self,"put url:",url)
                    yield self.queue.put(url)


@gen.coroutine
def main():
    settings = {
                "host": "localhost",
                "port": 6379,
                "db": 0
    }

    try:
        client = motor.MotorClient("mongodb://localhost:27017/")
        database = client['jd_db']
    except:
        print("mongodb init failed")
        sys.exit(0)

    app_settings = {
        "static_path":"static",
        "database":database
    }

    app = Application([
        (r"^http://www\.jd\.com", "anger6Spider.spiders.jd_spiders.Jd_Home_Spider"),
        (r"^http://list\.jd\.com.*", "anger6Spider.spiders.jd_spiders.Jd_BaseSpider"),
        (r"^http://channel\.jd\.com.*", "anger6Spider.spiders.jd_spiders.Jd_BaseSpider"),
        (r"^http://search\.jd\.com/search?.*", "anger6Spider.spiders.jd_spiders.Jd_BaseSpider"),
        (r"^http://item\.jd\.com.*", "anger6Spider.spiders.jd_spiders.Jd_Item_Spider"),
    ],**app_settings)

    cocurrency = 20



    from anger6Spider.spiderQueue.redisqueue import RedisQueue
    queue = RedisQueue(**settings)
    queue._create_redis_cli()
    #yield queue.put("http://www.jianshu.com")
    #yield queue.put("http://www.jd.com")
    #yield queue.put("http://www.ivsky.com")
    #yield queue.put("http://www.jd.com")

    workers = []
    for _ in range(cocurrency):
        workers.append(Worker(app,queue))

    for worker in workers:
        Log4Spider.debugLog("worker begin:",worker)
        worker.run()

    Log4Spider.debugLog("waitiing for spiderQueue empty:")
    yield queue.join(None)
    Log4Spider.debugLog("main done!")



if __name__ == "__main__":
    IOLoop.current().instance().run_sync(main)


