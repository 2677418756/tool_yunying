import pandas as pd

data = pd.read_csv(r'E:\Operation_File\新建文件夹\星岛12月10日\抖音-YIWEINUO\1、源文件\抖音-订单表.csv',usecols=['主订单编号','子订单编号','选购商品','商品数量','订单应付金额','订单提交时间','订单状态','售后状态','商家编码','商品ID'])



data.loc[data['售后状态']=='退款成功',['售后状态']]='同意退款，退款成功'
data.loc[data['售后状态']=='退款中',['售后状态']]='同意退款，退款成功'
data.loc[data['售后状态']=='已全额退款',['售后状态']]='同意退款，退款成功'
data.loc[data['售后状态']=='待收退货',['售后状态']]='待商家收货'
data.loc[data['售后状态']=='售后待处理',['售后状态']]='待商家处理'
data.loc[data['售后状态']=='待退货',['售后状态']]='待买家退货处理'


data.to_excel(r'E:\Operation_File\新建文件夹\星岛12月10日\抖音-YIWEINUO\1、源文件\抖音-订单表G.xlsx')