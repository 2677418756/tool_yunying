import os
import pandas as pd
from PDDCleanTool.common.CommonUtil import CommonUtil
import numpy as np

def 账单回款表(path):
    所有文件名列表 = os.listdir(path)
    for 文件名 in 所有文件名列表:
        if '订单表' in 文件名:
            order_data = CommonUtil().读取表格(path,文件名);
        elif '账单表' in 文件名:
            bill_data = CommonUtil().读取表格(path,文件名);
        elif  '推广表' in 文件名:
            promotion_data = CommonUtil().读取表格(path, 文件名);

    order_data['订单成交时间'] = pd.to_datetime(order_data['订单成交时间'])
    order_data['订单成交时间'] = order_data['订单成交时间'].dt.date
    order_data['订单成交时间'] = order_data['订单成交时间'].astype(str)
    bill_data.rename(columns={'收入金额（+元）': '收入金额'}, inplace=True)
    bill_data.rename(columns={'支出金额（-元）': '支出金额'}, inplace=True)
    bill_data['收入金额'] = bill_data['收入金额'].apply(lambda x: abs(float(x)))
    bill_data['支出金额'] = bill_data['支出金额'].apply(lambda x: abs(float(x)))
    bill_data['实际流水金额'] = bill_data['收入金额'] - bill_data['支出金额']
    bill_data['发生时间'] = pd.to_datetime(bill_data['发生时间'])
    bill_data['发生时间'] = bill_data['发生时间'].dt.date
    bill_data['发生时间'] = bill_data['发生时间'].astype(str)
    bill_data.rename(columns={'商户订单号': '订单号'}, inplace=True)
    #根据发生日期进行合并
    settlement_order = pd.pivot_table(bill_data, index=['发生时间'], values=['实际流水金额'], aggfunc={'实际流水金额': np.sum})
    settlement_order.rename(columns={'发生时间': '实际结算日期'}, inplace=True)
    settlement_order.rename(columns={'实际流水金额': '总计金额'}, inplace=True)
    pd.DataFrame(settlement_order).to_csv('C:\\Users\\huanglipan\\Desktop\\settlement_order.csv',float_format='%.2f')


    order_bill_data = pd.merge(bill_data, order_data, how='left', on='订单号')
    transaction_order = pd.pivot_table(order_bill_data, index=['订单成交时间'], values=['实际流水金额'], aggfunc={'实际流水金额': np.sum})
    transaction_order .rename(columns={'实际流水金额': '总计金额'}, inplace=True)
    pd.DataFrame(transaction_order).to_csv('C:\\Users\\huanglipan\\Desktop\\transaction_order.csv',float_format='%.2f')

if __name__ == '__main__':
    账单回款表('C:\\Users\\huanglipan\\Desktop\\拼多多-MVAV鞋服工厂店\\拼多多-MVAV鞋服工厂店\\2、清洗后');