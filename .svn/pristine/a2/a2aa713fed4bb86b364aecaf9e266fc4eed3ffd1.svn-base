__author__ = 'zhangxa'

from urllib.parse import urlparse

find_str="http://upload-images.jianshu.io/upload_images/1679702-7e810a34f3ef8d18.jpg?imageMogr2/auto-orient/strip%7CimageView2/1/w/300/h/300"
ret = urlparse(find_str)
print(ret)
path = ret.path
print(ret.netloc + path.replace("/","-"))