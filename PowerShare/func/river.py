#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/17 0017 10:34
# @Author  : LiangLiang
# @Site    : 
# @File    : river.py
# @Software: PyCharm
from PowerShare.settings import Settings
from PowerShare.utils.db_manage import init_engine
import pandas as pd
from pyecharts import Bar, Line, Grid
import datetime


__doc__ = """
包含河流的来水量信息，河流的出水量信息， 蓄水量信息。
提供获取数据，绘制图表的功能
"""


def get_data(engine, table_name, day_delta=30):
    """
    调用流域数据
    :param engine:
    :param table_name:
    :return:
    """
    datetime_now = datetime.datetime.now()
    last_month = (datetime_now - datetime.timedelta(days=day_delta)).strftime("%Y-%m-%d 00:00:00")
    df1 = pd.read_sql("SELECT * FROM {table_name} WHERE official_update_time> '{last_month}'".format(
        last_month=last_month,
        table_name=table_name), engine)
    return df1


def plot_inflow_of_all_main_river(title="四川当月水库蓄水量信息.html", day_delta=30, path="source"):
    """
    绘制四川当月所有河流的蓄水量信息。
    :param title:
    :return:
    """
    engine = init_engine(db="power_supply")

    datetime_now = datetime.datetime.now()
    last_month = (datetime_now - datetime.timedelta(days=day_delta)).strftime("%Y-%m-%d 00:00:00")
    df1 = pd.read_sql(
        "SELECT * FROM sc_main_river_storage WHERE official_update_time> '{last_month}'".format(last_month=last_month),
        engine)

    line2 = Line("全流域蓄水量", width="1600px", height="800px")
    df1_1 = df1.groupby(axis=0, by=["official_update_time"]).aggregate({"water_storage_capacity": "sum"})
    df1_2 = df1_1.reset_index()
    line2.add("全流域河流蓄水量图", df1_2["official_update_time"].map(lambda x: x.strftime("%Y-%m-%d")),
              df1_2["water_storage_capacity"])

    line2.render(title)


def plot_in_out_of_all_main_river(title="全流域信息来水出水.html", day_delta=30):
    """
    将河流的入水量，出水量信息按时间统计求和。
    :param day_delta:
    :return:
    """
    engine1 = init_engine(db="power_supply",)
    datetime_now = datetime.datetime.now()
    last_month = (datetime_now - datetime.timedelta(days=day_delta)).strftime("%Y-%m-%d 00:00:00")
    df1 = pd.read_sql("SELECT * FROM sc_main_river_inflow WHERE official_update_time> '{last_month}'".format(last_month=last_month), engine1)
    df2 = pd.read_sql(
        "SELECT * FROM sc_main_river_outflow WHERE official_update_time> '{last_month}'".format(last_month=last_month),
        engine1)
    print(df2["river_system"].unique())

    line2=  Line("全流域水流量", width="1600px", height="800px")
    df1_1 = df1.groupby(axis=0, by=["official_update_time"]).aggregate({"water_inflow": "sum"})
    df1_2 = df1_1.reset_index()
    df2_1 = df2.groupby(axis=0, by=["official_update_time"]).aggregate({"water_outflow": "sum"})
    df2_2 = df2_1.reset_index()
    line2.add("全流域河流水量图-来", df1_2["official_update_time"].map(lambda x:x.strftime("%Y-%m-%d")), df1_2["water_inflow"])
    line2.add("全流域河流水量图-出", df2_2["official_update_time"].map(lambda x:x.strftime("%Y-%m-%d")), df2_2["water_outflow"])

    line2.render(title)


