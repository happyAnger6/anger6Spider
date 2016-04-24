__author__ = 'zhangxa'

import sys
sys.path.append("../..")

from app.application import Application
from workers.worker import Worker
from tornado.queues import Queue

app = Application([
        (r"^http://www.baidu.com.*$", "urlHandler.urlHandler.UrlSeekHandler",{"a":10,"b":3}),
        (r"^http://www.jianshu.com/([0-9]+)/([0-9])+", "urlHandler.urlHandler.UrlBaseHandler",{"a":3}),
    ])

if __name__ == "__main__":
    queue = Queue()
    queue.put("http://www.jianshu.com")
    worker = Worker(app,queue)
    worker._find_url_handler("http://www.jianshu.com/1234/4")
    print(worker)