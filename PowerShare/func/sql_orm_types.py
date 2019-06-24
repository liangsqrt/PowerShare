#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/18 0018 16:30
# @Author  : LiangLiang
# @Site    :
# @File    : sql_types.py
# @Software: PyCharm
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative.api import AbstractConcreteBase
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, Float, VARCHAR, JSON, Text, Time, DATE, Index
Base = declarative_base()


#-------------------------------复式撮合页面的数据格式-------------------------------#

class CommonBase(AbstractConcreteBase, Base):
    """
    所有连接请求，都必须包含的字段，主要是时间，精确到*秒，用来唯一定位数据
    """
    spider_time = Column(DateTime(), nullable=False, default=0, primary_key=True)
    trade_id = Column(VARCHAR(length=100), default=0, primary_key=True)
    trade_name = Column(String(length=40), nullable=False, primary_key=True)
    trade_type = Column(String(length=10), nullable=False, primary_key=True)
    trade_time = Column(DateTime(), nullable=False, primary_key=True)


class loadcharts(CommonBase):
    """
    集中竞价的前30分钟情况
    """
    __tablename__ = "fsch_loadchats"
    energy = Column(Float(), default=0)
    role = Column(Integer(), nullable=False, default=1)
    roles = Column(Integer(), default=1)
    s_time = Column(String(20), nullable=False, default=0)
    sb_count = Column(Integer(), default=0)
    t_time = Column(String(length=20), default="")
    time = Column(DateTime(), default=0)
    freq = Column(Integer(), nullable=False, default=0)
    __table_args__ = (Index("unique_index", "trade_id", "trade_time", unique=True),
                      {"comment": "集中竞价模块1中的数据,对应前30分钟的数据"})



class loadchartsprice(CommonBase):
    __tablename__ = "fsch_loadchartsprice"
    energy = Column(Integer(), default=1)
    zb = Column(Float(), default=0)
    price = Column(String(length=10), default="", primary_key=True)
    price1 = Column(Float(), default=0)
    __table_args__ = (Index("unique_index", "trade_id", "trade_time", unique=True),
                      {"comment": "复式撮合中，成交占比的模块的数据"})


class loadDwxx(CommonBase):
    __tablename__ = "fsch_loadDwxx"
    energy = Column(Integer(), nullable=False, default=1)
    energys = Column(Text(), nullable=False, default=1)
    name = Column(String(40), nullable=False, default=1, primary_key=True)
    price = Column(Float(), default=0)
    rownum = Column(Integer(), default=0)
    __table_args__ = (Index("unique_index", "trade_id", "trade_time", unique=True),
                      {"comment": "复式撮合的盘口数据"})


class loadZpData(CommonBase):
    __tablename__ = "fsch_loadZpData"
    energy = Column(Integer(), nullable=False, default=1)
    price = Column(Float(), nullable=False, default=1)
    time = Column(Time(), nullable=False, default=1, primary_key=True)
    type = Column(String(10), nullable=False, default=1, primary_key=True)
    __table_args__ = (Index("unique_index", "trade_id", "trade_time", unique=True),
                      {"comment": "复式撮合-chengjiaojilu"})


class showInfo2(CommonBase):
    __tablename__ = "fsch_showInfo2"
    id = Column(String(20), nullable=False, default=1, primary_key=True)
    key = Column(String(20), nullable=False, default=1)
    value = Column(Integer(), nullable=False, default=1)
    text = Column(String(40), nullable=False, default=1)
    c = Column(Integer(), nullable=False, default=1)
    __table_args__ = (Index("unique_index", "trade_id", "trade_time", unique=True), {"comment": "复式撮合-展示信息"})


class loadchatssgsz(CommonBase):
    __tablename__ = "fsch_loadchatssgsz"
    g_energy = Column(Integer(), nullable=False, default=0)
    price = Column(Float(), nullable=False, default=0)
    s_energy = Column(Integer(), nullable=False, default=0)
    t_time = Column(String(20), nullable=False, default=0)
    time = Column(DateTime(), nullable=False, default="", primary_key=True)
    __table_args__ = (Index("unique_index", "trade_id", "trade_time", unique=True),
                      {"comment": "复式撮合-双挂双摘阶段的购方信息。"})


