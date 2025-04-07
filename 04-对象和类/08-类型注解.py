# 类型注解 方便类型坚持工具提示  注解在js相当于ts的类型定义
# :后面的就是类型注解
import random
from typing import Union, List, Dict

name: str = '测试'
age: int = 18
is_man: bool = True

data: list[int] = [1, 2, 3]

data2: dict = {'a': 1}

# -> 表示对返回值的类型注解
# 需要注意的是 类型注解是方便提示 如果你传入的参数和返回值类型不匹配的话 只会出现警告 但是也不会报错
def test(a:int, b:int) -> int:
    return a + b




# union类型  相当于在一个数据里面存在多种类型的数据 定义的是可以写成union[int, str]这种形式

my_list: list[Union[int, str]] = [1, 2, '3', 4]

my_dict: dict[str, Union[int, str]] = {
    'a': 1,
    'b': 2,
    'c': 3
}