__author__ = 'zhangxa'


def yield_func(n):
    for i in range(n):
        x = yield i
        print(x)

gen = yield_func(10)

next = gen.send(next(gen)) #return next yield
print(next)