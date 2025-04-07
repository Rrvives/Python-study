# 捕获全部的异常
try:
    file = open('aaa.txt', 'r', encoding="UTF-8")
except:
    file = open('aaa.txt', 'w', encoding="UTF-8")
    file.close()
    print(111)


# 捕获指定的异常
try:
    print(name)
except NameError as e:
    print('3333')


# 捕获多个异常

try:
    print(name)
    1/0
except (NameError, ZeroDivisionError) as e:
    print(e)


try:
    print('hellow')
except:
    print('出租哦')
else:
    print('没有发生异常时打印的语句')
finally:
    print('不管有没有出错，都会执行这句')