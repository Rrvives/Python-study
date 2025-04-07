from pyecharts.charts import Map
from pyecharts.options import VisualMapOpts
# 准备地图对象
map = Map()
# 准备地图数据
data = [
    ("北京", 1000),
    ("上海", 2000),
    ("广州", 3000),
    ("深圳", 4000),
    ("杭州", 5000),
    ("西安", 6000),
    ("成都", 7000),
    ("武汉", 8000),
    ("南京", 9000),
    ("重庆", 10000),
    ("天津", 11000),
    ("厦门", 12000),
]

# 添加数据
map.add("地图名称", data, "china")



# 配置全局变量
map.set_global_opts(
    visualmap_opts = VisualMapOpts(
        is_show = True,  # 图例
        is_piecewise= True,
    )
)

# 绘制地图
map.render()