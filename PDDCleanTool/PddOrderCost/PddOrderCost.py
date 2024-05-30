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

    bill_data.rename(columns={'商户订单号': '订单号'}, inplace=True)
    bill_data.rename(columns={'收入金额（+元）': '收入金额'}, inplace=True)
    bill_data.rename(columns={'支出金额（-元）': '支出金额'}, inplace=True)
    bill_data['收入金额'] = bill_data['收入金额'].apply(lambda x: abs(float(x)))
    bill_data['支出金额'] = bill_data['支出金额'].apply(lambda x: abs(float(x)))
    #结算状态为 交易收入
    settle_status_data = bill_data[bill_data['账务类型'].isin(['交易收入'])]
    settle_status_data = settle_status_data.loc[:,['订单号','账务类型','发生时间']]

    #结算金额
    settle_amount_data=bill_data.loc[:,['订单号','收入金额','支出金额']]
    settle_amount_data=settle_amount_data.set_index('订单号')
    settle_amount_data['收入金额']
    settle_amount_data=pd.pivot_table(
        settle_amount_data,
        index=['订单号'],
        values=['收入金额','支出金额'],
        aggfunc = {'收入金额': np.sum,'支出金额': np.sum}
    )
    settle_amount_data['实际结算金额']=settle_amount_data['收入金额']-settle_amount_data['支出金额']

    # 订单-账单状态-账单金额   连接
    order_bill_data = pd.merge(order_data, settle_status_data, how='left', on='订单号')
    order_bill_data = pd.merge(order_bill_data, settle_amount_data, how='left', on='订单号')

    有售后 = order_bill_data[order_bill_data['售后状态'].isin(['退款成功'])]
    无售后 = order_bill_data[~(order_bill_data['售后状态'].isin(['退款成功']))]

    回退 = 有售后[有售后['账务类型'].isin(['交易收入'])]
    已退 = 有售后[~(有售后['账务类型'].isin(['交易收入']))]
    已回 = 无售后[无售后['账务类型'].isin(['交易收入'])]
    待回 = 无售后[~(无售后['账务类型'].isin(['交易收入']))]

    回退['回退状态'] = '回退'
    已退['回退状态'] = '已退'
    已回['回退状态'] = '已回'
    待回['回退状态'] = '待回'
    合并数据 = pd.concat([回退, 已退, 已回, 待回])
    pd.DataFrame(合并数据).to_csv('aa.csv')
    print()

if __name__ == '__main__':
    订单全状态表('C:\\Users\\xwb\\Desktop\\拼多多-MVAV鞋服工厂店\\拼多多-MVAV鞋服工厂店\\2、清洗后');