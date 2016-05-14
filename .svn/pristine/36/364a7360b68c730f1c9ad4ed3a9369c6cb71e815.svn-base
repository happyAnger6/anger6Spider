__author__ = 'zhangxa'

from tornado.httpclient import AsyncHTTPClient
from tornado import gen
from tornado.ioloop import IOLoop
import functools
from bs4 import BeautifulSoup

def get_charset(content_type):
    try:
        lct = content_type.lower()
        c_c = lct[lct.index("charset="):]
        return c_c[len("charset="):]
    except:
        return 'UTF-8'

@gen.coroutine
def fetch_url(url):
    respone = yield AsyncHTTPClient().fetch(url)
    charset = get_charset(respone.headers['content-type'])
    soup = BeautifulSoup(respone.body)
    print(soup.prettify(encoding=charset))

ioLoop = IOLoop.current().instance()
ioLoop.run_sync(functools.partial(fetch_url,"http://www.jianshu.com"))