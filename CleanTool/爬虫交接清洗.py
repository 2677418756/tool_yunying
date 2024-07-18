import pandas as pd

import numpy as np


def 抖音处理模块(文件所在位置,文件类型,表格类型):

    判断表格名 = False

    if 表格类型 == '账单表' :
        if 文件类型 == '.xlsx':
            data = pd.read_excel(文件所在位置,usecols=['动账金额','动账时间','下单时间','动账摘要','子订单号','订单号','商品ID'])
        elif 文件类型 == '.csv':
            try:
                data = pd.read_csv(文件所在位置,usecols=['动账金额','动账时间','下单时间','动账摘要','子订单号','订单号','商品ID'])
            except(UnicodeDecodeError):
                data = pd.read_csv(文件所在位置,usecols=['动账金额','动账时间','下单时间','动账摘要','子订单号','订单号','商品ID'], encoding='GB18030')

            # 数据格式清洗转换
            data['商品ID'] = data['商品ID'].astype(str)
            data['商品ID'] = data['商品ID'].str.strip('\'')
            data['订单号'] = data['订单号'].astype(str)
            data['订单号'] = data['订单号'].str.strip('\'')
            data['子订单号'] = data['子订单号'].astype(str)
            data['子订单号'] = data['子订单号'].str.strip('\'')
            # 用完就扔
            data = data[data['动账摘要'].isin(['订单结算'])]
            data = data.drop(['动账摘要'],axis=1)

            # 重命名与数据库名保持一致
            data.rename(columns={'下单时间':'order_create_time'},inplace = True)
            data.rename(columns={'动账时间':'settlement_time'},inplace = True)
            data.rename(columns={'子订单号':'sub_order_no'},inplace = True)
            data.rename(columns={'订单号':'order_no'},inplace = True)
            data.rename(columns={'动账金额':'settlement_amount'},inplace = True)
            data.rename(columns={'商品ID':'item_id'},inplace = True)

    elif 表格类型 == '联盟表':
        if 文件类型 == '.xlsx':
            data = pd.read_excel(文件所在位置, usecols=['订单id', '预估佣金支出', '商品id'])
        elif 文件类型 == '.csv':
            try:
                data = pd.read_csv(文件所在位置, usecols=['订单id', '预估佣金支出', '商品id'])
            except(UnicodeDecodeError):
                data = pd.read_csv(文件所在位置, usecols=['订单id', '预估佣金支出', '商品id'], encoding='GB18030')
        # 防止订单id过长而导致数据失真
        data['订单id'] = data['订单id'].astype(str)
        data['商品id'] = data['商品id'].astype(str)
        # 数字格式转换
        data['预估佣金支出'] = data['预估佣金支出'].astype(float)
        print(111)
        # 数字保留两位小数
        data['预估佣金支出'] = np.round(data['预估佣金支出'], 2)

        # 统一字段名称
        data.rename(columns={'订单id': 'sub_order_no'}, inplace=True)
        data.rename(columns={'预估佣金支出': 'est_commission_amount'}, inplace=True)
        data.rename(columns={'商品id': 'item_id'}, inplace=True)

        判断表格名 = True

    elif 表格类型 == '团长表':
        if 文件类型 == '.xlsx':
            data = pd.read_excel(文件所在位置, usecols=['订单id', '预估服务费收入', '商品id'])
        elif 文件类型 == '.csv':
            try:
                data = pd.read_csv(文件所在位置, usecols=['订单id', '预估服务费收入', '商品id'])
            except(UnicodeDecodeError):
                data = pd.read_csv(文件所在位置, usecols=['订单id', '预估服务费收入', '商品id'], encoding='GB18030')

        # 防止订单id过长而导致数据失真
        data['订单id'] = data['订单id'].astype(str)
        data['商品id'] = data['商品id'].astype(str)
        # 数字格式转换
        data['预估服务费收入'] = data['预估服务费收入'].astype(float)
        # 数字保留两位小数
        data['预估服务费收入'] = np.round(data['预估服务费收入'], 2)
        # 统一字段名称
        data.rename(columns={'订单id': 'sub_order_no'}, inplace=True)
        data.rename(columns={'预估服务费收入': 'est_commission_amount'}, inplace=True)
        data.rename(columns={'商品id': 'item_id'}, inplace=True)

        判断表格名 = True

    return (data, 判断表格名)

def 快手处理模块(文件所在位置,文件类型,表格类型):

    判断表格名 = False

    if 表格类型 == '账单表':
        if 文件类型 == '.xlsx':
            data = pd.read_excel(文件所在位置, usecols=['订单号', '实际结算金额(元)', '实际结算时间', '订单创建时间','商品ID'])
        elif 文件类型 == '.csv':
            try:
                data = pd.read_csv(文件所在位置, usecols=['订单号', '实际结算金额(元)', '实际结算时间', '订单创建时间','商品ID'])
            except(UnicodeDecodeError):
                data = pd.read_csv(文件所在位置, usecols=['订单号', '实际结算金额(元)', '实际结算时间', '订单创建时间','商品ID'],
                                   encoding='GB18030')

        # 数据格式处理
        data['订单号'] = data['订单号'].astype(str)
        data['商品ID'] = data['商品ID'].astype(str)
        # 新增一列子订单号
        data['sub_order_no'] = data['订单号']
        # 重命名与数据库名保持一致
        data.rename(columns={'订单创建时间': 'order_create_time'}, inplace=True)
        data.rename(columns={'实际结算时间': 'settlement_time'}, inplace=True)
        data.rename(columns={'订单号': 'order_no'}, inplace=True)
        data.rename(columns={'实际结算金额(元)': 'settlement_amount'}, inplace=True)
        data.rename(columns={'商品ID': 'item_id'}, inplace=True)

    elif 表格类型 == '佣金表':
        if 文件类型 == '.xlsx':
            data = pd.read_excel(文件所在位置, usecols=['订单号', '预估推广佣金', '商品ID'])
        elif 文件类型 == '.csv':
            try:
                data = pd.read_csv(文件所在位置, usecols=['订单号', '预估推广佣金', '商品ID'])
            except(UnicodeDecodeError):
                data = pd.read_csv(文件所在位置, usecols=['订单号', '预估推广佣金', '商品ID'], encoding='GB18030')

        # 数据格式处理
        data['订单号'] = data['订单号'].astype(str)
        data['商品ID'] = data['商品ID'].astype(str)
        # 重命名与数据库名保持一致
        data.rename(columns={'订单号': 'sub_order_no'}, inplace=True)
        data.rename(columns={'预估推广佣金': 'est_commission_amount'}, inplace=True)
        data.rename(columns={'商品ID': 'item_id'}, inplace=True)


        判断表格名 = True

    return (data, 判断表格名)