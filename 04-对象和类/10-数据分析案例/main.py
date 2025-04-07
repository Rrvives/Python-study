# 设计一个类完成数据的封装
# 设计一个抽象类 用于读取文件

from file_defined import FileRender, TextFileRender, JsonFileRender

from data_define import Record
from pyecharts.charts import Bar

from pyecharts.options import *

text_file_reader = TextFileRender('1月.txt')
json_file_reader = JsonFileRender('2月.txt')

text_data = text_file_reader.read_data()
json_data = json_file_reader.read_data()

all_data = text_data + json_data

data_dict = {}
for l in all_data:
    if l.date not in data_dict:
        data_dict[l.date] = l.money
    else:
        data_dict[l.date] = data_dict[l.date] + l.money

# 可视化图标
bar = Bar()
bar.add_xaxis(list(data_dict.keys()))
bar.add_yaxis("", list(data_dict.values()))
bar.render("销售额图表.html")