__author__ = 'zhangxa'

from html.parser import HTMLParser
from log4Spider.log4s import Log4Spider

"""
BaseHtmlParse only parse all the data and sotrage them into a file
the file is given by called setParseFile on it
"""
class BaseHtmlParser(HTMLParser):

    def setParseFile(self,filename):
        self.file = open(filename,"wb")

    def recored(self,data):
        if isinstance(data,str):
            self.file.write((data).encode("UTF-8"))
        else:
            self.file.write((str(data)).encode("UTF-8"))

    def handle_starttag(self, tag, attrs):
        self.recored("start tag:[[[")
        self.recored(tag)
        self.recored("]]]")
        self.recored("attrs:[[[")
        self.recored(attrs)
        self.recored("]]]")

    def handle_endtag(self, tag):
        self.recored("end tag:[[[")
        self.recored(tag)
        self.recored("]]]")

    def handle_startendtag(self, tag, attrs):
        self.recored("startendtag:[[[")
        self.recored(tag)
        self.recored("]]]")
        self.recored("attrs:[[[")
        self.recored(attrs)
        self.recored("]]]")

    def handle_data(self, data):
        self.recored("data:[[[")
        self.recored(data)
        self.recored("]]]")

    def handle_comment(self, data):
        self.recored("comment:[[[")
        self.recored(data)
        self.recored("]]]")

    def handle_entityref(self, name):
        self.recored("entityref:[[[")
        self.recored(name)
        self.recored("]]]")

    def handle_charref(self, name):
        self.recored("charref:[[[")
        self.recored(name)
        self.recored("]]]")

    def handle_decl(self, decl):
        self.recored("decl:[[[")
        self.recored(decl)
        self.recored("]]]")

    # Overridable -- handle processing instruction
    def handle_pi(self, data):
        self.recored("pi:[[[")
        self.recored(data)
        self.recored("]]]")

"""
A UrlHtmlParse parse all the urls on the html page
You can register a hook function by call setUrlCallBack on it.The hook will called when a url find.
"""
class UrlHtmlParser(HTMLParser):
    def setUrlList(self,list):
        self._urlList = list

    def current_urlList(self):
        if not hasattr(self,"_urlList"):
            self._urlList = []
        return self._urlList

    def setUrlCallBack(self,func=None):
        self.dealUrl = func

    def parseUrlFromAttrs(self,attrs):
        for attr in attrs:
            if attr[0] in ("src","href","#src","#src2") and attr[1].startswith("http://"):
                url = attr[1]
                Log4Spider.infoLog(self,"url:[[[",url,"]]]","attr[[[",attr[0],"]]]")
                #self.current_urlList().append(url)
                if hasattr(self,'dealUrl') and self.dealUrl:
                    self.dealUrl(url)

    def handle_starttag(self, tag, attrs):
        self.parseUrlFromAttrs(attrs)

    def handle_startendtag(self, tag, attrs):
        self.parseUrlFromAttrs(attrs)

    @property
    def urlList(self):
        return self.current_urlList()

class JianShuUrlHtmlParser(HTMLParser):
    def setUrlList(self,list):
        self._urlList = list

    def current_urlList(self):
        if not hasattr(self,"_urlList"):
            self._urlList = []
        return self._urlList

    def setUrlCallBack(self,func=None):
        self.dealUrl = func

    def parseUrlFromAttrs(self,attrs):
        url = ""
        for attr in attrs:
            if attr[0] in ("src","href","#src","#src2"):
                if attr[1].startswith("http://www.jianshu.com"):
                    url = attr[1]
                elif attr[1].startswith("/"):
                    url = "http://www.jianshu.com"+attr[1]
                else:
                    continue
                Log4Spider.infoLog(self,"url:[[[",url,"]]]","attr[[[",attr[0],"]]]")
                #self.current_urlList().append(url)
                if hasattr(self,'dealUrl') and self.dealUrl:
                    self.dealUrl(url)

    def handle_starttag(self, tag, attrs):
        self.parseUrlFromAttrs(attrs)

    def handle_startendtag(self, tag, attrs):
        self.parseUrlFromAttrs(attrs)

    @property
    def urlList(self):
        return self.current_urlList()

class JianShuUserInfo_HtmlParser(HTMLParser):
    def __init__(self):
        self.h3 = 0
        self.clearfix=0
        self.infos = 0
        self.info = {}
        super().__init__(self)

    def setUrlList(self,list):
        self._urlList = list

    def current_urlList(self):
        if not hasattr(self,"_urlList"):
            self._urlList = []
        return self._urlList

    def setInfoHook(self,func=None):
        self.infoHook = func

    def parseUrlFromAttrs(self,attrs):
        pass

    def handle_starttag(self, tag, attrs):
        if tag == "h3":
            self.h3 = 1
        if tag == "ul":
            if attrs:
                attr = attrs[0]
                if attr[0] == "class" and attr[1] == "clearfix":
                    self.clearfix = 1
        if self.clearfix:
            if tag == "b":
                self.infos+=1

    def handle_data(self, data):
        if self.h3 == 1:
            self.info['name'] = data
        if self.clearfix:
            if self.infos == 1 and  'follows' not in self.info.keys():
                self.info['follows'] = int(data)
            if self.infos == 2 and  'fans' not in self.info.keys():
                self.info['fans'] = int(data)
            if self.infos == 3 and  'articles' not in self.info.keys():
                self.info['articles'] = int(data)
            if self.infos == 4 and 'words' not in self.info.keys():
                self.info['words'] = int(data)
            if self.infos == 5 and 'beliked' not in self.info.keys():
                self.info['beliked'] = int(data)

    def handle_endtag(self, tag):
        if tag == "h3":
            self.h3 = 0
        if self.clearfix and tag == "ul":
            self.clearfix = 0
            if hasattr(self,"infoHook"):
                self.infoHook(self.info)

    def handle_startendtag(self, tag, attrs):
         pass

    @property
    def urlList(self):
        return self.current_urlList()

if __name__ == "__main__":
    parser = JianShuUserInfo_HtmlParser();
    from curl import Curl
    import pycurl
    c = Curl()
    c.set_url("http://www.jianshu.com/users/d9edcb44e2f2/latest_articles")
    data = c.get()
    #parser.setParseFile("parse.txt")
    parser.setInfoHook(lambda info:print(str(info)))
    parser.feed(data.decode("utf-8"))
    parser.close()
    c.close()