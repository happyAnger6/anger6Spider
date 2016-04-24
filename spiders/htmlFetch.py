__author__ = 'zhangxa'
from tornado.httpclient import AsyncHTTPClient
from tornado import gen
from bs4 import BeautifulSoup

from anger6Spider.log4s import Log4Spider
@gen.coroutine
def fetch_html(url):
    http_cli = AsyncHTTPClient()
    respone = yield http_cli.fetch(url)
    return respone

class HtmlFetch:
    def __init__(self,url):
        self._url = url

    @gen.coroutine
    def fetch(self):
        result = {}
        res = yield fetch_html(self._url)
        result['header'] = res.headers
        soup = BeautifulSoup(res.body)
        result['soup'] = soup
        return result


if __name__ == "__main__":
    base_url = "http://www.163.com"

    @gen.coroutine
    def main():
        parse = HtmlFetch(base_url)
        result = yield parse.fetch()
        Log4Spider.infoLog(result)

    from tornado.ioloop import IOLoop
    IOLoop.instance().current().run_sync(main)