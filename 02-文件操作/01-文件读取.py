# 打开文件
file = open('./测试文件.txt', 'r', encoding="UTF-8")
print(file)

# 读取文件 .rend(读取文件的字节长度)
# a = file.read()
# print(a)

# 读取文件 .readlines()  读取文件所有行  每次读取.readline一行
b = file.readlines()
print(b)

# 文件关闭 file
file.close()