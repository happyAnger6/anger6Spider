__author__ = 'zhangxa'

import redis

from tornado import gen
from anger6Spider.spiderQueue.driver import QueueDriver,QueueEmpty
from tornado.concurrent import Future
from tornado import ioloop

def _set_timeout(future, timeout):
    if timeout:
        def on_timeout():
            future.set_exception(gen.TimeoutError())
        io_loop = ioloop.IOLoop.current()
        timeout_handle = io_loop.add_timeout(timeout, on_timeout)
        future.add_done_callback(
            lambda _: io_loop.remove_timeout(timeout_handle))

class RedisQueue(QueueDriver):
    VISITING = "list_url_visiting"
    VISITED = "set_url_visited"
    VISITING_NUM = "str_url_num"
    def save(self):
        self.client.save()

    def _get_internal(self):
        try:
            if self._getters:
                url = self.get_nowait()
                getter = self._getters.popleft()
                getter.set_result(url)
        except QueueEmpty:
            pass

    def get(self,timeout=None):
        future = Future()
        try:
            future.set_result(self.get_nowait())
        except QueueEmpty:
            self._getters.append(future)
            _set_timeout(future,timeout)
        return future


    def get_nowait(self):
        url = self.client.lpop(RedisQueue.VISITING)
        if not url:
            raise QueueEmpty
        self.client.decr(RedisQueue.VISITING_NUM)
        while self.client.sismember(RedisQueue.VISITED,url):
            url = self.client.lpop(RedisQueue.VISITING)
            if not url:
                break
            self.client.decr(RedisQueue.VISITING_NUM)
        if url:
            self.client.sadd(RedisQueue.VISITED,url)
            return url.decode("UTF-8")
        else:
            raise QueueEmpty


    @gen.coroutine
    def put(self,item):
        if not self.client.sismember(RedisQueue.VISITED,item):
            self.client.rpush(RedisQueue.VISITING,item)
            self.client.incr(RedisQueue.VISITING_NUM)
            self._get_internal() #if have a getter blocked,try to wake it up.

    def _create_redis_cli(self):
        if not hasattr(self,'client'):
            settings = self.settings
            self.client = redis.Redis(**settings)



if __name__ == "__main__":
    settings = {
                "host": "localhost",
                "port": 6379,
                "db": 1
    }

    from tornado import gen
    from tornado.ioloop import IOLoop
    from datetime import timedelta
    @gen.coroutine
    def main():
        q = RedisQueue(**settings)
        q._create_redis_cli()
        q.put("www.baidu.com")
        q.put("www.baidu.com")
        q.put("www.jd.com")
        q.put("www.jd.com")
        q.put("www.163.com")
        q.put("www.163.com")
        for _ in range(10):
            print(q.get())
        yield q.join(timeout=timedelta(seconds=10))
        print("done")

    @gen.coroutine
    def q_test():
        q = RedisQueue(**settings)
        q._create_redis_cli()

        @gen.coroutine
        def get_test():
            f = yield q.get(timeout=timedelta(seconds=5))
            print(f)

        @gen.coroutine
        def put_test():
            yield q.put("www.baidu2.com")

        get_test()
        put_test()
        yield q.join(timeout=timedelta(seconds=8))

    IOLoop.instance().run_sync(q_test)