#------申报阶段---------
class loadSfData(CommonBase):
    __tablename__ = "fsch_declare_loadSfData"
    busiunitname = Column(String(length=100), nullable=False, primary_key=True)
    code = Column(String(length=40), nullable=False, primary_key=True)
    energy = Column(Integer())
    __table_args__ = (Index("unique_index", "trade_id", "trade_time", unique=True),
     {"comment": "复式撮合-申报阶段-售方信息。"})


class loadSfTjData(CommonBase):
    __tablename__ = "fsch_declare_loadSfTjData"
    count = Column(Integer())
    energy = Column(Integer())
    __table_args__ = (Index("unique_index", "trade_id", "trade_time", unique=True),
                      {"comment": "复式撮合-申报阶段-售方提交的记录"})


class loadGfTjData(CommonBase):
    __tablename__ = "fsch_declare_loadGfTjData"
    count = Column(Integer())
    energy = Column(Integer())
    __table_args__ = (Index("unique_index", "trade_id", "trade_time", unique=True),
                      {"comment": "复式撮合-申报阶段-购方提交的记录"})


class loadGfData(CommonBase):
    __tablename__ = "fsch_declare_loadGfData"
    busiunitname = Column(String(100), primary_key=True)
    code = Column(String(40), primary_key=True)
    energy = Column(Integer())
    __table_args__ = (Index("unique_index", "trade_id", "trade_time", unique=True),
                      {"comment": "复式撮合-申报阶段-购方信息"})


class loadDataByTime(CommonBase):
    __tablename__ = "fsch_declare_loadDataByTime"
    busiunitname = Column(String(length=100), primary_key=True)
    energy = Column(Integer())
    sb_time = Column(Time(), primary_key=True)
    type = Column(Integer())
    __table_args__ = (Index("unique_index", "trade_id", "trade_time", unique=True),
                      {"comment": "复式撮合-申报阶段-购售双方提交的历史记录信息"})


#-----------------------------挂牌交易类型的页面数据格式-----------------------------------#

class gpjy_loadInfoData(CommonBase):
    __tablename__ = "gpjy_InfoData"
    avg_price = Column(String(length=40))
    cj_energy = Column(String(length=40))
    gf_count = Column(String(length=40))
    gf_energy = Column(String(length=40))
    max_price = Column(String(length=40))
    min_price = Column(String(length=40))
    sf_count = Column(String(length=40))
    sf_energy = Column(String(length=40))
    zb = Column(String(length=40))
    __table_args__ = (Index("unique_index", "trade_id", "trade_time", unique=True),
                      {"comment": "挂牌交易-申报阶段-购售双方提交的历史记录信息"})


class gpjy_loadChartData(CommonBase):
    __tablename__ = "gpjy_ChartData"
    dl = Column(Float())
    js = Column(Float())
    time = Column(Time())


class gpjy_loadSbData(CommonBase):
    __tablename__ = "gpjy_SbData"
    pass


class gpjy_loadGpData(CommonBase):
    __tablename__ = "gpjy_loadGpData"
    title = Column(String(length=40))
    tz = Column(Integer())
    dl_price = Column(Float())
    energy = Column(Float())
    fqbl = Column(Float())
    fqdl = Column(Float())
    gp_energy = Column(Float())
    gp_price = Column(Float())
    guid = Column(String(length=100))
    jydyid = Column(String(length=100))
    jydy_name = Column(String(length=100))
    key = Column(String(length=100))
    kqbl = Column(Float())
    kqdl = Column(Float())
    pqbl = Column(Float())
    pqdl = Column(Float())
    prid = Column(String(100))
    sy_energy = Column(Float())
    s_energy = Column(Float())
    type = Column(String(length=40))
    xh = Column(Float())
    xs = Column(Float())
    # ycj = Column(Float())
    # yhdm = Column(String(length=100))


