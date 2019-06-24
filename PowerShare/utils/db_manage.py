#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/12 0012 9:52
# @Author  : LiangLiang
# @Site    : 
# @File    : db_manage.py
# @Software: PyCharm
import os,sys
basedir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(basedir)
from sqlalchemy.engine import create_engine
from settings import Settings


settings = Settings()
setting_path = "PowerShare.setting"
settings.setmodule(setting_path, priority="project")


def init_engine(user=None, passwd=None, host=None, port=None, db=None):
    user = user if user else settings["MYSQL_USER"]
    passwd = passwd if passwd else settings["MYSQL_PASSWD"]
    host = host if host else settings["MYSQL_HOST"]
    port = port if port else settings["MYSQL_PORT"]
    db = db if db else settings["MYSQL_DB"]
    engine = create_engine(
        "mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}?charset=utf8".format(
            user=user, passwd=passwd, host=host, port=port, db=db
        ))

    return engine