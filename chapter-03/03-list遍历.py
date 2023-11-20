# 列表的遍历
def list_while_fn():
    list = [1,2,3,4,5,6,7]
    index = 0
    while index < len(list):
        item = list[index]
        print(item)
        index += 1

list_while_fn()
def list_for_fn():
    list = [1, 2, 3, 4, 5, 6, 7]
    for i in list:
        print(i)

list_for_fn()