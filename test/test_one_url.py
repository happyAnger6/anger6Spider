__author__ = 'zhangxa'

from curl import Curl
import pycurl

from html.parser import HTMLParser
from htmlParser.htmlParser import UrlHtmlParser
from download.downFile import DownFile
from urlHandler.urlHandler import UrlBaseHandler
from urlQueue.urlQueue import UrlQueue

start_url = "http://www.pcgames.com.cn/"
c = Curl()
c.set_url(start_url)
data = c.get()
info = c.info()
#print(info)

def get_charset(c_type):
    charset=None
    try:
        if c_type and 'charset' in c_type:
            start = c_type.find('charset=')
            charset_str = c_type[start:]
            end = charset_str.find(' ')
            if end > -1:
                charset = charset_str[len('charset='):end]
            else:
                charset = charset_str[len('charset='):]
    except:
        return 'UTF-8'
    if charset == None:
        return 'UTF-8'

#print(get_charset('text/html charset=gb2312 UTF-9'))
print(get_charset(info['content-type']))
parser = HTMLParser()
parser.feed(data.decode("GBK"))
c.close()