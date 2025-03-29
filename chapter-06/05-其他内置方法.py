# 内置方法一般有 也成魔术方法
# 简单的讲 python的魔术方法 会改变类里面一些内置方法执行 比如js里面有内置的toString()方法 然后在尾部可以
# 直接使用， 如果不想使用它内置的方法，那么可以在类里面重写它， 那么就可以使用我们重写的方法了

# __init__()方法
# __str__()方法  字符串方法 类对象转换为字符串的行为
# __lt__()方法 小于符号的比较
# __len__()方法
# __add__()方法
# __eq__()方法
# __getitem__()方法

class Student:
    # 这两个参数也可以不用定义 可以直接在__init__()方法里面使用
    name = None
    age = None

    def __init__(self, name, age):
        self.name = name
        self.age = age

    # str的魔术方法  当我在这里重写该方法之后  在重新打印
    def __str__(self):
        return f'{self.name} {self.age}'

data = Student('张三', 18)

# print(data) # <__main__.Student object at 0x000001D0C0A0EA90> 打印的是内存地址

# print(str(data)) #这个也是内存地址

# 重写之后的str属性
print(str(data))