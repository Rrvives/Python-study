# 装饰器也是闭包的一种
# 装饰器可以理解成是一个高阶的函数

def decorator(func):
    def inner():
        print('1')
        func()
        print('2')

    return inner


def test1():
    print('test1')


fn = decorator(test1)
fn()
