__author__ = 'zhangxa'

from curl import Curl
import pycurl

from log4Spider.log4s import Log4Spider

"""
A class used to down an pictures which contains 'jpg','png','gif'
"""
class DownFile:
    def __init__(self):
        self.filename = ""

    def getFileNameByUrl(self,url):
        splits = url.split('/')
        for step in splits:
            for suffix in ('jpg','png','gif'):
                if suffix in step:
                    self.filename = step[:step.rfind('.%s'%suffix)]+".%s"%suffix
                    break

    def saveFile2Local(self,url):
        self.getFileNameByUrl(url)
        if self.filename:
            with open(self.filename,"wb") as output:
                curl = Curl()
                curl.set_url(url)
                curl.set_option(pycurl.WRITEFUNCTION,output.write)
                curl.get()
                curl.close()
                Log4Spider.downLog(self,"downloaded a file:[[[",self.filename,"]]]")

if __name__ == "__main__":
    downf = DownFile()
    downf.saveFile2Local("http://upload-images.jianshu.io/upload_images/1679702-7e810a34f3ef8d18.jpg?imageMogr2/auto-orient/strip%7CimageView2/1/w/300/h/300")