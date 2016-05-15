__author__ = 'zhangxa'

"""
This is a test programe used to test web page like 'http://list.jd.com/list.html?cat=.*'
Use bs4 to parse the page
"""

from bs4 import BeautifulSoup

from tornado.httpclient import AsyncHTTPClient
from tornado import gen
from tornado.ioloop import IOLoop

from selenium import webdriver
import re

urls = ["http://search.jd.com/Search?keyword=Python&enc=utf-8&book=y&wq=Python&pvid=33xo9lni.p4a1qb",
        "http://search.jd.com/search?keyword=Python&enc=utf-8&qrst=1&rt=1&stop=1&book=y&vt=2&cid3=3649#J_crumbsBar"]

def parse_info_from_soup(bs):
    items = bs.find_all("li",class_="gl-item")   #查找所有class为"gl-item"，标签名为li的标签
    for item in items: #遍历所有标签
        name = item.find("div",class_="p-name").find("em") #查找class为"p-name",标签名为div的标签，并查找em内容
        price = item.find("div",class_="p-price").find("i") #查找价格
        book_detail = item.find("span",class_="p-bi-store").find("a") #查找出版社
        commit = item.find("div",class_="p-commit").find("a") #查找评论人数
        print(name.text,book_detail.text,price.text,commit.text)
    print(len(items))

@gen.coroutine
def main():
    cli = AsyncHTTPClient()
    for url in urls:
        response = yield cli.fetch(url) #用tornado的AsyncHTTPClient来下载页面
        bs = BeautifulSoup(response.body) #将页面信息转换为BeautifulSoup对象
        parse_info_from_soup(bs) #从页面中提取信息

@gen.coroutine
def main1():
    driver = webdriver.PhantomJS(executable_path="/usr/bin/phantomjs")
    for url in urls:
        driver.get(url)  #通过无头浏览器PhantomJS下载页面
        bs = BeautifulSoup(driver.page_source)  #将页面信息转换为BeautifulSoup对象
        parse_info_from_soup(bs) #从页面中提取信息

if __name__ == "__main__":
    IOLoop.instance().run_sync(main1)