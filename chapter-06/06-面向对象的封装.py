# 面向对象的封装和js的类定义差不多 在python里面私有成员使用__开头
# 有私有属性和公共属性

class Student:
    name = '测试数据'
    __age = 18 # 前面添加__表明该属性是私有属性

    def __test(self):
        return '私有方法'

    def test1(self):
        data1 = self.__test()
        print(data1)
        return f'私有方法{self.name}'



data = Student()
print(data.name)
# print(data.test) 这样也会报错
# print(data.age)  这样会报错

print(data.test1())