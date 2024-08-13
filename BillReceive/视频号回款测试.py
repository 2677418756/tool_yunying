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
            订单表 = CommonUtil().读取表格(path, 文件名);
        elif '订单流水表' in 文件名:
            订单流水表 = CommonUtil().读取表格(path, 文件名);
        else:
            continue
    订单流水表['实际结算金额'] = 订单流水表['实际结算金额'].astype(float)
    bill_data_start = 订单流水表

    订单表 = 订单表.loc[:, ['订单号', '订单创建日期']]
    订单表['订单创建日期'] = pd.to_datetime(订单表['订单创建日期'], errors='coerce')
    订单表['订单创建日期'] = np.where(订单表.订单创建日期.notnull(),
                                          订单表.订单创建日期.dt.strftime('%Y-%m-%d'), '2000-01-01')
    订单表['订单创建日期'] = 订单表['订单创建日期'].astype('datetime64[ns]')

    订单流水表 = 订单流水表[~订单流水表.商家结算时间.isin(["-"])]
    订单流水表['商家结算时间'] = pd.to_datetime(订单流水表['商家结算时间'], errors='coerce')
    订单流水表['商家结算时间'] = np.where(订单流水表.商家结算时间.notnull(), 订单流水表.商家结算时间.dt.strftime('%Y-%m-%d'),
                                     '2000-01-01')
    订单流水表['商家结算时间'] = 订单流水表['商家结算时间'].astype('datetime64[ns]')

    bill_order_data = pd.merge(订单流水表, 订单表, how='left', on='订单号')
    bill_order_data['天数'] = bill_order_data['商家结算时间'] - bill_order_data['订单创建日期']
    bill_order_data['天数'] = bill_order_data['天数'].astype(str)
    bill_order_data['天数'] = bill_order_data['天数'].str.split(" ", expand=True)[0]
    bill_order_data['天数'] = bill_order_data['天数'].apply(lambda x: '第' + x + '天')

    grouped = bill_order_data.groupby(['订单创建日期', '天数'], as_index=True)
    settle_amount_data = grouped['实际结算金额'].sum()
    settle_amount_data = settle_amount_data.reset_index()

    settle_amount_data = pd.pivot_table(
        settle_amount_data,
        index=['订单创建日期'],
        columns=['天数'],
        values=['实际结算金额']
    )
    settle_amount_data["实际结算金额"] = settle_amount_data["实际结算金额"].fillna(0)


    # 设置格式
    settle_amount_data.columns = settle_amount_data.columns.droplevel(0)
    settle_amount_data = settle_amount_data.reset_index()
    settle_amount_data["订单创建日期"] = settle_amount_data["订单创建日期"].apply(lambda x: str(x)[:10])
    settle_amount_data = settle_amount_data.set_index("订单创建日期")

    # 根据天数进行排序
    column_numbers = [int(col.split('第')[1].split('天')[0]) for col in settle_amount_data.columns]
    # 根据数字部分对列名进行排序
    sorted_columns = [x for _, x in sorted(zip(column_numbers, settle_amount_data.columns))]

    # 按照排序后的列名重新排列 DataFrame
    df_sorted = settle_amount_data[sorted_columns]

    df_sorted.to_excel("D:/账单回款表.xlsx",sheet_name="账单回款明细表")


    bill_data_start['商家结算时间'] = 订单流水表['商家结算时间'].apply(lambda x:str(x).split(" ")[0])

    处理 = pd.pivot_table(订单流水表, index=['商家结算时间'],
                          values=['实际结算金额'],
                          aggfunc={'实际结算金额': np.sum})
    处理.index.name = "实际结算日期"
    处理 = 处理.sort_index()
    with pd.ExcelWriter("D:/账单回款表.xlsx", mode='a') as writer:
        处理[["实际结算金额"]].to_excel(writer, sheet_name="账单回款总表")


    df_sorted["总计金额"] = 0
    for i in range(0,len(df_sorted.columns) - 1):
        df_sorted["总计金额"] += df_sorted[df_sorted.columns[i]]
    with pd.ExcelWriter("D:/账单回款表.xlsx", mode='a') as writer:
        df_sorted[["总计金额"]].to_excel(writer, sheet_name="订单创建日期回款表")


if __name__ == '__main__':
    账单回款表('D:/work/运营/视频号/视频号-MVAV鞋服工厂店/2、清洗后')
