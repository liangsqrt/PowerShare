#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/11 0011 6:40
# @Author  : LiangLiang
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
import codecs
import os
from PowerShare.settings import Settings
from PowerShare.func.trade import *

__version__ = "0.0.1"
__author__ = "liangl"


class PowerShare(object):
    def __init__(self):
        self.fsch = FSCHReader()
        self.jzzr = JZZRReader()
        self.gpjy = GPJYReader()
        self.settging = Settings()

    @classmethod
    def from_setting(cls, setting_module):
        s = cls()
        setting = Settings()
        setting.setmodule(setting_module, priority="user")
        s.settings = setting
        return s



if __name__ == '__main__':
    thisclass = PowerShare()
    df1 = thisclass.fsch.get_trade_record(trade_id="1210003486")
    print(df1)
