__author__ = 'zhangxa'

import sys
sys.path.append("../..")

from app.application import Application
from workers.worker import Worker

from tornado.queues import Queue
from tornado import gen
from tornado.ioloop import IOLoop

from log4Spider.log4s import Log4Spider
from datetime import timedelta

app = Application([
        (r"^http://www.baidu.com.*$", "urlHandler.urlHandler.UrlSeekHandler",{"a":10,"b":3}),
        (r"^http://www.jianshu.com/([0-9]+)/([0-9])+", "urlHandler.urlHandler.UrlBaseHandler",{"a":3}),
    ])

@gen.coroutine
def main():
    cocurrency = 10

    queue = Queue()
    queue.put("http://www.jianshu.com")

    workers = []
    for _ in range(cocurrency):
        workers.append(Worker(app,queue))

    for worker in workers:
        Log4Spider.debugLog("worker begin:",worker)
        worker.run()

    Log4Spider.debugLog("waitiing for spiderQueue empty:")
    yield queue.join(timeout=timedelta(seconds=300))
    Log4Spider.debugLog("main done!")

if __name__ == "__main__":
    IOLoop.current().instance().run_sync(main)