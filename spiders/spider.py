__author__ = 'zhangxa'


from anger6Spider.log4s import Log4Spider
from anger6Spider.env import SpiderEnv
from tornado.ioloop import IOLoop
from tornado.httpclient import AsyncHTTPClient
from tornado.curl_httpclient import CurlAsyncHTTPClient
from tornado import gen

from bs4 import BeautifulSoup
from urllib.parse import urlunparse

import pycurl
from urllib.parse import urlparse
"""
A BaseSpider only parse all the urls in a html and store it in _url_lists which can be get by call urlLists.
if a subclass want to do something else he should override the realWork function.
if a subclass do't want to parse urls he should override the initialize function and set the parse_url flag to be False.
"""
class BaseSpider:
    def __init__(self,env,application,**kwargs):
        self.env = env
        self.app = application
        self._url_lists = []
        self.parse_url = False
        if 'text' in self.env['mine']:   #we only parse url in a page when the content-type is text/html.
            self.parse_url = True
        self.initialize(**kwargs)

    #a hook for subclass to initialize
    def initialize(self,**kwargs):
        pass

    @gen.coroutine
    def work(self):
        if self.parse_url:
             yield self._urlWork()
        yield self.realWork()

    #a hook subclass to do what he really want to do
    @gen.coroutine
    def realWork(self):
        pass

    @gen.coroutine
    def _urlWork(self):
        AsyncHTTPClient.configure(CurlAsyncHTTPClient)
        httpCli = AsyncHTTPClient()
        try:
            respone = yield httpCli.fetch(self.env['url'])
        except Exception as e:
            Log4Spider.errLog("urlWork fetch url: ",self.env['url'],"error exception: ",e)
            return
        soup = BeautifulSoup(respone.body)
        a_tags = soup.find_all()
        for a_tag in a_tags:
            attrs = a_tag.attrs
            for attr in attrs:
                if attr in ('href','src','#src','#src2'): #find a url,some url likes javascript:void(null) are not filter
                    url = url_path = a_tag[attr]
                    if url_path.startswith("/"):
                        url_parse = self.env['urlparse']
                        url = urlunparse([url_parse.scheme,url_parse.netloc,url_path,"","",""])
                    if url.startswith("http"):
                        self._url_lists.append(url)
                    else:
                        Log4Spider.errLog("Find a unknown url:[[[",url,"]]]")

    @property
    def urlLists(self):
        return self._url_lists

"""
A UrlSeekSpider only parse all the urls in a html page.
"""
class UrlSeekSpider(BaseSpider):
    pass

class PicDownSpider(BaseSpider):
    @gen.coroutine
    def realWork(self):
        if self.env['mine'][1] in ('jpg','jpeg','png','gif'):
            AsyncHTTPClient.configure(CurlAsyncHTTPClient)
            def prepare_cul_opts(obj):
                parse = urlparse(self.env['url'])
                path = parse.path
                pic_name = parse.netloc + path.replace("/","-")
                Log4Spider.warnLog("PicDown url: ",self.env['url'])
                obj.setopt(pycurl.WRITEFUNCTION,open(pic_name,"wb").write)
            httpCli = AsyncHTTPClient()
            try:
                respone = yield httpCli.fetch(self.env['url'],prepare_curl_callback=prepare_cul_opts)
            except Exception as e:
                Log4Spider.errLog("PicDown failed url: ",self.env['url'],"error exception: ",e)
                return

if __name__ == "__main__": #this test case just parse one html page
    base_url = "http://www.jianshu.com"
    @gen.coroutine
    def main():
       for url in [ "http://www.jianshu.com",
                    "http://upload-images.jianshu.io/upload_images/1679702-7e810a34f3ef8d18.jpg?imageMogr2/auto-orient/strip%7CimageView2/1/w/300/h/300"
                    ]:
        env_obj = SpiderEnv(url)
        env = yield env_obj.gen_env()
        urlSeek = UrlSeekSpider(env,None)
        yield urlSeek.work()
        for url in urlSeek.urlLists:
           Log4Spider.infoLog(url)
        Log4Spider.infoLog(len(urlSeek.urlLists))

    @gen.coroutine
    def downPicTest():
        for url in ["http://upload-images.jianshu.io/upload_images/1679702-7e810a34f3ef8d18.jpg?imageMogr2/auto-orient/strip%7CimageView2/1/w/300/h/300",
                    "https://asearch.alicdn.com/bao/uploaded/i1/146280142867863617/TB2.atGhFXXXXcoXXXXXXXXXXXX_!!15874628-0-saturn_solar.jpg_210x210.jpg",
                    "http://pic18.wed114.cn/20140923/2014092312515083.jpg"]:
            env_obj = SpiderEnv(url)
            env = yield env_obj.gen_env()
            spider = PicDownSpider(env,None)
            yield spider.work()

    IOLoop.current().instance().run_sync(downPicTest)