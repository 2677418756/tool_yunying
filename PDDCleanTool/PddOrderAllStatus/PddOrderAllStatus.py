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
        elif ('佣金表' in 文件名) or ('推广表' in 文件名):
            commission_data = CommonUtil().读取表格(path, 文件名);
        elif ('售后表' in 文件名):
            aftersale_data = CommonUtil().读取表格(path, 文件名);
        else:
            continue

    bill_data.rename(columns={'商户订单号': '订单号'}, inplace=True)
    bill_data.rename(columns={'收入金额（+元）': '收入金额'}, inplace=True)
    bill_data.rename(columns={'支出金额（-元）': '支出金额'}, inplace=True)
    bill_data['收入金额'] = bill_data['收入金额'].apply(lambda x: abs(float(x)))
    bill_data['支出金额'] = bill_data['支出金额'].apply(lambda x: abs(float(x)))
    commission_data.rename(columns={'订单编号': '订单号'}, inplace=True)
    commission_data.rename(columns={'预估支付佣金（元）': '预估支付佣金'}, inplace=True)
    commission_data.rename(columns={'预估招商佣金（元）': '预估招商佣金'}, inplace=True)
    aftersale_data.rename(columns={'订单编号': '订单号'}, inplace=True)
    aftersale_data.rename(columns={'同意退款时间': '售后申请时间'}, inplace=True)
    aftersale_data = aftersale_data[aftersale_data['售后状态'].isin(['退款成功'])]
    aftersale_data = aftersale_data.loc[:,['订单号','售后申请时间']]

    #订单佣金（预估支付佣金+预估招商佣金） 每个订单对应一条记录
    commission_est_data = commission_data.loc[:,['订单号','预估支付佣金','预估招商佣金']]
    commission_est_data['预估推广佣金']=commission_est_data['预估支付佣金']+commission_est_data['预估招商佣金']

    #结算状态为 交易收入 每个订单对应一条记录
    settle_status_data = bill_data[bill_data['账务类型'].isin(['交易收入'])]
    settle_status_data = settle_status_data.loc[:,['订单号','账务类型','发生时间']]

    #结算金额 每个订单对应一条记录
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
    #订单-账单状态-账单金额-佣金表 连接
    order_bill_data = pd.merge(order_bill_data,commission_est_data,how='left',on='订单号')
    #订单-账单状态-账单金额-佣金表-售后表 连接
    order_bill_data = pd.merge(order_bill_data,aftersale_data,how='left',on='订单号')

    order_bill_data['订单成交时间']=order_bill_data['订单成交时间'].astype('datetime64[ns]')
    无效数据 = order_bill_data[order_bill_data['订单成交时间'].isna()]
    无效数据['回退状态'] = '已退'

    有效数据 = order_bill_data[~(order_bill_data['订单成交时间'].isna())]
    有售后 = 有效数据[有效数据['售后状态'].isin(['退款成功'])]
    无售后 = 有效数据[~(有效数据['售后状态'].isin(['退款成功']))]

    回退 = 有售后[有售后['账务类型'].isin(['交易收入'])]
    已退 = 有售后[~(有售后['账务类型'].isin(['交易收入']))]
    已回 = 无售后[无售后['账务类型'].isin(['交易收入'])]
    待回 = 无售后[~(无售后['账务类型'].isin(['交易收入']))]
    回退['回退状态'] = '回退'
    已退['回退状态'] = '已退'
    已回['回退状态'] = '已回'
    待回['回退状态'] = '待回'

    合并数据 = pd.concat([回退, 已退, 已回, 待回, 无效数据])
    合并数据['统计时间'] = datetime.datetime.now()

    合并数据.rename(columns={'订单号': '订单编号'}, inplace=True)
    合并数据['商品单号'] = 合并数据['订单编号']
    合并数据.rename(columns={'商家编码-规格维度': '商家编码'}, inplace=True)
    合并数据.rename(columns={'商品': '商品名称'}, inplace=True)
    合并数据.rename(columns={'商品数量(件)': '成交数量'}, inplace=True)
    合并数据.rename(columns={'商家实收金额(元)': '订单应付金额'}, inplace=True)
    合并数据.rename(columns={'订单成交时间': '订单创建时间'}, inplace=True)
    合并数据.rename(columns={'发货时间': '物流时间'}, inplace=True)
    合并数据.rename(columns={'发生时间': '实际结算时间'}, inplace=True)
    合并数据['商品总价(元)'] = 合并数据['商品总价(元)'].apply(lambda x: float(x))
    合并数据['成交数量'] = 合并数据['成交数量'].apply(lambda x:int(x))
    合并数据['商品单价'] = 合并数据['商品总价(元)']/合并数据['成交数量']
    合并数据['达人昵称'] = ''
    合并数据['出单机构'] = ''
    合并数据['达人ID'] = ''
    合并数据['平台'] = '拼多多'
    合并数据['店铺'] = ''

    合并数据['实际结算金额']=合并数据['实际结算金额'].fillna(0)
    订单全状态表 = 合并数据.loc[:, ['订单编号', '商品单号', '商家编码', '商品名称', '成交数量', '订单应付金额', '订单创建时间','订单状态', '售后状态', '售后申请时间', '实际结算时间', '实际结算金额', '预估推广佣金','物流时间', '回退状态', '统计时间', '达人昵称','出单机构','达人ID','商品单价','店铺','平台']]
    pd.DataFrame(订单全状态表).to_excel('全状态表.xlsx')
    print()

if __name__ == '__main__':
    订单全状态表('C:\\Users\\xwb\Desktop\\拼多多-MVAV鞋服工厂店(3)\\拼多多-MVAV鞋服工厂店\\2、清洗后');