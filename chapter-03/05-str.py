# 常见的操作
name = 'abcdefg'

# 1、根据下标获取获取特定位置的字符  注意：可以获取但是不能修改
print(name[0])  # a

# 2、查找固定字符串索引位置
print(name.index('b')) # 1

# 3、指定字符串替换 字符串.replace(字符串1，字符串2)
new_name = name.replace('b', 'i')
print(new_name)  # aicdefg

# 4、字符串分隔 字符串.split(分隔符)
new_name1 = name.split(' ')
print(new_name1)

# 5、字符串的规整  去掉前后空格或指定的字符
test1 = '  123   '
new_test = test1.strip()
print(test1)
print(new_test)

test2 = '12abc21'
new_test2 = test2.strip('12')  # 注意 在这里去除固定字符的时候 是一个一个去除  不是一个整体 所以12或者21 都是可以的
print(test2)
print(new_test2)

# 6、统计某字符串在字符或字符在字符串里面出现的次数
test3 = 'abcabcaa32e23weaawe'
new_test3 = test3.count('aa')
print(new_test3)

# 7、len  统计字符串的长度
# 8、当然也是支持while和for循环遍历的