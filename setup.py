#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/11 0011 6:40
# @Author  : LiangLiang
# @Site    : 
# @File    : setup.py
# @Software: PyCharm
import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="PowerShare",
    version="0.0.1",
    author="liangl",
    author_email="liangsqrt@163.com",
    description="四川电力交易中心的交易数据分享工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liangl/PowerShare.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='==3.6.*,',
    install_requires=[
        'pyecharts==0.5.x',
        'pandas>=0.24.1',
        'sqlalchemy>=1.2.17',
        '',
        'lxml',
        'pyOpenSSL',
        'cssselect>=0.9',
        'six>=1.5.2',
        'parsel>=1.5',
        'PyDispatcher>=2.0.5',
        'service_identity',
    ],

)