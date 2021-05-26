from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.charts import Bar, Timeline, Tab

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

# 获取国家名称列表，并将源数据文件与pyechart中的国家名称不对应的进行修改
CountrynameSeries = data_global_confirmed_timeSeries['Country'].unique().tolist()
# 美国
CountrynameSeries[CountrynameSeries.index("US")] = 'United States'
# 南苏丹
CountrynameSeries[CountrynameSeries.index("South Sudan")] = 'S. Sudan'
# 中非共和国
CountrynameSeries[CountrynameSeries.index("Central African Republic")] = 'Central African Rep.'
# 刚果共和国（面积较小，位于西侧）
CountrynameSeries[CountrynameSeries.index("Congo (Brazzaville)")] = 'Congo'
# 刚果民主共和国（面积较大，位于东侧）
CountrynameSeries[CountrynameSeries.index("Congo (Kinshasa)")] = 'Dem. Rep. Congo'
# 老挝
CountrynameSeries[CountrynameSeries.index("Laos")] = 'Lao PDR'
# 韩国
CountrynameSeries[CountrynameSeries.index("Korea, South")] = 'Korea'
# 赤道几内亚
CountrynameSeries[CountrynameSeries.index("Guinea")] = 'Eq. Guinea'
# 多米尼加共和国
CountrynameSeries[CountrynameSeries.index("Dominican Republic")] = 'Dominican Rep.'

# 按国家进行分组，内置求和，并转置
data_global_confirmed_timeSeries = data_global_confirmed_timeSeries.groupby(by=['Country']).aggregate(np.sum).transpose()
# 转置后日期是时序数据的索引，将日期转化为标准日期格式
data_global_confirmed_timeSeries.index = pd.to_datetime(data_global_confirmed_timeSeries.index)

# 同理对死亡人数时序数据和治愈人数时序数据进行预处理
data_global_deaths_timeSeries = data_global_deaths_timeSeries.groupby(by=['Country']).aggregate(np.sum).transpose()
data_global_deaths_timeSeries.index = pd.to_datetime(data_global_deaths_timeSeries.index)

data_global_recovered_timeSeries = data_global_recovered_timeSeries.groupby(by=['Country']).aggregate(np.sum).transpose()
data_global_recovered_timeSeries.index = pd.to_datetime(data_global_recovered_timeSeries.index)

# 中国的确诊人数时序数据
data_China_confirmed_timeSeries = pd.read_csv('data/time_series_covid19_confirmed_China.csv')
# 中国的死亡人数时序数据
data_China_deaths_timeSeries = pd.read_csv('data/time_series_covid19_deaths_China.csv')
# 中国的治愈人数时序数据
data_China_recovered_timeSeries = pd.read_csv('data/time_series_covid19_recovered_China.csv')

# 获取省份名的列表，并将其中的英文省份名转化为中文
ProvincenameSeries = data_China_confirmed_timeSeries['Province'].unique().tolist()
for a in ProvincenameSeries:
    if a == 'Anhui':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '安徽'
    if a == 'Beijing':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '北京'
    if a == 'Chongqing':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '重庆'
    if a == 'Fujian':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '福建'
    if a == 'Gansu':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '甘肃'
    if a == 'Guangdong':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '广东'
    if a == 'Guangxi':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '广西'
    if a == 'Guizhou':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '贵州'
    if a == 'Hainan':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '海南'
    if a == 'Hebei':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '河北'
    if a == 'Heilongjiang':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '黑龙江'
    if a == 'Henan':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '河南'
    if a == 'Hong Kong':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '香港'
    if a == 'Hubei':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '湖北'
    if a == 'Hunan':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '湖南'
    if a == 'Inner Mongolia':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '内蒙古'
    if a == 'Jiangsu':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '江苏'
    if a == 'Jiangxi':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '江西'
    if a == 'Jilin':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '吉林'
    if a == 'Liaoning':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '辽宁'
    if a == 'Macau':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '澳门'
    if a == 'Ningxia':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '宁夏'
    if a == 'Qinghai':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '青海'
    if a == 'Shaanxi':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '陕西'
    if a == 'Shandong':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '山东'
    if a == 'Shanghai':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '上海'
    if a == 'Shanxi':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '山西'
    if a == 'Sichuan':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '四川'
    if a == 'Tianjin':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '天津'
    if a == 'Tibet':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '西藏'
    if a == 'Taiwan':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '台湾'
    if a == 'Xinjiang':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '新疆'
    if a == 'Yunnan':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '云南'
    if a == 'Zhejiang':
        ProvincenameSeries[ProvincenameSeries.index(a)] = '浙江'

