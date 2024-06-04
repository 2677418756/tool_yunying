# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 15:42:36 2022

@author: Admin
"""

import pandas as pd
import os
import numpy as np
import datetime
from PDDCleanTool.common.CommonUtil import CommonUtil

#【笔记】小店自卖的订单不会出现在联盟表，还有部分订单编号不会出现在团长表，所以合并表格时不能用inner
def 揽收成本速度表(path):
    所有文件名列表 = os.listdir(path)
    for 文件名 in 所有文件名列表:
        if '订单表' in 文件名:
            order_data = CommonUtil().读取表格(path,文件名);
        elif '账单表' in 文件名:
            bill_data = CommonUtil().读取表格(path,文件名);
        elif  '推广表' in 文件名:
            promotion_data = CommonUtil().读取表格(path, 文件名);



if __name__ == '__main__':
    揽收成本速度表('C:\\Users\\huanglipan\\Desktop\\拼多多-MVAV鞋服工厂店\\拼多多-MVAV鞋服工厂店\\2、清洗后');

