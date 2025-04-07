# 多态 同一的方法名，不同的功能
class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(self.name + '正在吃')


class Dog(Animal):
    def eat(self):
        print(self.name + '正在吃狗粮')


class Cat(Animal):
    def eat(self):
        print(self.name + '正在吃猫粮')


dog = Dog('旺财')
dog.eat()

cat = Cat('小花')
cat.eat()