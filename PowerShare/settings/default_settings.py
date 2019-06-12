"""
This module contains the default values for all settings used by Scrapy.

For more information about these settings you can read the settings
documentation in docs/topics/settings.rst

Scrapy developers, if you add a setting here remember to:

* add it in alphabetical order
* group similar settings without leaving blank lines
* add its documentation to the available settings documentation
  (docs/topics/settings.rst)

"""

import os
import sys
from importlib import import_module
from os.path import join, abspath, dirname

import six


MYSQL_HOST = "172.16.15.49"
MYSQL_PORT = "3306"
MYSQL_DB = "sc_electric_trade"


MONGO_HOST = "172.16.15.49"
MONGO_PORT = 27017
MONGO_DB = "市场主体信息"


TRADE_TABLE = "集中撮合交易监控界面展示"
FSCH_TABLE = "复式撮合盘口信息"
GPJY_TABLE = "挂牌交易交易详细信息"
JZZR_TABLE = "集中撮合交易监控界面展示"

FSCH_TABLE_TRADE_DETAIL = {
    "declare_gf": "fsch_declare_loadGfData",
    "declare_fgtj": "fsch_declare_loadGfTjData",
    "declare_sf":"fsch_declare_loadSfData",
    "declare_sftj":"fsch_declare_loadSfTjData",
    "after_loadchart":"fsch_loadchartsprice",
    # "after_loadchart": "fsch_loadchats",
    # "fsch_loadchatssgsz",
    # "fsch_loadDwxx",
    # "fsch_loadZpData",
    # "fsch_showInfo2",
}


TRADE_TYPE_MAP = {
    "1": "复式撮合交易详细信息",
    "0": "挂牌交易交易详细信息",
    "2": "集中转让交易详细信息"
}

TRADE_TYPE_MAP2 = {
    'fsch': "复式撮合交易详细信息",
    'gpjy': "挂牌交易交易详细信息",
    'jzzr': "集中转让交易详细信息"
}


TABLE_STATUS = {
    0: "unfinish",
    1: "finish",
    3: "ignore",
    10: "is_updating"
}

