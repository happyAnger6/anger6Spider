__author__ = 'zhangxa'

from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from bs4 import BeautifulSoup
from tornado import gen


thread_pool = ThreadPoolExecutor(4)


@gen.coroutine
def fetch_url(url):
    driver = webdriver.PhantomJS("/usr/bin/phantomjs")
    response = yield thread_pool.submit(driver.get,url)
    pagesource = driver.page_source
    bs = BeautifulSoup(pagesource)
    print("url:%s done"%url)
    driver.close()

@gen.coroutine
def main():
    urllists = ["http://channel.jd.com/1713-3287.html","http://e.jd.com/ebook.html","http://e.jd.com/rank/5272-0-2-1.html"]
    for url in urllists:
        fetch_url(url)

    yield gen.sleep(10)

if __name__ == "__main__":
    from tornado.ioloop import IOLoop
    IOLoop.instance().run_sync(main)
    
