from pyecharts import options as opts
from pyecharts.charts import Bar, Timeline
from pyecharts.commons.utils import JsCode
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from datetime import timedelta
import csv

# 世界的确诊人数时序数据
data_global_confirmed_timeSeries = pd.read_csv('data/time_series_covid19_confirmed_global.csv')
# 世界的死亡人数时序数据
data_global_deaths_timeSeries = pd.read_csv('data//time_series_covid19_deaths_global.csv')
# 世界的治愈人数时序数据
data_global_recovered_timeSeries = pd.read_csv('data//time_series_covid19_recovered_global.csv')

# 按国家进行分组，内置求和，并转置
data_global_confirmed_timeSeries = data_global_confirmed_timeSeries.groupby(by=['Country']).aggregate(np.sum).transpose()
# 转置后日期是时序数据的索引，将日期转化为标准日期格式
data_global_confirmed_timeSeries.index = pd.to_datetime(data_global_confirmed_timeSeries.index)

# 选取国家,选取不同国家可修改此段代码
# 设置需要显示的国家
CountrynameSeries = ['China','US','India','France','Italy','Canada','Russia','United Kingdom','Spain','Germany']
data_confirmed_part_Country = data_global_confirmed_timeSeries[CountrynameSeries]

# 同理对死亡人数时序数据和治愈人数时序数据进行预处理
data_global_deaths_timeSeries = data_global_deaths_timeSeries.groupby(by=['Country']).aggregate(np.sum).transpose()
data_global_deaths_timeSeries.index = pd.to_datetime(data_global_deaths_timeSeries.index)
data_deaths_part_Country = data_global_deaths_timeSeries[CountrynameSeries]

data_global_recovered_timeSeries = data_global_recovered_timeSeries.groupby(by=['Country']).aggregate(np.sum).transpose()
data_global_recovered_timeSeries.index = pd.to_datetime(data_global_recovered_timeSeries.index)
data_recovered_part_Country = data_global_recovered_timeSeries[CountrynameSeries]

# 设置需要显示的日期，利用循环生成时间列表，从2020-01-22开始，每隔5天取1天
date_start = '2020-01-22'
dateSeries = []
for i in range(155):
    dateSeries.append(date_start)
    now = datetime.strptime(date_start, "%Y-%m-%d").date()
    datetime_tomorrow = now + timedelta(days=3)
    tomorrow = str(datetime_tomorrow)
    date_start = tomorrow

# 设置整个图幅的长宽
tl = Timeline(init_opts=opts.InitOpts(width="1280px",height="720px"))
for i in range(len(dateSeries)):
    bar = (
        Bar()
        # 设置x轴的数据标签为国家的名称
        .add_xaxis(CountrynameSeries)
        # 设置三个y轴的数据值分别为"confirmed"、"deaths"和"recovered"的特定日期的数据，通过将dataframe转成np.array再转成list将数据传入
        .add_yaxis("confirmed", np.array(data_confirmed_part_Country[(data_confirmed_part_Country.index == dateSeries[i])]).tolist()[0])
        .add_yaxis("deaths", np.array(data_deaths_part_Country[(data_deaths_part_Country.index == dateSeries[i])]).tolist()[0])
        .add_yaxis("recovered", np.array(data_recovered_part_Country[(data_recovered_part_Country.index == dateSeries[i])]).tolist()[0])
        .set_colors(["red", "gray", "green"])

        # 横竖坐标轴转置
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))

        # 全局属性设置
        .set_global_opts(
            title_opts=opts.TitleOpts("{}当日各国疫情数据".format(dateSeries[i])),
            # 设置x轴和y轴的名称
            yaxis_opts=opts.AxisOpts(name="国家"),
            xaxis_opts=opts.AxisOpts(name="人数"),
            # 设置垂直滑动条效果
            #datazoom_opts=opts.DataZoomOpts(orient="vertical"),

            # 设置右下角的小标签
            graphic_opts=[
                opts.GraphicGroup(
                    graphic_item=opts.GraphicItem(
                        rotation=JsCode("Math.PI / 4"),
                        bounding="raw",
                        right=100,
                        bottom=110,
                        z=100,
                    ),
                    children=[
                        opts.GraphicRect(
                            graphic_item=opts.GraphicItem(
                                left="center", top="center", z=100
                            ),
                            graphic_shape_opts=opts.GraphicShapeOpts(
                                width=400, height=50
                            ),
                            graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                                fill="rgba(0,0,0,0.3)"
                            ),
                        ),
                        opts.GraphicText(
                            graphic_item=opts.GraphicItem(
                                left="center", top="center", z=100
                            ),
                            graphic_textstyle_opts=opts.GraphicTextStyleOpts(
                                text="{}疫情数据".format(dateSeries[i]),
                                font="bold 26px Microsoft YaHei",
                                graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                                    fill="#fff"
                                ),
                            ),
                        ),
                    ],
                )
            ],
        )
    )
    # 将每一张bar添加到时间轴里，并设置播放速度为750
    tl.add(bar, "{}".format(dateSeries[i])).add_schema(play_interval=750)
tl.render("全球主要国家动态Covid-19数据柱状图.html")
