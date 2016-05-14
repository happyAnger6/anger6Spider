__author__ = 'zhangxa'
from anger6Spider.spiders.spider import BaseSpider
from anger6Spider.application import Application
from anger6Spider.env import SpiderEnv
from anger6Spider.log4s import Log4Spider
from selenium import webdriver

from tornado import gen
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains

class Jd_BaseSpider(BaseSpider):

    def initialize(self, **kwargs):
        super().initialize(**kwargs)
        #self.db = self.app.settings['database']
        #print("db",self.db)

    @gen.coroutine
    def work(self):
        exec = self.app.executor
        driver = webdriver.PhantomJS(executable_path="/usr/bin/phantomjs")
        yield exec.submit(driver.get,self.env['url'])
        yield self.scrapy(driver)


    @gen.coroutine
    def scrapy(self,driver):
        pagesource = driver.page_source
        bs = BeautifulSoup(pagesource)
        self.getUrlBySoup(bs)

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


if __name__ == "__main__":
    url_lst = ["http://list.jd.com/list.html?cat=1713,3287,3800&ev=87812_555207",
               "http://list.jd.com/list.html?cat=6233%2C6235%2C6245",
               "http://list.jd.com/list.html?cat=1672%2C2577%2C2589"]
    app = Application([
        (r"^.*$", "anger6Spider.spiders.jd_spiders.Jd_List_Spider"),
    ])

    @gen.coroutine
    def main():
        for url in url_lst:
            fetch_one_url(url)
        yield gen.sleep(10)

    @gen.coroutine
    def fetch_one_url(url):
        env_obj = SpiderEnv(url)
        env = yield env_obj.gen_env()
        urlSeek = Jd_List_Spider(env,app)
        yield urlSeek.work()
        for url in urlSeek.urlLists:
           Log4Spider.infoLog(url)
        Log4Spider.infoLog(len(urlSeek.urlLists))

    from tornado.ioloop import IOLoop
    IOLoop.instance().run_sync(main)