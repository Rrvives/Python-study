class Student:
    # 里面的self相当于类本身 相当于js里面的this
    name = '测试'
    age = 18

    def test(self):
        print('test')

    def tes1(self):
        print(f'我是类的成员方法，我的年龄是{self.age}')

    def test3(self, params):
        print(f'我是类的成员方法，我的年龄是{self.age}', params)


data = Student()

print(data.tes1())

print(data.test3('参数'))
