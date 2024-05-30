import os
import pandas as pd
from PDDCleanTool.common.CommonUtil import CommonUtil
import numpy as np

def 订单金额成本表(path):
    所有文件名列表 = os.listdir(path)
    for 文件名 in 所有文件名列表:
        if '订单表' in 文件名:
            order_data = CommonUtil().读取表格(path,文件名);
        elif '账单表' in 文件名:
            bill_data = CommonUtil().读取表格(path,文件名);

    bill_data.rename(columns={'商户订单号': '订单号'}, inplace=True)
    bill_data.rename(columns={'收入金额（+元）': '收入金额'}, inplace=True)
    bill_data.rename(columns={'支出金额（-元）': '支出金额'}, inplace=True)
    # 筛选账单表中账务类型为技术服务费和其他服务
    bill_data = bill_data[bill_data.账务类型.isin(['技术服务费', '其他服务'])]
    #合并收入金额和支出金额
    bill_data['收入金额'] = bill_data['收入金额'].apply(lambda x: abs(float(x)))
    bill_data['支出金额'] = bill_data['支出金额'].apply(lambda x: abs(float(x)))
    bill_data['实际服务金额'] = bill_data['收入金额'] - bill_data['支出金额']
    #合并收支金额
    grouped_bill = bill_data.groupby('订单号')['实际服务金额'].sum().reset_index()

    #修改订单表时间
    order_data['订单成交时间'] = pd.to_datetime(order_data['订单成交时间'])
    order_data['订单成交时间'] = order_data['订单成交时间'].dt.date
    order_data['订单成交时间'] = order_data['订单成交时间'].astype(str)
    order_data['商家实收金额(元)'] = order_data['商家实收金额(元)'].apply(lambda x: abs(float(x)))
    # 合并表格
    order_bill_data = pd.merge(order_data, grouped_bill, how='left', on='订单号')

   #所有服务费计算，因为拼多多不管退货不退货都会进行技术服务费收取，并且不会退回，单独计算服务金额
    Service_order = pd.pivot_table(order_bill_data, index=['订单成交时间'], values=['实际服务金额'],aggfunc={'实际服务金额': np.sum})

    #筛选正常订单，即售后状态为'无售后或售后取消', '售后处理中'两种
    all_order=order_bill_data[order_bill_data.售后状态.isin(['无售后或售后取消', '售后处理中'])]
    end_order=pd.pivot_table(all_order,index=['订单成交时间'],values = ['商家实收金额(元)','订单号'],aggfunc={'商家实收金额(元)':np.sum,'订单号':len})

    # 修改正确的字段的名称
    end_order.rename(columns={'商家实收金额(元)': '剩余销售金额'}, inplace=True)

    # 增加算术运算得到的列
    end_order['运费'] = end_order['订单号'].map(lambda x: round(x * 6, 2))
    # 透析0['上游成本税'] = 透析0['成本价'].map(lambda x : x*0.08)
    end_order['平台扣点'] = end_order['剩余销售金额'].map(lambda x: round(x * 0.07, 2))
    end_order['资金成本'] = end_order['剩余销售金额'].map(lambda x: round(x * 0.02, 2))
    end_order.drop('订单号', axis=1, inplace=True)

    # 合并表格
    order_bill_data = pd.merge(end_order, Service_order, how='left', on='订单成交时间')


    pd.DataFrame(order_bill_data).to_csv('C:\\Users\\huanglipan\\Desktop\\order_bill_data.csv')
if __name__ == '__main__':
    订单金额成本表('C:\\Users\\huanglipan\\Desktop\\拼多多-MVAV鞋服工厂店\\拼多多-MVAV鞋服工厂店\\2、清洗后');