__author__ = 'zhangxa'

from anger6Spider.spiders.spider import BaseSpider
from anger6Spider.env import SpiderEnv
from anger6Spider.log4s import Log4Spider
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.curl_httpclient import AsyncHTTPClient,CurlAsyncHTTPClient
import pycurl

from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urlunparse

class TaobaoSpider(BaseSpider):
    def initialize(self,**kwargs):
        self.parse_url = True

    @gen.coroutine
    def _urlWork(self):
        driver = webdriver.Chrome()
        driver.get("http://www.taobao.com")
        pagesource = driver.page_source
        soup = BeautifulSoup(pagesource)
        print(soup)
        a_tags = soup.find_all()
        for a_tag in a_tags:
            attrs = a_tag.attrs
            for attr in attrs:
                Log4Spider.debugLog("tag: ",a_tag,"attr:",attr)
                if attr in ('href','src','#src','#src2'): #find a url,some url likes javascript:void(null) are not filter
                    url = url_path = a_tag[attr]
                    url_path = url_path.replace("//","/")
                    if url_path.startswith("/"):
                        url_parse = self.env['urlparse']
                        url = urlunparse([url_parse.scheme,url_parse.netloc,url_path,"","",""])
                    if url.startswith("http"):
                        if not self.parse_url_own or url_parse.netloc in url:
                            self._url_lists.append(url)
                    else:
                        Log4Spider.errLog("Find a unknown url:[[[",url,"]]]")
        driver.close()

    @gen.coroutine
    def realWork(self):
        AsyncHTTPClient.configure(CurlAsyncHTTPClient)
        def prepare_cul_opts(obj):
            obj.setopt(pycurl.WRITEFUNCTION,open("test.html","wb").write)
        httpCli = AsyncHTTPClient()
        yield httpCli.fetch(self.env['url'],prepare_curl_callback=prepare_cul_opts)

if __name__ == "__main__":
    @gen.coroutine
    def main():
        s_env = SpiderEnv("http://www.jd.com")
        env = yield s_env.gen_env()
        print(env)
        tbs = TaobaoSpider(env,None)
        yield tbs.work()
        for url in tbs.urlLists:
            Log4Spider.infoLog(url)

    IOLoop.instance().run_sync(main)

