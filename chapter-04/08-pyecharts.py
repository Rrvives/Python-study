# 用于数据可视化的需求开发
from pyecharts.charts import Line

line = Line()
line.add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
line.add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
line.render("line.html")