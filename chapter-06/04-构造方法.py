# 构造方法
# __init__()方法
# 特性： 1、会自动执行  2、外部传递进来的参数胡赋值给__init__()方法里面定义的变量

class Student:
    # 这两个参数也可以不用定义 可以直接在__init__()方法里面使用
    name = None
    age = None

    def __init__(self, name, age):
        self.name = name
        self.age = age


data = Student('张三', 18)

print(data.name)