##------------------------集中转让申报阶段的数据格式---------------------------------
#### -----申报阶段----
class declare_loadZrfData(CommonBase):
    """
    转让方的申报情况
    """
    __tablename__ = "jzzr_declare_loadzrfdata"
    busiunitname = Column(String(length=100), primary_key=True)
    code = Column(String(40), primary_key=True)
    energy = Column(Float())
    __table_args__ = (Index("unique_index", "trade_id", "trade_time", unique=True),
                      {"comment": "集中转让-转让方信息"})


class declare_loadSrfData(CommonBase):
    """
    受让方的挂单情况
    """
    __tablename__ = "jzzr_declare_loadsrfdata"
    busiunitname = Column(String(length=100), primary_key=True)
    code = Column(String(40), primary_key=True)
    energy = Column(Float())
    __table_args__ = (Index("unique_index", "trade_id", "trade_time", unique=True),
                      {"comment": "集中转让-受让方信息"})


class declare_loadDataByTimeZr(CommonBase):
    """
    各个时刻的买卖双方的申报情况
    """
    __tablename__ = "jzzr_declare_loaddatabytimezr"
    busiunitname = Column(String(length=100), primary_key=True)
    code = Column(String(40), primary_key=True)
    energy = Column(Float())
    sb_time = Column(DateTime())
    type = Column(Integer())
    __table_args__ = (Index("unique_index", "trade_id", "trade_time", unique=True),
                      {"comment": "集中转让-双方时间序列的信息"})


class declare_showInfo(CommonBase):
    """
    本次交易的总体概览
    """
    __tablename__ = "jzzr_declare_showinfo"
    id = Column(String(40))
    key = Column(String(100), primary_key=True)
    text = Column(String(40))
    value = Column(String(100), primary_key=True)
    __table_args__ = (Index("unique_index", "trade_id", "trade_time", unique=True),
                      {"comment": "集中转让-总体信息"})


class declare_go3(CommonBase):
    """
    无用
    """
    __tablename__ = "jzzr_declare_go3"


#### ----集中竞价阶段----
class jzzr_loadchartsprice(CommonBase):
    __tablename__ = "jzzr_loadchartsprice"
    energy = Column(Float(), default=1)
    zb = Column(Float(), default=0)
    price = Column(String(length=10), default="", primary_key=True)
    price1 = Column(Float(), default=0)
    __table_args__ = (Index("unique_index", "trade_id", "trade_time", unique=True),
                      {"comment": "集中转让-各个价位的占比"})


class jzzr_loadcharts(CommonBase):
    """
    """
    __tablename__ = "jzzr_loadchats"
    energy = Column(Float(), default=0)
    role = Column(Integer(), nullable=False, default=1, primary_key=True)
    roles = Column(Integer(), default=1)
    s_time = Column(String(20), nullable=False, default=0, primary_key=True)
    sb_count = Column(Integer(), default=0)
    t_time = Column(String(length=20), default="")
    time = Column(DateTime(), default=0)
    freq = Column(Integer(), nullable=False, default=0)
    __table_args__ = (Index("unique_index", "trade_id", "trade_time", unique=True),
                      {"comment": "集中转让-前30分钟的申报阶段"})


class jzzr_loadDwxx(CommonBase):
    __tablename__ = "jzzr_loadDwxx"
    energy = Column(Float(), nullable=False, default=1)
    energys = Column(Text(), nullable=False, default=1)
    name = Column(String(40), nullable=False, default=1, primary_key=True)
    price = Column(Float(), default=0)
    rownum = Column(Integer(), default=0)
    __table_args__ = (Index("unique_index", "trade_id", "trade_time", unique=True),
                      {"comment": "集中转让-盘口信息"})


class jzzr_loadZpData(CommonBase):
    __tablename__ = "jzzr_loadZpData"
    energy = Column(Integer(), nullable=False, default=1)
    price = Column(Float(), nullable=False, default=1)
    time = Column(Time(), nullable=False, default=1, primary_key=True)
    type = Column(String(10), nullable=False, default=1, primary_key=True)
    __table_args__ = (Index("unique_index", "trade_id", "trade_time", unique=True),
                      {"comment": "集中转让-成交记录"})


