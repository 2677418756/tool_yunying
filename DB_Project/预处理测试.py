# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 15:30:15 2022

@author: Admin
"""

import pandas as pd
import datetime as datetime
import numpy as np
import os

def 全合并快手订单(订单表,售后表,账单表,运单表):
    
    订单表['商品单号'] = 订单表['订单编号']

    运单表.rename(columns={'发货时间':'物流时间'},inplace = True)
    
    #售后表只接收同意
    售后表 = 售后表[售后表.售后状态.isin(['售后成功'])]
    
    data1 = pd.merge(订单表,售后表,how='left',on='订单编号')

    data2 = pd.merge(data1,账单表,how='left',on='订单编号')

    data3 = pd.merge(data2,运单表,how='left',on='订单编号')
    
    data3['实际结算金额(元)'].fillna(value=0,axis=0,inplace=True) 
    data3['预估推广佣金'].fillna(value=0,axis=0,inplace=True)
    data3['售后状态'].fillna(value='-',axis=0,inplace=True)
    
    data3['订单编号'] = data3['订单编号'].astype(str)
    data3['商品单号'] = data3['商品单号'].astype(str)
    
    
    return data3

def 快手全订单状态表(union,date):
    
    """
    预处理模块
        #宽泛的先来处理数据：先提取每一条记录的结算时间和售后时间，把为空的时间赋值，且设置对应临时标志
    """
    union['回退状态'] = '待回'
       
    union['实际结算时间'] = pd.to_datetime(union['实际结算时间'], errors='coerce')
    union['实际结算时间'] = np.where(union.实际结算时间.notnull(),union.实际结算时间.dt.strftime('%Y-%m-%d %H:%M:%S'),'2000-01-01 00:00:00')
    union['实际结算时间'] = union['实际结算时间'].astype('datetime64[ns]')
    
    union['售后申请时间'] = pd.to_datetime(union['售后申请时间'], errors='coerce')
    union['售后申请时间'] = np.where(union.售后申请时间.notnull(),union.售后申请时间.dt.strftime('%Y-%m-%d %H:%M:%S'),'2000-01-01 00:00:00')
    union['售后申请时间'] = union['售后申请时间'].astype('datetime64[ns]')
    
    union['物流时间'] = pd.to_datetime(union['物流时间'], errors='coerce')
    union['物流时间'] = np.where(union.物流时间.notnull(),union.物流时间.dt.strftime('%Y-%m-%d %H:%M:%S'),'2000-01-01 00:00:00')
    union['物流时间'] = union['物流时间'].astype('datetime64[ns]')
    
    
    # 默认时间 = '2000-01-01 00:00:00'
    # print(type(date))
    统计日期 = datetime.datetime.strptime(date,'%Y-%m-%d').date()
    
    #
    有售后 = union[~(union['售后申请时间'].isin(['2000-01-01 00:00:00']))]
    无售后 = union[union['售后申请时间'].isin(['2000-01-01 00:00:00'])]
    已退 = 有售后[有售后['实际结算时间'].isin(['2000-01-01 00:00:00'])]
    回退 = 有售后[~(有售后['实际结算时间'].isin(['2000-01-01 00:00:00']))]
    已回 = 无售后[~(无售后['实际结算时间'].isin(['2000-01-01 00:00:00']))]
    待回 = 无售后[无售后['实际结算时间'].isin(['2000-01-01 00:00:00'])]
    
    
    回退['实际结算金额(元)'] = 回退['实际结算金额(元)'].map(lambda x : -x)
    
    回退['回退状态'] = '回退'
    已退['回退状态'] = '已退'
    已回['回退状态'] = '已回'
    
    frame = pd.DataFrame()
    frame1 = pd.concat([待回,已回])
    #对无售后的，有物流时间，单独提取出来再添加统计时间
    揽收可授信统计 = frame1[frame1['物流时间'].dt.date == 统计日期]
    #将昨日揽收的数据提取出来
    揽收可授信统计['统计时间'] = datetime.datetime.now()
    
    
    frame = pd.concat([frame1,已退])
    frame = pd.concat([frame,回退])

    frame.rename(columns={'实际结算金额(元)': '实际结算金额'}, inplace=True)
    揽收可授信统计.rename(columns={'实际结算金额(元)': '实际结算金额'}, inplace=True)
    frame['统计时间'] = datetime.datetime.now()
    frame.reset_index(inplace=True,drop=True)
   
    return frame,揽收可授信统计    

com = r'E:\Operation_File\火光店铺系列\1、历史过程数据\TB鞋服品牌\10.24\快手-TB品牌鞋服\2、清洗后'

订单表 = pd.read_excel(com + r'\\TB品牌鞋服-快手-订单表-HGM-无备注.xlsx')
售后表 = pd.read_excel(com + r'\\TB品牌鞋服-快手-售后表-HGM-无备注.xlsx')
账单表 = pd.read_excel(com + r'\\TB品牌鞋服-快手-账单表-HGM-无备注.xlsx')
运单表 = pd.read_excel(com + r'\\TB品牌鞋服-快手-运单表-HGM-无备注.xlsx')


data = 全合并快手订单(订单表,售后表,账单表,运单表)

data.to_excel(com + r'\\TB品牌鞋服无备注.xlsx')

