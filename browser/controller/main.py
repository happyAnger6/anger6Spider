__author__ = 'zhangxa'

#coding=utf-8
__author__ = 'phithon'
import tornado.web
from tornado import gen
import pymongo

class HomeHandler(tornado.web.RequestHandler):
	def initialize(self):
		self.db = self.settings.get("database")
		self.backend = self.settings.get("thread_pool")
		self.topbar = "home"

	def pagenav(self, count, url, each, now,
		pre = '<ul class="am-pagination am-fr admin-content-pagination">', end = '</ul>'):
		_ret = ''
		_pre = pre
		_end = end
		page = (int(count / each) + 1) if (count % each != 0) else (count / each)
		i = now - 5
		while (i <= now + 5) and (i <= page):
			if i > 0:
				if now == i:
					_url = url % i
					_ret += '<li class="am-active"><a class="am-link-muted" href="%s">%d</a></li>' % (_url, i)
				else:
					_url = url % i
					_ret += '<li><a class="am-link-muted" href="%s">%d</a></li>' % (_url, i)
			i += 1
		if now > 6:
			_url = url % 1
			_ret = u'<li><a class="am-link-muted" href="%s">首页</a></li><li class="am-disabled"><a href="#">...</a></li>%s' % (_url, _ret)
		if now + 5 < page:
			_url = url % page
			_ret = u'%s<li class="am-disabled"><a href="#">...</a></li><li><a class="am-link-muted" href="%s">尾页</a></li>' % (_ret, _url)
		if page <= 1:
			_ret = ''
		_ret = _pre + _ret + _end
		return _ret

	@tornado.web.asynchronous
	@gen.coroutine
	def get(self, *args, **kwargs):
		def intval(str):
			'''
			如php中的intval，将字符串强制转换成数字

			:param str: 输入的字符串
			:return: 数字
			'''
			import re
			if type(str) is int: return str
			try:
				ret = re.match(r"^(\-?\d+)[^\d]?.*$", str).group(1)
				ret = int(ret)
			except:
				ret = 0
			return ret
		limit = 25
		page = intval(args[1])
		if not page or page <= 0 : page = 1
		cursor = self.db.jianshu_users.find()
		total = yield cursor.count()
		cursor.sort([('fans',pymongo.DESCENDING)]).limit(limit).skip((page - 1) * limit)
		count = yield cursor.count()
		users = yield cursor.to_list(length = limit)
		self.render("main.htm", users = users,page = page,total=total,
					count = count, each = limit,pagenav=self.pagenav)