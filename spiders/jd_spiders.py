__author__ = 'zhangxa'
from anger6Spider.spiders.spider import BaseSpider
from anger6Spider.application import Application
from anger6Spider.env import SpiderEnv
from anger6Spider.log4s import Log4Spider
from selenium import webdriver

from tornado import gen
from tornado.locks import Event
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains

import re

re_price = re.compile(r"[\d\.]{1,}")

"""
A base spider only parse the urls in a html page.
"""
class Jd_BaseSpider(BaseSpider):

    def initialize(self, **kwargs):
        super().initialize(**kwargs)
        self.db = self.app.settings['database']

    @gen.coroutine
    def work(self):
        exec = self.app.executor
        try:
            driver = webdriver.PhantomJS(executable_path="/usr/bin/phantomjs")
            yield exec.submit(driver.get,self.env['url'])
            yield self.scrapy(driver)
        except Exception as e:
            Log4Spider.errLog(self,"webdriver.PhantomJS failed: ",e)


    @gen.coroutine
    def scrapy(self,driver):
        pagesource = driver.page_source
        bs = BeautifulSoup(pagesource)
        self.getUrlBySoup(bs)

"""
A spider to parse www.jd.com.
use selinum's ActionChains to hover on left items to show all the hiden pages.
"""
class Jd_Home_Spider(Jd_BaseSpider):
    @gen.coroutine
    def scrapy(self,driver):
        exec = self.app.executor
        css_div = 'div[class="%s"] h3'%('dd-inner')
        div_book = yield exec.submit(driver.find_elements_by_css_selector,css_div)
        for h in div_book:
            ActionChains(driver).move_to_element(h).perform()
        super().scrapy(driver)


class Jd_Channel_Spider(Jd_BaseSpider):
    @gen.coroutine
    def scrapy(self, driver):
        exec = self.app.executor
        css_div = 'div[class="%s"] h3'%('item-inner')
        div_book = yield exec.submit(driver.find_elements_by_css_selector,css_div)
        for h in div_book:
            ActionChains(driver).move_to_element(h).perform()
        super().scrapy(driver)

class Jd_List_Spider(Jd_BaseSpider):
    @gen.coroutine
    def scrapy(self, driver):
        exec = self.app.executor

        #css_div = 'div[class="%s"] h3'%('item-inner')
        #div_book = yield exec.submit(driver.find_elements_by_css_selector,css_div)
        #for h in div_book:
         #   ActionChains(driver).move_to_element(h).perform()
        pagesource = driver.page_source
        bs = BeautifulSoup(pagesource)
        eles = bs.findAll("div",{"class":"p-name"})
        prices = bs.findAll("div",{"class":"p-price"})
        for price in prices:
            i = price.find("i")
            if i:
                print(i.text)
        for ele,price in zip(eles,prices):
            Log4Spider.dataLog(ele.text,price.text)
        super().scrapy(driver)

"""
A spider scrapy a book info from a url like:http://item.jd.com/[0-9]*.html
"""
class Jd_Item_Spider(Jd_BaseSpider):
    @gen.coroutine
    def scrapy(self,driver):
        bs = BeautifulSoup(driver.page_source)
        item = bs.find("div",id="product-intro").find("div",id="itemInfo")
        name = item.find("div",id="name").find("h1").text
        price = item.find("div",id="summary-price").find("strong",class_="p-price").text
        #print(price)
        price = re_price.search(price).group()
        discount = item.find("div",id="summary-price").find("span",class_="p-discount").text
        #print(discount)
        discount = re_price.search(discount).group()
        #print(name,price,discount)
        Log4Spider.dataLog("insert a shop",name,price,discount)
        self.db.shops.insert({"name":name,"price":price,"discount":discount})
        super().scrapy(driver)


if __name__ == "__main__":
    url_lst = ["http://list.jd.com/list.html?cat=1713,3287,3800&ev=87812_555207",
               "http://channel.jd.com/1713-3286.html",
               "http://channel.jd.com/1713-3287.html"
                ]

    url_items = ["http://item.jd.com/10064429.html",
                 "http://item.jd.com/11075150.html"]

    app = Application([
        (r"^.*$", "anger6Spider.spiders.jd_spiders.Jd_Item_Spider"),
    ])

    num = 0
    event = Event()

    @gen.coroutine
    def main():
        global num
        for url in url_items:
            num+=1
            fetch_one_url(url)
        yield event.wait()
        print("end")

    @gen.coroutine
    def fetch_one_url(url):
        env_obj = SpiderEnv(url)
        env = yield env_obj.gen_env()
        urlSeek = Jd_Item_Spider(env,app)
        yield urlSeek.work()
        for url in urlSeek.urlLists:
           Log4Spider.infoLog(url)
        Log4Spider.infoLog(len(urlSeek.urlLists))
        global num
        num-=1
        if num == 0:
            event.set()


    from tornado.ioloop import IOLoop
    IOLoop.instance().run_sync(main)