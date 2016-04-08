__author__ = 'zhangxa'

from curl import Curl
import pycurl


def down_file(url,dest):
    USER_AGENT="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
    c = Curl()
    c.set_url(url)
    c.set_option(pycurl.USERAGENT,USER_AGENT)
    with open(dest,"wb") as output:
         c.set_option(pycurl.WRITEFUNCTION,output.write)
         c.get()
         c.close()

