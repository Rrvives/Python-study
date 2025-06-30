# 在python里面list和js的array基本保持一致
list1 = [1,2,3]
list2 =['1', '2', '3']
num1 = list1[0]    # 这个和js里面相同
num2 = list1[-1]   # 这个和js里面相同
num3 = list1[0:1]  # 这个表示从第0个开始取一个数据包含第一个 返回值也是一个list
print(num1, num2, num3)

# 主要方法

list1.append(1)  # 返回值死NONE
list1[1] = 10
list1.append(list2)
del list1[-1]
    