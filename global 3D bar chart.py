from pyecharts import options as opts
from pyecharts.charts import Bar3D
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
# 选取国家：'China', 'US', 'India'，选取不同国家可修改此段代码
# 设置需要显示的国家
CountrynameSeries = ['China','US','India','France','Italy','Canada','Russia','United Kingdom','Spain','Germany']
data_confirmed_part_Country = data_global_confirmed_timeSeries[CountrynameSeries]

# 设置需要显示的日期，利用循环生成时间列表，从2020-01-22开始，每隔5天取1天
date_start = '2020-01-22'
dateSeries = []
data = []
for i in range(45):
    dateSeries.append(date_start)
    now = datetime.strptime(date_start, "%Y-%m-%d").date()
    datetime_tomorrow = now + timedelta(days=10)
    tomorrow = str(datetime_tomorrow)
    date_start = tomorrow
    # 使用循环创造data数据集，数据集的要素类型为list，格式为：[国家，日期，值]
    for j in range(len(CountrynameSeries)):
        temp = [CountrynameSeries[j], dateSeries[i],np.array(data_confirmed_part_Country[(data_confirmed_part_Country.index == dateSeries[i])]).tolist()[0][j]]
        data.append(temp)

c = (
    # 设置渲染风格
    Bar3D(init_opts=opts.InitOpts(renderer='canvas',width="1280px",height="720px"))
    .add(
        "",
        data=data,
        xaxis3d_opts=opts.Axis3DOpts(CountrynameSeries, type_="category",name='Country',interval=0),
        yaxis3d_opts=opts.Axis3DOpts(dateSeries, type_="category",name='Date',interval=3),
        zaxis3d_opts=opts.Axis3DOpts(type_="value",name='Number'),
        grid3d_opts=opts.Grid3DOpts(
            # 设置三个坐标轴x,z,y的长度
            width=100,
            height=100,
            depth=120,
            # 是否开启自动旋转
            is_rotate=True,
        )
    )
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(max_=35000000),
        title_opts=opts.TitleOpts(title="3DBar chart of global major countries Covid-19 confirmed data"),
    )
    .render("全球主要国家Covid-19确诊人数3D柱状图.html")
)
