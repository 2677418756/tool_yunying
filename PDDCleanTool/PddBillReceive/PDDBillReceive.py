import datetime
import os
import time

import numpy as np
import pandas as pd
from PDDCleanTool.common.CommonUtil import CommonUtil

def 账单回款表(path):
    所有文件名列表 = os.listdir(path)
    for 文件名 in 所有文件名列表:
        if '订单表' in 文件名:
            order_data = CommonUtil().读取表格(path,文件名);
        elif '账单表' in 文件名:
            bill_data =  CommonUtil().读取表格(path,文件名);
        else:
            continue

    order_data=order_data.loc[:,['订单号','订单成交时间']]
    order_data['订单成交时间'] = pd.to_datetime(order_data['订单成交时间'] , errors='coerce')
    order_data['订单成交时间'] = np.where(order_data.订单成交时间.notnull(), order_data.订单成交时间.dt.strftime('%Y-%m-%d'), '2000-01-01')
    order_data['订单成交时间'] = order_data['订单成交时间'].astype('datetime64[ns]')

    bill_data.rename(columns={'商户订单号': '订单号'}, inplace=True)
    bill_data.rename(columns={'收入金额（+元）': '收入金额'}, inplace=True)
    bill_data.rename(columns={'支出金额（-元）': '支出金额'}, inplace=True)
    bill_data['收入金额'] =  bill_data['收入金额'].astype(np.float)
    bill_data['支出金额'] = bill_data['支出金额'].astype(np.float)
    bill_data['发生时间'] = pd.to_datetime(bill_data['发生时间'], errors='coerce')
    bill_data['发生时间'] = np.where(bill_data.发生时间.notnull(),bill_data.发生时间.dt.strftime('%Y-%m-%d'), '2000-01-01')
    bill_data['发生时间'] = bill_data['发生时间'].astype('datetime64[ns]')

    bill_order_data = pd.merge(bill_data, order_data, how='left', on='订单号')
    bill_order_data['天数'] = bill_order_data['发生时间'] - bill_order_data['订单成交时间']
    bill_order_data['天数'] = bill_order_data['天数'].astype(str)
    bill_order_data['天数'] = bill_order_data['天数'].str.split(" ", expand=True)[0]
    bill_order_data['天数'] = bill_order_data['天数'].apply(lambda x: '第'+x+'天')
    bill_order_data['金额'] = bill_order_data['收入金额']+bill_order_data['支出金额']

    grouped = bill_order_data.groupby(['订单成交时间','天数'], as_index=True)
    settle_amount_data = grouped['金额'].sum()
    settle_amount_data = settle_amount_data.reset_index()

    settle_amount_data=pd.pivot_table(
        settle_amount_data,
        index=['订单成交时间'],
        columns=['天数'],
        values=['金额']
    )
    return settle_amount_data

if __name__ == '__main__':
    账单回款表('C:\\Users\\xwb\\Desktop\\拼多多-MVAV鞋服工厂店\\拼多多-MVAV鞋服工厂店\\2、清洗后');