# 方法一
# 占位符拼接字符串  %s为占位符， 后面跟相应的变量去替换，如果只有一个值时，不需要写（） 可以直接写
# %s 是将内容转换为字符串然后在拼接
# %d 是数字类型 不会将类型转换字符串
# %f 是浮点数类型
class_num = 57
avg_salary = 1000
message = "大数据学科，北京%s期，毕业工资%s元" %(class_num, avg_salary)
print(message)


# 方法二
# 快速格式化  在字符串前面只需要加f就能在串里面替换数据 不限数据类型  类似于js里面的${}
num1 = 100
num2 = 200.12
print(f'我是num1{num1}, 我是num2{num2}')