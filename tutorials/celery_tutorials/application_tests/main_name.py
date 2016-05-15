__author__ = 'zhangxa'

from celery import Celery
app = Celery()

@app.task
def add(x,y):
    return x + y

print(add)
print(add.name)

"""
if you import this py as a module,the __main__.add will be not existed and cause a exception
"""
#print(app.tasks['__main__.add'])

if __name__ == "__main__":
    print(add)
    app.worker_main()