def plot_in_out_8_river(pic_name="8大流域来水量出水量图.html"):
    """
    1. 画8张图，每个小图两条线，为入水量和出水量
    :param df1: 入水量的dataframe
    :param df2: 出水量的dataframe
    :param columns_name1: 列名1
    :param columns_name2: 列名2 ，如果画蓄水量，这个列名变量不会被使用
    :param pic_name:  "picture——name"
    :param df1_tail:  "legend的尾巴，出/入"
    :return: None
    """
    df1_tail = "-进"
    df2_tail = "-出"
    engine1 = init_engine(db="power_supply")
    df1 = get_data(engine1, "sc_main_river_inflow")
    df2 = get_data(engine1, "sc_main_river_outflow")
    columns_name1 = "water_inflow"
    columns_name2 = "water_outflow"

    df1_mj = df1[df1["river_system"]=="岷江"]
    df1_jlj = df1[df1["river_system"]=="嘉陵江"]
    df1_ddh = df1[df1["river_system"] == "大渡河"]
    df1_fj = df1[df1["river_system"] == "涪江"]
    df1_qj = df1[df1["river_system"] == "渠江"]
    df1_jsj = df1[df1["river_system"] == "金沙江"]
    df1_ylj = df1[df1["river_system"] == "雅砻江"]
    df1_qyj = df1[df1["river_system"] == "青衣江"]
    print(df1["river_system"].unique())

    grid = Grid(width="1600px", height="800px", page_title="来水量信息图")
    line1 = Line("嘉陵江",title_text_size="80%", title_pos="2%", title_top="2%",)
    line1.add("嘉陵江{}".format(df1_tail),df1_jlj["official_update_time"].map(lambda x:x.strftime("%Y-%m-%d")), df1_jlj[columns_name1],
              yaxis_label_textsize="50%",
              xaxis_label_textsize="50%",
              is_legend_show=False,
              yaxis_max=12000,
                xaxis_rotate="30",
              yaxis_rotate="30"
              )

    line2 = Line("岷江", title_text_size="80%", title_pos="25%", title_top="2%")
    line2.add("岷江{}".format(df1_tail),df1_mj["official_update_time"].map(lambda x:x.strftime("%Y-%m-%d")), df1_mj[columns_name1],
              yaxis_label_textsize="50%",
              xaxis_label_textsize="50%",
              is_legend_show=False,
              yaxis_max=12000,
    xaxis_rotate="30",
    yaxis_rotate="30",
              )

    line3 = Line("大渡河", title_text_size="80%", title_pos="50%", title_top="2%")
    line3.add("大渡河{}".format(df1_tail), df1_ddh["official_update_time"].map(lambda x:x.strftime("%Y-%m-%d")), df1_ddh[columns_name1],
              yaxis_label_textsize="50%",
              xaxis_label_textsize="50%",
              is_legend_show=False,
              yaxis_max=12000,
    # yaxis_force_interval="vertical"
    xaxis_rotate="30",
    yaxis_rotate="30",
              )

    line4 = Line("涪江", title_text_size="80%", title_pos="75%", title_top="2%")
    line4.add("涪江{}".format(df1_tail), df1_fj["official_update_time"].map(lambda x:x.strftime("%Y-%m-%d")), df1_fj[columns_name1],
              yaxis_label_textsize="50%",
              xaxis_label_textsize="50%",
              is_legend_show=False,
              yaxis_max=12000,
    # yaxis_force_interval="vertical"
    xaxis_rotate="30",
    yaxis_rotate="30",
              )

    line5 = Line("渠江", title_text_size="80%", title_pos="2%", title_top="50%")
    line5.add("渠江{}".format(df1_tail), df1_qj["official_update_time"].map(lambda x:x.strftime("%Y-%m-%d")), df1_qj[columns_name1],
              yaxis_label_textsize="50%",
              xaxis_label_textsize="50%",
              is_legend_show=False,
              yaxis_max=12000,
              xaxis_rotate="30",
                yaxis_rotate="30",
              )

    line6 = Line("金沙江", title_text_size="80%", title_pos="25%", title_top="50%")
    line6.add("金沙江{}".format(df1_tail), df1_jsj["official_update_time"].map(lambda x:x.strftime("%Y-%m-%d")), df1_jsj[columns_name1],
              yaxis_label_textsize="50%",
              xaxis_label_textsize="50%",
              is_legend_show=False,
              yaxis_max=12000,
    # yaxis_force_interval="vertical"
    xaxis_rotate="30",
    yaxis_rotate="30",
              )

    line7 = Line("雅砻江", title_text_size="80%", title_pos="50%", title_top="50%")
    line7.add("雅砻江{}".format(df1_tail), df1_ylj["official_update_time"].map(lambda x:x.strftime("%Y-%m-%d")), df1_ylj[columns_name1],
              yaxis_label_textsize="50%",
              xaxis_label_textsize="50%",
              is_legend_show=False,
            yaxis_max=12000,
    xaxis_rotate="30",
    yaxis_rotate="30",
              )

    line8 = Line("青衣江", title_text_size="80%", title_pos="75%", title_top="50%")
    line8.add("青衣江{}".format(df1_tail), df1_qyj["official_update_time"].map(lambda x:x.strftime("%Y-%m-%d")), df1_qyj[columns_name1],
              yaxis_label_textsize="50%",
              xaxis_label_textsize="50%",
              is_legend_show=False,
              yaxis_max=12000,
    xaxis_rotate="30",
    yaxis_rotate="30",
              )

    df2_mj = df2[df2["river_system"] == "岷江"]
    df2_jlj = df2[df2["river_system"] == "嘉陵江"]
    df2_ddh = df2[df2["river_system"] == "大渡河"]
    df2_fj = df2[df2["river_system"] == "涪江"]
    df2_qj = df2[df2["river_system"] == "渠江"]
    df2_jsj = df2[df2["river_system"] == "金沙江"]
    df2_ylj = df2[df2["river_system"] == "雅砻江"]
    df2_qyj = df2[df2["river_system"] == "青衣江"]

    line8.add("青衣江-{}".format(df2_tail), df2_qyj["official_update_time"].map(lambda x: x.strftime("%Y-%m-%d")), df2_qyj[columns_name2],
              yaxis_label_textsize="50%",
              xaxis_label_textsize="50%",
              is_legend_show=False,
              yaxis_max=12000,
              xaxis_rotate="30",
              yaxis_rotate="30",
              )
    line7.add("雅砻江-{}".format(df2_tail), df2_ylj["official_update_time"].map(lambda x: x.strftime("%Y-%m-%d")), df2_ylj[columns_name2],
              yaxis_label_textsize="50%",
              xaxis_label_textsize="50%",
              is_legend_show=False,
              yaxis_max=12000,
              xaxis_rotate="30",
              yaxis_rotate="30",
              )
    line6.add("金沙江-{}".format(df2_tail), df2_jsj["official_update_time"].map(lambda x: x.strftime("%Y-%m-%d")), df2_jsj[columns_name2],
              yaxis_label_textsize="50%",
              xaxis_label_textsize="50%",
              is_legend_show=False,
              yaxis_max=12000,
              # yaxis_force_interval="vertical"
              xaxis_rotate="30",
              yaxis_rotate="30",
              )
    line5.add("渠江-{}".format(df2_tail), df2_qj["official_update_time"].map(lambda x: x.strftime("%Y-%m-%d")), df2_qj[columns_name2],
              yaxis_label_textsize="50%",
              xaxis_label_textsize="50%",
              is_legend_show=False,
              yaxis_max=12000,
              xaxis_rotate="30",
              yaxis_rotate="30",
              )
    line4.add("涪江-{}".format(df2_tail), df2_fj["official_update_time"].map(lambda x: x.strftime("%Y-%m-%d")), df2_fj[columns_name2],
              yaxis_label_textsize="50%",
              xaxis_label_textsize="50%",
              is_legend_show=False,
              yaxis_max=12000,
              # yaxis_force_interval="vertical"
              xaxis_rotate="30",
              yaxis_rotate="30",
              )
    line3.add("大渡河-{}".format(df2_tail), df2_ddh["official_update_time"].map(lambda x: x.strftime("%Y-%m-%d")), df2_ddh[columns_name2],
              yaxis_label_textsize="50%",
              xaxis_label_textsize="50%",
              is_legend_show=False,
              yaxis_max=12000,
              # yaxis_force_interval="vertical"
              xaxis_rotate="30",
              yaxis_rotate="30",

              )
    line2.add("岷江-{}".format(df2_tail), df2_mj["official_update_time"].map(lambda x: x.strftime("%Y-%m-%d")), df2_mj[columns_name2],
              yaxis_label_textsize="50%",
              xaxis_label_textsize="50%",
              is_legend_show=False,
              yaxis_max=12000,
              xaxis_rotate="30",
              yaxis_rotate="30",
              )
    line1.add("嘉陵江-{}".format(df2_tail), df2_jlj["official_update_time"].map(lambda x: x.strftime("%Y-%m-%d")),
              df2_jlj[columns_name2],
              yaxis_label_textsize="50%",
              xaxis_label_textsize="50%",
              is_legend_show=False,
              yaxis_max=12000,
              xaxis_rotate="30",
              yaxis_rotate="30"
              )


    grid.add(line1, grid_right="75%", grid_bottom="55%", grid_left="2.5%")
    grid.add(line2, grid_right="50%", grid_bottom="55%", grid_left="27.5%")
    grid.add(line3, grid_right="25%", grid_bottom="55%", grid_left="52.5%")
    grid.add(line4, grid_right="0%", grid_bottom="55%", grid_left="77.5%")

    grid.add(line5, grid_right="75%", grid_top="55%", grid_left="2.5%")
    grid.add(line6, grid_right="50%", grid_top="55%", grid_left="27.5%")
    grid.add(line7, grid_right="25%", grid_top="55%", grid_left="52.5%")
    grid.add(line8, grid_right="0%", grid_top="55%", grid_left="77.5%")

    grid.render(pic_name)


