__author__ = 'zhangxa'

from urllib.parse import urlparse,urlunparse

o = urlparse("http://search.jd.com/Search?keyword=python&enc=utf-8&wq=python&pvid=t63yw8ni.bqlsp9")
print(o.scheme)
print(urlunparse(["http","www.baidu.com","Search?keyword=python&enc=utf-8&wq=python&pvid=t63yw8ni.bqlsp9","","",""]))