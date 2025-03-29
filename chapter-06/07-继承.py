# 类的继承
# 继承的特性 在继承的属性里面 在使用的时候 优先使用自身的属性 自身没有了才会去继承的类里面去查找
# 私有属性和方法不会被继承
# 可以继承多个类 当继承的类里面有相同的属性和方法 按照继承的优先级选 优先级是继承的顺序
class Animal:
    __age = 18
    def __init__(self, name):
        self.name = name

    def eat(self):
        print('{} is eating'.format(self.name))

    def sleep(self):
        print('{} is sleeping'.format(self.name))

class Cat(Animal):
    # pass  这个属性相当于自身没有属性 属性和方法全部来自继承的类
    def __init__(self, name):
        super().__init__(name)

    # 这个属性父类里面也有这个属性 子类里面也有这个属性 这样也算是都父类属性的复写 当父类里面的属性不满足当前条件时
    # 可以重新改写这个方法
    def eat(self):
        print('{} is eating11111'.format(self.name))

    def sleep(self):
        print('{} is sleeping'.format(self.name))

    def catch(self):

        print('{} is catching'.format(self.name))


data = Cat('小黑')
print(data.eat())
print(data.catch())