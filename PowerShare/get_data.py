#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/11 0011 7:03
# @Author  : LiangLiang
# @Site    : 
# @File    : get_data.py
# @Software: PyCharm
import os,sys
basedir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(basedir)
import pandas as pd
import numpy as np
from sqlalchemy.engine import create_engine
from settings import Settings
from utils.db_manage import init_engine


settings = Settings()
setting_path = "PowerShare.setting"
settings.setmodule(setting_path, priority="project")



def get_trade_data(start_time, end_time, trade_id):
    engine = init_engine()
    df = pd.read_sql("select * from fsch_declare_loadDataByTime where trade_id = {trade_id}".format(
        trade_id=trade_id
    ))


def get_basic_trade_table():
    engine = init_engine()
    basic_table = settings["TRADE_TABLE"]
    df = pd.read_sql("select * from {basic_trade_table}".format(basic_trade_table=basic_table), engine)
    del engine
    print(df)


def get_detal_trade_table(basic_table_id=None, detail_table_id=None, trade_type=None):
    """
    用来获得某场交易的详细信息！
    :param basic_table_id:  某批次的所有交易信息
    :param detail_table_id:  具体某批次中某场交易的详细信息
    :param trade_type: 交易的详细
    :return:
    """
    assert basic_table_id or detail_table_id, "至少必须指明一个交易id"
    assert not(basic_table_id and detail_table_id), "只能指明一个id"
    if detail_table_id:
        assert trade_type, "必须指明交易类型"
    assert trade_type in ["fsch", "jzzr", "gpjy"], "交易必须是‘复式撮合’， ‘集中转让’， ‘挂牌交易’中的某一个"
    engine = init_engine()

    basic_table = settings["TRADE_TABLE"]
    map_relation = settings["TRADE_TYPE_MAP"]
    map_relation2 = settings["TRADE_TYPE_MAP2"]
    detail_table = map_relation2[trade_type]

    if basic_table_id:
        df1 = pd.read_sql("select * from {basic_trade_table} WHERE trade_id ='{trade_id}'".format(
            basic_trade_table=basic_table, trade_id=basic_table_id
        ), engine)
        if not df1.empty:
            trade_type = df1["trade_type"].values[0]
            table_name = map_relation[str(trade_type)]
            if trade_type != "0":
                detail_table = pd.read_sql("select * from {detail_table} where `GROUP_ID`='{basic_table_id}' ".format(
                    detail_table=table_name, basic_table_id=basic_table_id
                ), engine)
            else:
                detail_table = pd.read_sql("select * from {detail_table} where `KEY`='{basic_table_id}' ".format(
                    detail_table=table_name, basic_table_id=basic_table_id
                ), engine)
            return detail_table
        else:
            raise Exception("交易_{trade_id}__不存在！！".format(trade_id=basic_table_id))
    else:

        try:
            if detail_table:
                if trade_type != "gpjy":
                    df_detail = pd.read_sql("select * from {detail_table} where `TRID`='{trade_id}'".format(
                        detail_table=detail_table, trade_id=detail_table_id
                    ), engine)
                else:
                    df_detail = pd.read_sql("select * from {detail_table} where `KEY`='{trade_id}'".format(
                        detail_table=detail_table, trade_id=detail_table_id
                    ), engine)
                return df_detail
        except Exception as e:
            print(e)


def get_fsch_detail(trade_id):
    assert trade_id, "必须指明交易id"
    engine = init_engine()




if __name__ == '__main__':
    # get_basic_trade_table()
    # r = get_detal_trade_table(detail_table_id="863D3F5D31509326E053D228B00A625C", trade_type="jzzr")
    # print(r)
    print(get_basic_trade_table())
