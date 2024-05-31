import datetime
import os

import numpy as np
import pandas as pd
from PDDCleanTool.common.CommonUtil import CommonUtil

def 订单全状态表(path):
    所有文件名列表 = os.listdir(path)
    for 文件名 in 所有文件名列表:
        if '订单表' in 文件名:
            order_data = CommonUtil().读取表格(path,文件名);
        elif '账单表' in 文件名:
            bill_data =  CommonUtil().读取表格(path,文件名);


if __name__ == '__main__':
    订单全状态表('C:\\Users\\xwb\\Desktop\\拼多多-MVAV鞋服工厂店\\拼多多-MVAV鞋服工厂店\\2、清洗后');