# 对中国的确诊人数时序数据进行处理
# 将中国时序数据的索引设为“Province”，转置并去除掉“Country”行
data_China_confirmed_timeSeries = data_China_confirmed_timeSeries.set_index('Province').transpose().drop(['Country'])
# 转置后日期是时序数据的索引，将日期转化为标准日期格式
data_China_confirmed_timeSeries.index = pd.to_datetime(data_China_confirmed_timeSeries.index)
# 同理对死亡人数时序数据和治愈人数时序数据进行预处理
data_China_deaths_timeSeries = data_China_deaths_timeSeries.set_index('Province').transpose().drop(['Country'])
data_China_deaths_timeSeries.index= pd.to_datetime(data_China_deaths_timeSeries.index)
data_China_recovered_timeSeries = data_China_recovered_timeSeries.set_index('Province').transpose().drop(['Country'])
data_China_recovered_timeSeries.index= pd.to_datetime(data_China_recovered_timeSeries.index)

# 设置需要显示的日期，利用循环生成时间列表，从2020-01-22开始，每隔5天取1天
date_start = '2020-01-22'
dateSeries = []
for i in range(155):
    dateSeries.append(date_start)
    now = datetime.strptime(date_start, "%Y-%m-%d").date()
    datetime_tomorrow = now + timedelta(days=3)
    tomorrow = str(datetime_tomorrow)
    date_start = tomorrow

# 上面是数据准备部分，下面开始绘图
# 全球确诊人数分布图
def Global_Confirmed_Map() -> Timeline:
    tl = Timeline(init_opts=opts.InitOpts(width="1280px", height="720px"))
    for j in range(len(dateSeries)):
        c = (
            Map()
            .add("confirmed",
                 [list(z) for z in zip(CountrynameSeries, np.array(data_global_confirmed_timeSeries[(data_global_confirmed_timeSeries.index == dateSeries[j])]).tolist()[0])],
                 "world",
                 is_map_symbol_show=False)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            # 在这里需要设置视觉映射配置项的最大值，分段数和颜色区间
            # 需要注意的是，我们以2021.04.30的数据按国家分组求和后得到CDR的三个四分位（较大）数分别为：358738、6957、257261，分别将其作为三张图的视觉映射配置项的最大值
            .set_global_opts(title_opts=opts.TitleOpts(title="{} 世界Covid-19疫情确诊人数分布地图".format(dateSeries[j])),visualmap_opts=opts.VisualMapOpts(max_=358738,split_number=20,range_color=['#FFFFFF','#610B0B']), )
            .set_colors(["red"])
        )
        # 将每一张Map添加到时间轴里，并设置播放速度为400
        tl.add(c, "{}".format(dateSeries[j])).add_schema(play_interval=400)
    return tl

# 全球死亡人数分布图
def Global_deaths_Map() -> Timeline:
    tl = Timeline(init_opts=opts.InitOpts(width="1280px", height="720px"))
    for j in range(len(dateSeries)):
        c = (
            Map()
            .add("deaths",
                 [list(z) for z in zip(CountrynameSeries, np.array(data_global_deaths_timeSeries[(data_global_deaths_timeSeries.index == dateSeries[j])]).tolist()[0])],
                 "world",
                 is_map_symbol_show=False)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(title_opts=opts.TitleOpts(title="{} 世界Covid-19疫情死亡人数分布地图".format(dateSeries[j])),visualmap_opts=opts.VisualMapOpts(max_=6957,split_number=20,range_color=['#FFFFFF','#1C1C1C']),)
            .set_colors(["gray"])
        )
        # 将每一张Map添加到时间轴里，并设置播放速度为400
        tl.add(c, "{}".format(dateSeries[j])).add_schema(play_interval=400)
    return tl

# 全球治愈人数分布图
def Global_recovered_Map() -> Timeline:
    tl = Timeline(init_opts=opts.InitOpts(width="1280px", height="720px"))
    for j in range(len(dateSeries)):
        c = (
            Map()
            .add("recovered",
                 [list(z) for z in zip(CountrynameSeries, np.array(data_global_recovered_timeSeries[(data_global_recovered_timeSeries.index == dateSeries[j])]).tolist()[0])],
                 "world",
                 is_map_symbol_show=False)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(title_opts=opts.TitleOpts(title="{} 世界Covid-19疫情治愈人数分布地图".format(dateSeries[j])),visualmap_opts=opts.VisualMapOpts(max_=257261,split_number=20,range_color=['#FFFFFF','#04B431']),)
            .set_colors(["green"])
        )
        # 将每一张Map添加到时间轴里，并设置播放速度为400
        tl.add(c, "{}".format(dateSeries[j])).add_schema(play_interval=400)
    return tl

