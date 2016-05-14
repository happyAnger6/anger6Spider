__author__ = 'zhangxa'

from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado import ioloop

url = "http://www.baidu.com"

@gen.coroutine
def fetch_url():
    httpClient = AsyncHTTPClient()
    respond = yield httpClient.fetch(url)
    print(respond)
    #raise gen.Return([])

if __name__ == '__main__':
    io_loop = ioloop.IOLoop.current()
    io_loop.run_sync(fetch_url)

