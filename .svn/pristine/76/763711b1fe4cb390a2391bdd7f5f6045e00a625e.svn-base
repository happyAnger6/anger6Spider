__author__ = 'zhangxa'

from selenium import webdriver
from bs4 import BeautifulSoup

import time

driver = webdriver.PhantomJS(executable_path="/usr/bin/phantomjs")
driver.get("http://www.jd.com")
#time.sleep(6)
pagesource = driver.page_source
bs = BeautifulSoup(pagesource)
print(bs)
driver.close()