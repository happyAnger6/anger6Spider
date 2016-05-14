__author__ = 'zhangxa'

from tornado.httpclient import AsyncHTTPClient
from tornado.curl_httpclient import CurlAsyncHTTPClient
from tornado import gen
from tornado.ioloop import IOLoop
from urllib.parse import urlparse
from anger6Spider.response import charset_from_content,mine_from_content
from bs4 import BeautifulSoup

import pycurl
"""
A SpiderEnv contains url,charset,mine(eg. ('image','png'),('text','html')),
text,soup,headers and urlparse.It can be used in a spider.
"""
class SpiderEnv:
    def __init__(self,url):
        self._url = url
        self._env = {"url":url}

    @gen.coroutine
    def gen_env(self):
        AsyncHTTPClient.configure(CurlAsyncHTTPClient)
        def prepare_cul_opts(obj):
            obj.setopt(pycurl.NOBODY,True)

        httpCli = AsyncHTTPClient()
        response = yield httpCli.fetch(self._url,prepare_curl_callback=prepare_cul_opts)
        for name,value in response.headers.get_all():
            if name.lower().startswith('content-type'):
                self._env['charset'] = charset_from_content(value)
                self._env['mine'] = mine_from_content(value)
        self._env['headers'] = response.headers.get_all()
        self._env['urlparse'] = urlparse(self._url)
        return self._env

    @property
    def env(self):
        return self._env

if __name__ == "__main__":
    #env = SpiderEnv("http://static.360buyimg.com/item/main/1.0.16/css/i/item.sprite.png")
    #env = SpiderEnv("http://www.jd.com")
    #env = SpiderEnv("http://www.jianshu.com")
    @gen.coroutine
    def main():
        for url in ["http://static.360buyimg.com/item/main/1.0.16/css/i/item.sprite.png","http://www.jd.com",
                    "http://www.jianshu.com"]:
            env = SpiderEnv(url)
            yield env.gen_env()
            print(env.env['mine'])
            print(env.env['urlparse'])

    IOLoop.instance().run_sync(main)

