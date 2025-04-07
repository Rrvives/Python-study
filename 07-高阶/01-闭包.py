
def outer(data):
    def inner(data1):
        # nonlocal data 这个定义会使得内部函数可以修改外部函数的变量
        print(f'外部变量{data}, 内部变量{data1}')

    return inner


fn = outer('外部变量')
fn('内部变量')