class jzzr_showInfo2(CommonBase):
    __tablename__ = "jzzr_showInfo2"
    id = Column(String(20), nullable=False, default=1, primary_key=True)
    key = Column(String(20), nullable=False, default=1)
    value = Column(Integer(), nullable=False, default=1)
    text = Column(String(40), nullable=False, default=1)
    c = Column(Integer(), nullable=False, default=1)
    __table_args__ = (Index("unique_index", "trade_id", "trade_time", unique=True),
                      {"comment": "集中转让-最终的展示信息"})


class jzzr_loadchatssgsz(CommonBase):
    __tablename__ = "jzzr_loadchatssgsz"
    g_energy = Column(Integer(), nullable=False, default=1)
    price = Column(Float(), nullable=False, default=1)
    s_energy = Column(Integer(), nullable=False, default=1)
    t_time = Column(String(20), nullable=False, default=1)
    time = Column(DateTime(), nullable=False, default="", primary_key=True)
    __table_args__ = (Index("unique_index", "trade_id", "trade_time", unique=True),
                      {"comment": "集中转让-未知"})


class trade_board(Base):
    __tablename__ = "集中撮合交易监控界面展示"
    start_time = Column(DateTime(), nullable=False)
    end_time = Column(DateTime(), nullable=False)
    trade_id = Column(String(100), nullable=False, default=0, primary_key=True)
    trade_name = Column(String(40))
    fz = Column(Integer(),)
    status = Column(Integer(), default=0)
    trade_type = Column(String(10), default="1", nullable=False)
    updated = Column(Integer(), default=0, nullable=False)


class initGroup_FSCH(Base):
    __tablename__ = "复式撮合交易详细信息"
    CJDJ = Column(Float())
    CJDL = Column(Float())
    FZ = Column(Float())
    GF_SJ = Column(Float())
    GF_ZL = Column(Float())
    GROUP_ID = Column(String(100))
    SF_SJ = Column(Float())
    SF_ZL = Column(Float())
    STATU = Column(Float())
    TRID = Column(String(40), primary_key=True)
    TRNAME = Column(String(40))
    msg = Column(String(40))

    updated= Column(Integer(), default=0)


class initGroup_GPJY(Base):
    __tablename__ = "挂牌交易交易详细信息"
    NAME = Column(String(length=100))
    CJ_ENERGY = Column(Float())
    GP_ENERGY = Column(Float())
    FZ = Column(Float())
    YNS = Column(DATE())
    SFM = Column(Time())
    CJ_PRICE = Column(Float())
    ZPF_ENERGY = Column(Float())
    KEY = Column(String(length=100), primary_key=True)
    ZPF_COUNT = Column(Float())
    STATU = Column(Float())
    GP_COUNT = Column(Float())

    updated= Column(Integer(), default=0)


class initGroup_JZZR(Base):
    __tablename__ = "集中转让交易详细信息"
    ENERGY = Column(Integer())
    GROUP_ID = Column(String(100), primary_key=True)
    ID = Column(String(100), primary_key=True)
    PRICE = Column(Float())
    SRF_JS = Column(Integer())
    SRF_ZL = Column(Integer())
    STATU = Column(Integer())
    TRID = Column(String(100), primary_key=True)
    TRNAME = Column(String(100))
    ZRF_JS = Column(Integer())
    ZRF_ZL = Column(Integer())
    updated = Column(Integer(), default=0)


class FSCH_pankou(Base):
    """
    使用方法,先实例化，再做base的crate_all
    """
    __tablename__ = "复式撮合盘口信息"
    trade_time = Column(DateTime(),nullable=False, primary_key=True)
    trade_id = Column(VARCHAR(100), nullable=False, primary_key=True)
    created = False

    @classmethod
    def __build_buyer_sealer_structure__(cls):
        for i in range(50, 0, -1):
            setattr(cls, "ask_{}".format(str(i)), Column(Float()))
            setattr(cls, "ask_volume_" + str(i), Column(Integer()))

        for i in range(1,51):
            setattr(cls, "buy_{}".format(str(i)), Column(Float()))
            setattr(cls, "buy_volume_{}".format(str(i)), Column(Integer()))

    def __new__(cls, *args, **kwargs):
        if not cls.created:
            cls.__build_buyer_sealer_structure__()
            cls.created = True
        return super(FSCH_pankou, cls).__new__(cls, *args, **kwargs)

