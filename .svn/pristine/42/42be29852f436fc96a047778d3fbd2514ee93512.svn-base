__author__ = 'zhangxa'

from tornado.ioloop import IOLoop
from tornado.httpclient import AsyncHTTPClient

async def fetch_coroutine():
    http_cli = AsyncHTTPClient()
    reponse = await http_cli.fetch("http://www.baidu.com")
    print(reponse.body)

IOLoop.instance().run_sync(fetch_coroutine)