# 中国确诊人数分布图
def Chinese_Confirmed_Map() -> Timeline:
    tl = Timeline(init_opts=opts.InitOpts(width="1280px", height="720px"))
    for j in range(len(dateSeries)):
        c = (
            Map()
            .add("confirmed",
                 [list(z) for z in zip(ProvincenameSeries, np.array(data_China_confirmed_timeSeries[(data_China_confirmed_timeSeries.index == dateSeries[j])]).tolist()[0])],
                 "china",
                 is_map_symbol_show=False)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            # 在这里需要设置视觉映射配置项的最大值，分段数和颜色区间
            # 需要注意的是，我们以2021.04.30的数据按国家分组求和后得到CDR的三个四分位（较大）数分别为：1057、7、1041，分别将其作为三张图的视觉映射配置项的最大值
            .set_global_opts(title_opts=opts.TitleOpts(title="{} 中国Covid-19疫情确诊人数分布地图".format(dateSeries[j])),visualmap_opts=opts.VisualMapOpts(max_=1057,split_number=20,range_color=['#FFFFFF','#610B0B']), )
            .set_colors(["red"])
        )
        # 将每一张Map添加到时间轴里，并设置播放速度为400
        tl.add(c, "{}".format(dateSeries[j])).add_schema(play_interval=400)
    return tl

# 中国死亡人数分布图
def Chinese_deaths_Map() -> Timeline:
    tl = Timeline(init_opts=opts.InitOpts(width="1280px", height="720px"))
    for j in range(len(dateSeries)):
        c = (
            Map()
            .add("confirmed",
                 [list(z) for z in zip(ProvincenameSeries, np.array(data_China_deaths_timeSeries[(data_China_deaths_timeSeries.index == dateSeries[j])]).tolist()[0])],
                 "china",
                 is_map_symbol_show=False)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            # 在这里需要设置视觉映射配置项的最大值，分段数和颜色区间
            .set_global_opts(title_opts=opts.TitleOpts(title="{} 中国Covid-19疫情死亡人数分布地图".format(dateSeries[j])),visualmap_opts=opts.VisualMapOpts(max_=7,split_number=20,range_color=['#FFFFFF','#1C1C1C']), )
            .set_colors(["gray"])
        )
        # 将每一张Map添加到时间轴里，并设置播放速度为400
        tl.add(c, "{}".format(dateSeries[j])).add_schema(play_interval=400)
    return tl

# 中国确诊人数分布图
def Chinese_recovered_Map() -> Timeline:
    tl = Timeline(init_opts=opts.InitOpts(width="1280px", height="720px"))
    for j in range(len(dateSeries)):
        c = (
            Map()
            .add("confirmed",
                 [list(z) for z in zip(ProvincenameSeries, np.array(data_China_recovered_timeSeries[(data_China_recovered_timeSeries.index == dateSeries[j])]).tolist()[0])],
                 "china",
                 is_map_symbol_show=False)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            # 在这里需要设置视觉映射配置项的最大值，分段数和颜色区间
            .set_global_opts(title_opts=opts.TitleOpts(title="{} 中国Covid-19疫情治愈人数分布地图".format(dateSeries[j])),visualmap_opts=opts.VisualMapOpts(max_=1041,split_number=20,range_color=['#FFFFFF','#04B431']), )
            .set_colors(["green"])
        )
        # 将每一张Map添加到时间轴里，并设置播放速度为400
        tl.add(c, "{}".format(dateSeries[j])).add_schema(play_interval=400)
    return tl

tab = Tab()
tab.add(Global_Confirmed_Map(), "Global Confirmed Map")
tab.add(Global_deaths_Map(), "Global deaths Map")
tab.add(Global_recovered_Map(), "Global recovered Map")
tab.add(Chinese_Confirmed_Map(), "Chinese confirmed Map")
tab.add(Chinese_deaths_Map(), "Chinese deaths Map")
tab.add(Chinese_recovered_Map(), "Chinese recovered Map")
tab.render("Covid-19疫情CDR人数时序地图.html")
