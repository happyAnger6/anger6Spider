__author__ = 'zhangxa'

from tornado import gen
from tornado.platform.asyncio import to_asyncio_future,AsyncIOMainLoop
from tornado.httpclient import AsyncHTTPClient
import asyncio

@gen.coroutine
def tornado_coroutine():
    cli = AsyncHTTPClient()
    response = yield cli.fetch("http://www.baidu.com")
    print(response.body)

AsyncIOMainLoop().install()
asyncio.get_event_loop().run_until_complete(to_asyncio_future(tornado_coroutine()))
