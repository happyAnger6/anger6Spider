__author__ = 'zhangxa'

from curl import Curl
import pycurl
from download.DownFile import DownFile
from urlHandle.urlBaseHandler import UrlBaseHandler

#USER_AGENT="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
url = "http://upload-images.jianshu.io/upload_images/790541-fad4392a3025443f.jpg?imageMogr2/auto-orient/strip%7CimageView2/1/w/300/h/300"
handle = UrlBaseHandler(url)
info = handle.httpGet()
file_down = DownFile()
file_down.getFileNameByUrl(info['url'])
file_down.saveFile2Local(info['data'])
