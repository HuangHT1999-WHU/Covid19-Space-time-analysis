from pyecharts import options as opts
from pyecharts.charts import Bar, Timeline, Tab
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

# 同理对死亡人数时序数据和治愈人数时序数据进行预处理
data_global_deaths_timeSeries = data_global_deaths_timeSeries.groupby(by=['Country']).aggregate(np.sum).transpose()
data_global_deaths_timeSeries.index = pd.to_datetime(data_global_deaths_timeSeries.index)

data_global_recovered_timeSeries = data_global_recovered_timeSeries.groupby(by=['Country']).aggregate(np.sum).transpose()
data_global_recovered_timeSeries.index = pd.to_datetime(data_global_recovered_timeSeries.index)

# 设置需要显示的日期，利用循环生成时间列表，从2020-01-22开始，每隔5天取1天
date_start = '2020-01-22'
dateSeries = []
for i in range(155):
    dateSeries.append(date_start)
    now = datetime.strptime(date_start, "%Y-%m-%d").date()
    datetime_tomorrow = now + timedelta(days=3)
    tomorrow = str(datetime_tomorrow)
    date_start = tomorrow


def Global_Confirmed_dynamic_data() -> Timeline:
    tl = Timeline(init_opts=opts.InitOpts(width="1280px", height="720px"))
    for i in range(len(dateSeries)):
        # 首先对数据进行排序，取出排名前20的国家
        # 对当日的数据使用sort_values(by=dateSeries[i], axis=1, ascending=False)进行降序排列，人数越多越靠前
        datatemp = data_global_confirmed_timeSeries[
            (data_global_confirmed_timeSeries.index == dateSeries[i])].sort_values(by=dateSeries[i], axis=1,
                                                                                   ascending=False)
        # 转置，取前20行，再转置取一个升序排列，让人数最多的在最上面，即可得到需要的数据序列
        datatemp = datatemp.transpose()[0:20].transpose().sort_values(by=dateSeries[i], axis=1, ascending=True)
        # 生成国家列表
        CountrynameSeries = datatemp.transpose().index.values.tolist()

        bar = (
            Bar()
                # 设置x轴的数据标签为国家的名称
                .add_xaxis(CountrynameSeries)
                # 设置y轴的数据值为"confirmed"的特定日期的数据，通过将dataframe转成np.array再转成list将数据传入
                .add_yaxis("confirmed", np.array(datatemp).tolist()[0])
                .set_colors(['red'])

                # 横竖坐标轴转置
                .reversal_axis()
                .set_series_opts(label_opts=opts.LabelOpts(position="right"))

                # 全局属性设置
                .set_global_opts(
                title_opts=opts.TitleOpts("{}当日各国疫情数据".format(dateSeries[i])),
                # 设置x轴和y轴的名称
                yaxis_opts=opts.AxisOpts(name="国家"),
                xaxis_opts=opts.AxisOpts(name="人数"),

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
                                    text="{}确诊数据".format(dateSeries[i]),
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
        tl.add(bar, "{}".format(dateSeries[i])).add_schema(play_interval=850)
    return tl

def Global_deaths_dynamic_data() -> Timeline:
    tl = Timeline(init_opts=opts.InitOpts(width="1280px", height="720px"))
    for i in range(len(dateSeries)):
        # 首先对数据进行排序，取出排名前20的国家
        # 对当日的数据使用sort_values(by=dateSeries[i], axis=1, ascending=False)进行降序排列，人数越多越靠前
        datatemp = data_global_deaths_timeSeries[(data_global_deaths_timeSeries.index == dateSeries[i])].sort_values(by=dateSeries[i], axis=1,ascending=False)
        # 转置，取前20行，再转置取一个升序排列，让人数最多的在最上面，即可得到需要的数据序列
        datatemp = datatemp.transpose()[0:20].transpose().sort_values(by=dateSeries[i], axis=1, ascending=True)
        # 生成国家列表
        CountrynameSeries = datatemp.transpose().index.values.tolist()

        bar = (
            Bar()
                # 设置x轴的数据标签为国家的名称
                .add_xaxis(CountrynameSeries)
                # 设置y轴的数据值为"deaths"的特定日期的数据，通过将dataframe转成np.array再转成list将数据传入
                .add_yaxis("deaths", np.array(datatemp).tolist()[0])
                .set_colors(['gray'])

                # 横竖坐标轴转置
                .reversal_axis()
                .set_series_opts(label_opts=opts.LabelOpts(position="right"))

                # 全局属性设置
                .set_global_opts(
                title_opts=opts.TitleOpts("{}当日各国疫情数据".format(dateSeries[i])),
                # 设置x轴和y轴的名称
                yaxis_opts=opts.AxisOpts(name="国家"),
                xaxis_opts=opts.AxisOpts(name="人数"),

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
                                    text="{}死亡数据".format(dateSeries[i]),
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
        tl.add(bar, "{}".format(dateSeries[i])).add_schema(play_interval=850)
    return tl

def Global_recovered_dynamic_data() -> Timeline:
    tl = Timeline(init_opts=opts.InitOpts(width="1280px", height="720px"))
    for i in range(len(dateSeries)):
        # 首先对数据进行排序，取出排名前20的国家
        # 对当日的数据使用sort_values(by=dateSeries[i], axis=1, ascending=False)进行降序排列，人数越多越靠前
        datatemp = data_global_recovered_timeSeries[(data_global_recovered_timeSeries.index == dateSeries[i])].sort_values(by=dateSeries[i], axis=1,ascending=False)
        # 转置，取前20行，再转置取一个升序排列，让人数最多的在最上面，即可得到需要的数据序列
        datatemp = datatemp.transpose()[0:20].transpose().sort_values(by=dateSeries[i], axis=1, ascending=True)
        # 生成国家列表
        CountrynameSeries = datatemp.transpose().index.values.tolist()

        bar = (
            Bar()
                # 设置x轴的数据标签为国家的名称
                .add_xaxis(CountrynameSeries)
                # 设置y轴的数据值为"recovered"的特定日期的数据，通过将dataframe转成np.array再转成list将数据传入
                .add_yaxis("recovered", np.array(datatemp).tolist()[0])
                .set_colors(['green'])

                # 横竖坐标轴转置
                .reversal_axis()
                .set_series_opts(label_opts=opts.LabelOpts(position="right"))

                # 全局属性设置
                .set_global_opts(
                title_opts=opts.TitleOpts("{}当日各国疫情数据".format(dateSeries[i])),
                # 设置x轴和y轴的名称
                yaxis_opts=opts.AxisOpts(name="国家"),
                xaxis_opts=opts.AxisOpts(name="人数"),

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
                                    text="{}治愈数据".format(dateSeries[i]),
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
        tl.add(bar, "{}".format(dateSeries[i])).add_schema(play_interval=850)
    return tl

tab = Tab()
tab.add(Global_Confirmed_dynamic_data(), "Global Confirmed dynamic data")
tab.add(Global_deaths_dynamic_data(), "Global deaths Map")
tab.add(Global_recovered_dynamic_data(), "Global recovered Map")
tab.render("全球Covid-19疫情CDR人数前20名动态数据.html")

