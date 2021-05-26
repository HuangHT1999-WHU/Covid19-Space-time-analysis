from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line
import pandas as pd
import matplotlib.pyplot as plt
import csv
import numpy as np
from datetime import datetime
from datetime import timedelta
from pyecharts.faker import Faker

# 中国的确诊人数时序数据
data_China_confirmed_timeSeries = pd.read_csv('data/time_series_covid19_confirmed_China.csv')
# 中国的死亡人数时序数据
data_China_deaths_timeSeries = pd.read_csv('data/time_series_covid19_deaths_China.csv')
# 中国的治愈人数时序数据
data_China_recovered_timeSeries = pd.read_csv('data/time_series_covid19_recovered_China.csv')

# 对中国的确诊人数时序数据进行处理,得到求和数据
# 将中国时序数据按照"Country"列分组求和，即将中国各省数据求和，随后转置，交换行列，使索引变为日期
data_China_confirmed_sum_timeSeries = data_China_confirmed_timeSeries.groupby(by=['Country']).aggregate(np.sum).transpose()
# 转置后日期是时序数据的索引，将日期转化为标准日期格式，通过strftime('%Y-%m-%d')限制只保留日期而包含时间
data_China_confirmed_sum_timeSeries.index = pd.to_datetime(data_China_confirmed_sum_timeSeries.index).strftime('%Y-%m-%d')
# 同理对死亡人数时序数据和治愈人数时序数据进行预处理
data_China_deaths_sum_timeSeries = data_China_deaths_timeSeries.groupby(by=['Country']).aggregate(np.sum).transpose()
data_China_deaths_sum_timeSeries.index = pd.to_datetime(data_China_deaths_sum_timeSeries.index).strftime('%Y-%m-%d')
data_China_recovered_sum_timeSeries = data_China_recovered_timeSeries.groupby(by=['Country']).aggregate(np.sum).transpose()
data_China_recovered_sum_timeSeries.index = pd.to_datetime(data_China_recovered_sum_timeSeries.index).strftime('%Y-%m-%d')

# 如果只想用部分时间段的数据进行分析，修改并释放下面这个代码段即可
'''
data_China_confirmed_sum_timeSeries = data_China_confirmed_sum_timeSeries['2020-01-22':'2020-03-01']
data_China_deaths_sum_timeSeries = data_China_deaths_sum_timeSeries['2020-01-22':'2020-03-01']
data_China_recovered_sum_timeSeries = data_China_recovered_sum_timeSeries['2020-01-22':'2020-03-01']
'''
# 处理得到较前一日人数增长的数据
diff_data_China_confirmed_sum_timeSeries = data_China_confirmed_sum_timeSeries.diff()
diff_data_China_deaths_sum_timeSeries = data_China_deaths_sum_timeSeries.diff()
diff_data_China_recovered_sum_timeSeries = data_China_recovered_sum_timeSeries.diff()

bar = (
    Bar()
    .add_xaxis(data_China_confirmed_sum_timeSeries.index.values.tolist())
    # 这个地方要注意，查看了pyechart的源码，发现这里导入需要的数据格式为float64，
    # 因此需要使用astype()对数据进行格式转换，再使用list(np.ravel())将list内部的list拆分掉
    .add_yaxis("确诊人数", list(np.ravel(np.array(data_China_confirmed_sum_timeSeries).astype(np.float64))),
               color="red",
               yaxis_index=0,
               label_opts=opts.LabelOpts(is_show=False))
    .add_yaxis("死亡人数", list(np.ravel(np.array(data_China_deaths_sum_timeSeries).astype(np.float64))),
               color="gray",
               yaxis_index=1,
               label_opts=opts.LabelOpts(is_show=False))
    .add_yaxis("治愈人数", list(np.ravel(np.array(data_China_recovered_sum_timeSeries).astype(np.float64))),
               color="green",
               yaxis_index=0,
               label_opts=opts.LabelOpts(is_show=False))
    .set_colors(["red", "gray", "green"])
    # 设置第二个y坐标轴，以“添加额外的坐标轴”（.extend_axis）的方式添加，对应的yaxis_index=1
    .extend_axis(
        yaxis=opts.AxisOpts(
            name="死亡人数",
            type_="value",
            min_=0,
            max_=8000,
            position="right",
            axislabel_opts=opts.LabelOpts(formatter="{value}人"),
        )
    )
    # 设置第三个y坐标轴，以“添加额外的坐标轴”（.extend_axis）的方式添加，对应的yaxis_index=2
    .extend_axis(
        yaxis=opts.AxisOpts(
            type_="value",
            name="确诊/治愈人数的增长数",
            min_=0,
            max_=16000,
            position="left",
            axislabel_opts=opts.LabelOpts(formatter="{value}人"),
            splitline_opts=opts.SplitLineOpts(
                is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
            ),
        )
    )
    # 设置第四个y坐标轴，以“添加额外的坐标轴”（.extend_axis）的方式添加，对应的yaxis_index=3
    .extend_axis(
        yaxis=opts.AxisOpts(
            type_="value",
            name="死亡人数的增长数",
            min_=0,
            max_=2000,
            position="left",
            offset=120,
            axislabel_opts=opts.LabelOpts(formatter="{value}人"),
            splitline_opts=opts.SplitLineOpts(
                is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
            ),
        )
    )
    .set_global_opts(
        # 设置第一个y轴，对应的yaxis_index=0
        yaxis_opts=opts.AxisOpts(
            name="确诊/治愈人数",
            min_=0,
            max_=110000,
            position="right",
            offset=100,
            axislabel_opts=opts.LabelOpts(formatter="{value}人"),),
        # 设置标题等其他全局设置
        title_opts=opts.TitleOpts(title="全国Covid19全时段疫情数据"),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        # 设置区域缩放配置滑动条
        datazoom_opts=[opts.DataZoomOpts()],
    )
)

line = (
    Line()
    .add_xaxis(data_China_confirmed_sum_timeSeries.index.values.tolist())
    .add_yaxis("确诊人数较前一天的增长数", np.array(diff_data_China_confirmed_sum_timeSeries).tolist(),
               is_smooth=True,
               label_opts=opts.LabelOpts(is_show=False),
               yaxis_index=2)
    .add_yaxis("死亡人数较前一天的增长数", np.array(diff_data_China_deaths_sum_timeSeries).tolist(),
               is_smooth=True,
               label_opts=opts.LabelOpts(is_show=False),
               yaxis_index=3)
    .add_yaxis("治愈人数较前一天的增长数", np.array(diff_data_China_recovered_sum_timeSeries).tolist(),
               is_smooth=True,
               label_opts=opts.LabelOpts(is_show=False),
               yaxis_index=2)
    .set_colors(["red", "gray", "green"])
)

bar.overlap(line)
grid = Grid(init_opts=opts.InitOpts(width="1360px",height="765px"))
grid.add(bar, opts.GridOpts(pos_left="15%", pos_right="15%"), is_control_axis_index=True)
grid.render("全国Covid19全时段疫情数据.html")
