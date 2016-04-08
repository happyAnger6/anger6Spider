#coding=utf-8
__author__ = 'zhangxa'

from curl import Curl
import pycurl

from html.parser import HTMLParser
from download.DownFile import down_file

USER_AGENT="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"

c = Curl()
c.set_url("http://www.jianshu.com/")
c.set_option(pycurl.USERAGENT,USER_AGENT)
data = c.get()
class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
       pass

    def handle_startendtag(self, tag, attrs):
        if tag == "img":
            for attr in attrs:
                if attr[0] == 'src':
                    url = attr[1].split('/')
                    for ele in url:
                        if 'jpg' in ele.lower():
                            down_file(attr[1],ele.split('?')[0])

    def handle_data(self, data):
        pass

    def handle_comment(self, data):
        pass

    def handle_entityref(self, name):
        pass

    def handle_charref(self, name):
        pass

parser = MyHTMLParser()
parser.feed(data.decode("UTF-8"))
parser.close()