def plot_storage_8_river(pic_name="8大流域蓄水量图.html"):
    """
    画8条河域的蓄水量图
    :param pic_name:  "picture——name"
    :return: None
    """
    engine = init_engine(db="power_supply")
    df1 = get_data(engine=engine, table_name="sc_main_river_storage")
    df1_tail = ""
    columns_name1 = "water_storage_capacity"

    df1_mj = df1[df1["river_system"]=="岷江"]
    df1_jlj = df1[df1["river_system"]=="嘉陵江"]
    df1_ddh = df1[df1["river_system"] == "大渡河"]
    df1_fj = df1[df1["river_system"] == "涪江"]
    df1_qj = df1[df1["river_system"] == "渠江"]
    df1_jsj = df1[df1["river_system"] == "金沙江"]
    df1_ylj = df1[df1["river_system"] == "雅砻江"]
    df1_qyj = df1[df1["river_system"] == "青衣江"]
    print(df1["river_system"].unique())

    grid = Grid(width="1600px", height="800px", page_title="来水量信息图")
    line1 = Line("嘉陵江",title_text_size="80%", title_pos="2%", title_top="2%",)
    line1.add("嘉陵江{}".format(df1_tail),df1_jlj["official_update_time"].map(lambda x:x.strftime("%Y-%m-%d")), df1_jlj[columns_name1],
              yaxis_label_textsize="50%",
              xaxis_label_textsize="50%",
              is_legend_show=False,
              yaxis_max=12000,
                xaxis_rotate="30",
              yaxis_rotate="30"
              )

    line2 = Line("岷江", title_text_size="80%", title_pos="25%", title_top="2%")
    line2.add("岷江{}".format(df1_tail),df1_mj["official_update_time"].map(lambda x:x.strftime("%Y-%m-%d")), df1_mj[columns_name1],
              yaxis_label_textsize="50%",
              xaxis_label_textsize="50%",
              is_legend_show=False,
              yaxis_max=12000,
    xaxis_rotate="30",
    yaxis_rotate="30",
              )

    line3 = Line("大渡河", title_text_size="80%", title_pos="50%", title_top="2%")
    line3.add("大渡河{}".format(df1_tail), df1_ddh["official_update_time"].map(lambda x:x.strftime("%Y-%m-%d")), df1_ddh[columns_name1],
              yaxis_label_textsize="50%",
              xaxis_label_textsize="50%",
              is_legend_show=False,
              yaxis_max=12000,
    # yaxis_force_interval="vertical"
    xaxis_rotate="30",
    yaxis_rotate="30",
              )

    line4 = Line("涪江", title_text_size="80%", title_pos="75%", title_top="2%")
    line4.add("涪江{}".format(df1_tail), df1_fj["official_update_time"].map(lambda x:x.strftime("%Y-%m-%d")), df1_fj[columns_name1],
              yaxis_label_textsize="50%",
              xaxis_label_textsize="50%",
              is_legend_show=False,
              yaxis_max=12000,
    # yaxis_force_interval="vertical"
    xaxis_rotate="30",
    yaxis_rotate="30",
              )

    line5 = Line("渠江", title_text_size="80%", title_pos="2%", title_top="50%")
    line5.add("渠江{}".format(df1_tail), df1_qj["official_update_time"].map(lambda x:x.strftime("%Y-%m-%d")), df1_qj[columns_name1],
              yaxis_label_textsize="50%",
              xaxis_label_textsize="50%",
              is_legend_show=False,
              yaxis_max=12000,
              xaxis_rotate="30",
                yaxis_rotate="30",
              )

    line6 = Line("金沙江", title_text_size="80%", title_pos="25%", title_top="50%")
    line6.add("金沙江{}".format(df1_tail), df1_jsj["official_update_time"].map(lambda x:x.strftime("%Y-%m-%d")), df1_jsj[columns_name1],
              yaxis_label_textsize="50%",
              xaxis_label_textsize="50%",
              is_legend_show=False,
              yaxis_max=12000,
    # yaxis_force_interval="vertical"
    xaxis_rotate="30",
    yaxis_rotate="30",
              )

    line7 = Line("雅砻江", title_text_size="80%", title_pos="50%", title_top="50%")
    line7.add("雅砻江{}".format(df1_tail), df1_ylj["official_update_time"].map(lambda x:x.strftime("%Y-%m-%d")), df1_ylj[columns_name1],
              yaxis_label_textsize="50%",
              xaxis_label_textsize="50%",
              is_legend_show=False,
            yaxis_max=12000,
    xaxis_rotate="30",
    yaxis_rotate="30",
              )

    line8 = Line("青衣江", title_text_size="80%", title_pos="75%", title_top="50%")
    line8.add("青衣江{}".format(df1_tail), df1_qyj["official_update_time"].map(lambda x:x.strftime("%Y-%m-%d")), df1_qyj[columns_name1],
              yaxis_label_textsize="50%",
              xaxis_label_textsize="50%",
              is_legend_show=False,
              yaxis_max=12000,
    xaxis_rotate="30",
    yaxis_rotate="30",
              )

    grid.add(line1, grid_right="75%", grid_bottom="55%", grid_left="2.5%")
    grid.add(line2, grid_right="50%", grid_bottom="55%", grid_left="27.5%")
    grid.add(line3, grid_right="25%", grid_bottom="55%", grid_left="52.5%")
    grid.add(line4, grid_right="0%", grid_bottom="55%", grid_left="77.5%")

    grid.add(line5, grid_right="75%", grid_top="55%", grid_left="2.5%")
    grid.add(line6, grid_right="50%", grid_top="55%", grid_left="27.5%")
    grid.add(line7, grid_right="25%", grid_top="55%", grid_left="52.5%")
    grid.add(line8, grid_right="0%", grid_top="55%", grid_left="77.5%")

    grid.render(pic_name)


if __name__ == '__main__':
    plot_inflow_of_all_main_river()
    plot_in_out_of_all_main_river()
    plot_in_out_8_river()
    plot_storage_8_river()