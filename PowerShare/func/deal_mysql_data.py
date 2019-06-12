#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/12 0012 13:56
# @Author  : LiangLiang
# @Site    : 
# @File    : deal_mysql_data.py
# @Software: PyCharm
import sys,os
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(basedir))
sys.path.append(basedir)
import pandas as pd
from sqlalchemy.orm.session import sessionmaker
from PowerShare.settings import Settings
from PowerShare.func.new_sql_types import *
from utils.db_manage import init_engine



class FSCHReader(object):
    def __init__(self):
        self.settings = Settings()
        self.settings.setmodule("PowerShare.setting", priority="project")
        self.engine = init_engine()

    def get_turnover_ratio(self, trade_id):
        """
        获取成交占比的详细信息
        :return:
        """
        df = pd.read_sql("select * from `fsch_loadchartsprice` where trade_id='{trade_id}'".format(
            trade_id=trade_id
        ), self.engine)
        return df

    def get_ticket_data(self, trade_id, windows_size=10):
        """
        获取盘口的ticket数据
        :param trade_id:
        :param windows_size: max 50
        :return:
        """
        df = pd.read_sql("select * from `复式撮合盘口信息` where trade_id = '{trade_id}'".format(
            trade_id=trade_id
        ), self.engine)
        return df

    def get_pankou(self, trade_id):
        pass

    def get_trade_record(self, trade_id):
        """
        获取成交记录信息
        :param trade_id:
        :return:
        """
        df1 = pd.read_sql("select * from `fsch_loadZpData` where  trade_id='{trade_id}'".format(
            trade_id=trade_id
        ), self.engine)
        unique_df = df1.drop_duplicates(subset=["time", "energy", "price"], keep="first")
        return unique_df

    def get_declare_info(self):
        gouf_df = pd.read_sql("")


if __name__ == '__main__':
    thisclass = FSCHReader()
    df1 = thisclass.get_trade_record(trade_id="1210003393")
    print(df1)







