# 在python里面数据容器一般包含 数组 元祖 集合 字典 映射
# 列表的定义语法
# 列表的定义
list = ['shuju1','shuju2','shuju3','shuju4']
# 根据下标取值  index 是查找这个元素的下标 如果没有该元素将会报错
print(list.index('shuju1'))

# 修改下标索引的值  直接使用下标直接赋值就可以了
list[1] = 1
print(list)

# 在列表里面插入一个数据  使用 列表.insert(下标， 元素)
list.insert(2, '我是插入的元素')
print(list)

# 元素的追加 相当于js的push
list.append('我是append的元素')
print(list)

# 在列表里面追加多个元素  extend里面传递的是一个数据容器
list.extend([1,2,3,4])
print(list)

#  删除指定下标的元素  后面输入的是下标
del list[0]  # 方法一
print(list)
list.pop(0) # 方法二  返回值是删除的元素
print(list)

# 删除列表里面的第一个匹配项
list1 = [ 1, 2, 3,2,5,4]
list1.remove(2)
print(list1)

# 清空列表
list3 = [1,2,3,4,5]
list3.clear()
print(list3)

# 统计元素在列表里面的数量
list4 = [1,2,3,4,3,4,5,6,2,3]
print(list4.count(2))

# 统计列表的长度 相当于js里面的length