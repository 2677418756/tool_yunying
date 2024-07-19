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
            order_data = CommonUtil().读取表格(path, 文件名);
        elif '账单表' in 文件名:
            bill_data = CommonUtil().读取表格(path, 文件名);
        else:
            continue
    bill_data_start = bill_data

    order_data = order_data.loc[:, ['订单号', '订单成交时间']]
    order_data['订单成交时间'] = pd.to_datetime(order_data['订单成交时间'], errors='coerce')
    order_data['订单成交时间'] = np.where(order_data.订单成交时间.notnull(),
                                          order_data.订单成交时间.dt.strftime('%Y-%m-%d'), '2000-01-01')
    order_data['订单成交时间'] = order_data['订单成交时间'].astype('datetime64[ns]')

    bill_data.rename(columns={'商户订单号': '订单号'}, inplace=True)
    bill_data.rename(columns={'收入金额（+元）': '收入金额'}, inplace=True)
    bill_data.rename(columns={'支出金额（-元）': '支出金额'}, inplace=True)
    bill_data['收入金额'] = bill_data['收入金额'].astype(float)
    bill_data['支出金额'] = bill_data['支出金额'].astype(float)
    bill_data['发生时间'] = pd.to_datetime(bill_data['发生时间'], errors='coerce')
    bill_data['发生时间'] = np.where(bill_data.发生时间.notnull(), bill_data.发生时间.dt.strftime('%Y-%m-%d'),
                                     '2000-01-01')
    bill_data['发生时间'] = bill_data['发生时间'].astype('datetime64[ns]')

    bill_order_data = pd.merge(bill_data, order_data, how='left', on='订单号')
    bill_order_data['天数'] = bill_order_data['发生时间'] - bill_order_data['订单成交时间']
    bill_order_data['天数'] = bill_order_data['天数'].astype(str)
    bill_order_data['天数'] = bill_order_data['天数'].str.split(" ", expand=True)[0]
    bill_order_data['天数'] = bill_order_data['天数'].apply(lambda x: '第' + x + '天')
    bill_order_data['金额'] = bill_order_data['收入金额'] + bill_order_data['支出金额']

    grouped = bill_order_data.groupby(['订单成交时间', '天数'], as_index=True)
    settle_amount_data = grouped['金额'].sum()
    settle_amount_data = settle_amount_data.reset_index()

    settle_amount_data = pd.pivot_table(
        settle_amount_data,
        index=['订单成交时间'],
        columns=['天数'],
        values=['金额']
    )

    settle_amount_data["金额"] = settle_amount_data["金额"].fillna(0)

    settle_amount_data["金额"] = settle_amount_data["金额"].astype(float)

    # 设置格式
    settle_amount_data.columns = settle_amount_data.columns.droplevel(0)
    settle_amount_data = settle_amount_data.reset_index()
    settle_amount_data["订单成交时间"] = settle_amount_data["订单成交时间"].apply(lambda x: str(x)[:10])
    settle_amount_data = settle_amount_data.set_index("订单成交时间")

    # 根据天数进行排序
    column_numbers = [int(col.split('第')[1].split('天')[0]) for col in settle_amount_data.columns]
    # 根据数字部分对列名进行排序
    sorted_columns = [x for _, x in sorted(zip(column_numbers, settle_amount_data.columns))]

    # 按照排序后的列名重新排列 DataFrame
    df_sorted = settle_amount_data[sorted_columns]

    df_sorted.to_excel("D:/账单回款表.xlsx",sheet_name="账单回款明细表")


    bill_data_start['发生时间'] = bill_data['发生时间'].apply(lambda x:str(x).split(" ")[0])
    bill_data_start["收入金额"] = bill_data_start["收入金额"].astype(float)
    bill_data_start["支出金额"] = bill_data_start["支出金额"].astype(float)

    处理 = pd.pivot_table(bill_data, index=['发生时间'],
                          values=['收入金额','支出金额'],
                          aggfunc={'收入金额': np.sum,'支出金额': np.sum})
    处理["实际结算金额(元)"] = 处理["收入金额"] + 处理["支出金额"]
    处理.index.name = "实际结算日期"
    处理 = 处理.sort_index()
    with pd.ExcelWriter("D:/账单回款表.xlsx", mode='a') as writer:
        处理[["实际结算金额(元)"]].to_excel(writer, sheet_name="账单回款总表")


    df_sorted["总计金额"] = 0
    for i in range(0,len(df_sorted.columns) - 1):
        df_sorted["总计金额"] += df_sorted[df_sorted.columns[i]]
    with pd.ExcelWriter("D:/账单回款表.xlsx", mode='a') as writer:
        df_sorted[["总计金额"]].to_excel(writer, sheet_name="订单创建日期回款表")










if __name__ == '__main__':
    账单回款表('D:/work/运营/熔视界7月17日/拼多多-MVAV鞋服工厂店/2、清洗后')
