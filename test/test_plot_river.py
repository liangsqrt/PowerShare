#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/17 0017 10:52
# @Author  : LiangLiang
# @Site    : 
# @File    : test_plot_river.py
# @Software: PyCharm
from PowerShare.func.river import get_river



if __name__ == '__main__':
    river_df = get_river()
    print(river_df)