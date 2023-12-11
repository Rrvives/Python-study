# set 集合 和 js差不多 都是不可重复 用{}表示  乱序

test = {'name', 'age', }

# 1、添加新元素add  会改变原数据 是乱序的
test.add('test')
print(test)

# 2、删除指定元素 remove  会改变原数据
test.remove('test')
print(test)

# 3、随机删除一个元素pop 会改变原数据
test.pop()
print(test)

# 4、清空集合 clear
test.clear()
print(test)

# 5、集合1.difference(集合2)，功能：取出集合1和集合2的差集（集合1有而集合2没有的）   原始集合不会发生改变
set1 = {1,2,3}
set2 = {1, 4, 5}
set3 = set1.difference(set2)
print(set3)

# 6、消除两个集合的差别 集合1.difference_update(集合2)  对比集合1和集合2，在集合1内，删除和集合2相同的元素  会改变原始数据
set4 = {1,2,3}
set5 = {1, 4, 5}
set4.difference_update(set5)
print(set4)

# 7、集合的合并 集合1.union(集合2)  将集合1和集合2组合成新集合  原始数据不变 返回一个新的序列(去重)
set6 = {1,2,3}
set7 = {1, 4, 5}
set8 = set6.union(set7)
print(set8)

# 8、len长度统计
# 9、支持for循环遍历