__author__ = 'zhangxa'

def func(**kwargs):
    kwargs.update({"url":"www.baidu.com"})
    print(kwargs)

func(x=3,y=4)
