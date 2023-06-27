# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 15:18:44 2022

@author: Admin
"""

import pandas as pd
import datetime
import timeit
from openpyxl import load_workbook, workbook

def str_to_date(str_):
    #【日期类型转换】让数据从str型转换成date型
    date_p = datetime.datetime.strptime(str_,'%Y-%m-%d').date()
    return date_p
def date_to_str(date_):
    #【日期类型转换】让数据从date型转换成str型
    return str(date_)

def timestamp_to_date(timestamp_):
    date = timestamp_.to_pydatetime().date()
    return date

def read():
    
    df = pd.read_excel(r'C:\Users\Admin\Desktop\0726成本表提取\FOLA旗舰店-抖音-订单表-HGM-无备注.xlsx')
    
    return df

def circle(Order):
    
     #防止表格读取后再写入相关字段乱码
    Order['订单编号'] = Order['订单编号'].astype(str)
    Order['商品单号'] = Order['商品单号'].astype(str)

    
    # 先精炼出订单创建日期
    Order['匹配标志'] = '失败'
    Order['成本价'] = round(Order['订单应付金额'] * 0.5,2)
    Order['订单创建日期'] = Order['订单创建日期'].map(timestamp_to_date)
    need_drop = Order.duplicated('订单创建日期') #返回与检测列相同长度的布尔类型Series，来反应某列中的重复值
    order_only = Order[~need_drop]
    orderDate = order_only['订单创建日期']

    orderDateList = orderDate.tolist()

    for date in orderDateList:
        """
        思路：第一个循环 —— 按订单创建日期切片
            第二个循环 —— 再按商家编码切片
        """
        #提取同一订单创建日期下的唯一商家编码  
        temp_order = Order[Order['订单创建日期'].isin([date])] #返回类型：dataframe
        temp_need_drop = temp_order.duplicated('商家编码') #返回类型：dataframe
        temp_order_only = temp_order[~temp_need_drop] #返回类型：dataframe
        orderBusinessCode = temp_order_only['商家编码'] #返回类型：series
        print(orderBusinessCode)
    


def base_func2():
    for n in range(10000):
        print('当前n的值是：{}'.format(n))
        
path = r'C:\Users\Admin\Desktop\0726成本表提取\FOLA旗舰店-抖音-订单表-HGM-无备注.xlsx'
# # read(path)
# res = timeit.timeit(stmt = 'read(path)',number=2)

# print('当前的函数的运行时间是：{}'.format(res))

# -*-coding:utf-8-*-
# AUTHOR:tyltr
# TIME :2018/10/11
 
 
# 待测试的函数
def add():
    # df = pd.read_excel(r'C:\Users\Admin\Desktop\0726成本表提取\FOLA旗舰店-抖音-订单表-HGM-无备注.xlsx')
    workbook = load_workbook(filename=r'C:\Users\Admin\Desktop\0726成本表提取\FOLA旗舰店-抖音-订单表-HGM-无备注.xlsx')
    sheet = workbook.active
    values = sheet.values
    df = pd.DataFrame(values)  
    # df = pd.read_excel(r'C:\Users\Admin\Desktop\0726成本表提取\FOLA旗舰店-抖音-订单表-HGM-无备注.xlsx')
    return df
 
 
# stmt 需要测试的函数或语句，字符串形式
# setup 运行的环境，本例子中表示 if __name__ == '__main__':
# number 被测试的函数或语句，执行的次数，本例表示执行100000次add()。省缺则默认是10000次
# repeat 测试做100次
# 综上：此函数表示 测试 在if __name__ == '__main__'的条件下，执行100000次add()消耗的时间，并把这个测试做100次,并求出平均值
 
t = timeit.repeat(stmt="add()", setup="from __main__ import add", number=1)
print(t)
print(sum(t) / len(t))






