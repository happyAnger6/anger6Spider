__author__ = 'zhangxa'

import sys
sys.path.append("../..")
"""
Configures the `AsyncHTTPClient` subclass to use.

``AsyncHTTPClient()`` actually creates an instance of a subclass.
This method may be called with either a class object or the
fully-qualified name of such a class (or ``None`` to use the default,
``SimpleAsyncHTTPClient``)

If additional keyword arguments are given, they will be passed
to the constructor of each subclass instance created.  The
keyword argument ``max_clients`` determines the maximum number
of simultaneous `~AsyncHTTPClient.fetch()` operations that can
execute in parallel on each `.IOLoop`.  Additional arguments
may be supported depending on the implementation class in use.

Example::

   AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")
"""
from tornado.httpclient import AsyncHTTPClient
from tornado.curl_httpclient import CurlAsyncHTTPClient
from tornado import gen
from tornado.ioloop import IOLoop
from anger6Spider.response import parse_headers
from anger6Spider.log4s import Log4Spider
from bs4 import BeautifulSoup
import pycurl
import re

re_price = re.compile(r"[\d\.]{1,}")

@gen.coroutine
def main():
    def scrapy(body):
        bs = BeautifulSoup(body)
        print(bs)
        item = bs.find("div",id="product-intro").find("div",id="itemInfo")
        name = item.find("div",id="name").find("h1").text
        price = item.find("div",id="summary-price").find("strong",class_="p-price").text
        #print(price)
        price = re_price.search(price).group()
        discount = item.find("div",id="summary-price").find("span",class_="p-discount").text
        #print(discount)
        discount = re_price.search(discount).group()
        #print(name,price,discount)
        print("insert a shop(%s,%s,%s)"%(name,price,discount))



    def prepare_cul_opts(obj):
        pass
        #obj.setopt(pycurl.WRITEFUNCTION,open("result.html","wb").write)
        #obj.setopt(pycurl.NOBODY,True)
    #url="http://upload-images.jianshu.io/upload_images/1679702-7e810a34f3ef8d18.jpg?imageMogr2/auto-orient/strip%7CimageView2/1/w/300/h/300"
    AsyncHTTPClient.configure(CurlAsyncHTTPClient)
    for url in ["http://item.jd.com/11917788.html"]:
        httpCli = AsyncHTTPClient()
        respone = yield httpCli.fetch(url,prepare_curl_callback=prepare_cul_opts)
        scrapy(respone.body)
        print(list(respone.headers.get_all()))

if __name__ == "__main__":
    IOLoop.current().instance().run_sync(main)

