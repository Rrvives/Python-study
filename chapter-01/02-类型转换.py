# int(x) 将转换为int类型
print(int('1'))
print(int(True))
print(int('123'), type(int('123')))
# print(int('abc'), type(int('abc')))  # 带字母的字符串不能转换为int'类型

# float(x) 将x转换为float类型  一般int能转的 float就都能转
print(float('123'))
print(float(123))
print(float(True))
# print(float('a'))  会报错

# str（x)  将x转换为str类型 一般所有的数据类型都能转换为str类型
print('-----------------str转化数据类型-------------------------')
print(str(123))
print(str([1, 2, 3, 4]))
print(str(True))
# 下面的这几个针对不要的业务在去验证

# complex(real，[,imag]） 该操作比较少，用于创建一个复数

# repr(x)  将x转换为表达式字符串

# eval(str) 计算在字符串中的有效 Python 表达式，并返回一个对象

# chr(x) 将一个整数转换为字符

# ord(x) 将一个字符x转换为她对应的整数值

# hex(x) 将一个整数x转换为一个十六进制字符串

# oct(x) 将一个整数 x 转换为一个八进制的字符串
