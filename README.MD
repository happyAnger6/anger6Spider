还在改进完善中，现在只是一个demo版本，仅仅实现下载页面中的图片功能.

实现:
python实现的网络爬虫
基于tornado,redis,mongodb实现
利用协程和tornado异步库高效地爬取页面

抓取到的url存储在redis中

数据存储在mongodb中

html解析部分使用beautifulsoup


特点:
可以通过定制对不同的URL采用不同的爬虫进行抓取
举例:
app = Application([
        (r"^http://www.baidu.com.*$", "anger6Spider.spiders.spider.BaseSpider"),
        (r"^http://www.jianshu.com.*$", "anger6Spider.spiders.spider.UrlSeekSpider"),
    ])
	

软件依懒:	
python使用3.4.4版本
tornado版本4.3

pip install tornado
pip install pycurl
pip install beautifulsoup
pip install redis
pip install motor

运行:
python anger6Spider/worker.py