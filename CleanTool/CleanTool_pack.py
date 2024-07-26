# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 18:00:54 2022

@author: Admin
"""

import pandas as pd
import os
import os.path
import re
import numpy as np
import datetime
import gc
from PDDCleanTool import 拼多多理模块


def 抖音处理模块(文件所在位置,文件类型,表格类型):
     
    def 提取最长字符串(strings):

        try:
            #匹配2-10位字母与数字组成的子串，返回一个数组（列表）
            ret = re.findall("[a-zA-Z0-9]{2,10}",strings)
        except(TypeError):
            #因为有可能商家编码为空值
            return 'Empty'
        
        if ret:                  
            return max(ret,key=len) #返回列表中长度最大的值
        else:
            return 'Not exis code'
    #设置初始值
    判断表格名 = False
    
    if 表格类型 == '订单表' :
        #判断文件类型，防止平台后期修改文件的保存格式
        if 文件类型 == '.xlsx' :
            data = pd.read_excel(文件所在位置,usecols=['主订单编号','子订单编号','选购商品','商品数量','订单应付金额','订单提交时间','订单状态','售后状态','商家编码','商品ID','达人昵称','达人ID','商品单价'])
        elif 文件类型 == '.csv' :
            try:
                data = pd.read_csv(文件所在位置,usecols=['主订单编号','子订单编号','选购商品','商品数量','订单应付金额','订单提交时间','订单状态','售后状态','商家编码','商品ID','达人昵称','达人ID','商品单价'])
            except(UnicodeDecodeError):
                data = pd.read_csv(文件所在位置,usecols=['主订单编号','子订单编号','选购商品','商品数量','订单应付金额','订单提交时间','订单状态','售后状态','商家编码','商品ID','达人昵称','达人ID','商品单价'],encoding='GB18030')

                
        #筛选去除不重要的数据
        data = data[~(data.订单状态.isin(['已关闭'])&data.售后状态.isin(['-']))]
        #将外部字段编号变为内部同一字段编号【蠢办法先】
        data.loc[data['售后状态'] == '退款成功', ['售后状态']] = '同意退款，退款成功'
        data.loc[data['售后状态'] == '退款中', ['售后状态']] = '同意退款，退款成功'
        data.loc[data['售后状态'] == '已全额退款', ['售后状态']] = '同意退款，退款成功'
        data.loc[data['售后状态'] == '待收退货', ['售后状态']] = '待商家收货'
        data.loc[data['售后状态'] == '售后待处理', ['售后状态']] = '待商家处理'
        data.loc[data['售后状态'] == '待退货', ['售后状态']] = '待买家退货处理'

        #提取字符串
        # data['商家编码'] = data['商家编码'].map(提取最长字符串)
        #数据的某一列=数据的某一列进行格式转换，来达成清除前后空格
        data['订单提交时间'] = data['订单提交时间'].astype('datetime64[ns]')
        #超过4位数会有逗号，需要统一转换为str使用replace去除
        data['订单应付金额'] = data['订单应付金额'].astype(str)
        data['订单应付金额'] = data['订单应付金额'].str.replace(',','')
        data['订单应付金额'] = data['订单应付金额'].astype(float)
        data['主订单编号'] = data['主订单编号'].astype(str)
        data['子订单编号'] = data['子订单编号'].astype(str)
        data['商品ID'] = data['商品ID'].astype(str)
        data['达人ID'] =data['达人ID'].astype(str)
        data['订单提交日期'] = pd.to_datetime(data['订单提交时间'])
        data['订单提交日期'] = data['订单提交日期'].dt.date
        
        #【智能去重功能，根据子订单编号去重，且只能放在筛选之后】
        data = data.drop_duplicates('子订单编号')
        
        #统一字段的名称
        data.rename(columns={'选购商品':'商品名称'},inplace = True)
        data.rename(columns={'主订单编号':'订单编号'},inplace = True)
        data.rename(columns={'子订单编号':'商品单号'},inplace = True)
        data.rename(columns={'订单提交时间':'订单创建时间'},inplace = True)
        data.rename(columns={'订单提交日期':'订单创建日期'},inplace = True)
        data.rename(columns={'商品数量':'成交数量'},inplace = True)        
        判断表格名 = True
        
    elif 表格类型 == '运单表' :
        #判断文件类型，防止平台后期修改文件的保存格式
        if 文件类型 == '.xlsx' :
            data = pd.read_excel(文件所在位置,usecols=['运单号','订单编号','揽件时间','发货时间'],dtype=str)
        elif 文件类型 == '.csv' :
            try:
                data = pd.read_csv(文件所在位置,usecols=['运单号','订单编号','揽件时间','发货时间'],dtype=str)
            except(UnicodeDecodeError):
                data = pd.read_csv(文件所在位置,usecols=['运单号','订单编号','揽件时间','发货时间'],encoding='GB18030',dtype=str)
         
        #——————————————————————————————————先删除真重复的运单表，再向下分列，再删除重复订单号
        #【重要】已证实，运单号重复是因为异常类型不一致！
        data = data.drop_duplicates('运单号')
        #将运单表中一个单元格内的多个订单编号向下分列
        data['运单号'] = data['运单号'].astype(str)
        data['订单编号'] = data['订单编号'].astype(str)
        data_ = data['订单编号'].str.split(',', expand=True)
        data_ = data_.stack()
        data_ = data_.reset_index(level=1,drop=True).rename('订单编号')
        data = data.drop(['订单编号'],axis=1).join(data_)
        # data = data.drop('订单号',axis=1).join(data_)

        #清除掉重复值【已核实1.0】
        data = data.drop_duplicates('订单编号')
        #——————————————————————————————————先删除真重复的运单表，再向下分列，再删除重复订单号
        
        #【重要】将该死的\t符号干掉，但依然不能去除空值
        #print(repr(data.loc[0,'订单号']))
        data['订单编号'] = data['订单编号'].str.strip('\t')
        #print(repr(data.loc[0,'订单号']))
        
        #————————————————————————————————————————临时处理方法
        data['空值处理'] = data['订单编号']
        data['空值处理'] = data['空值处理'].astype(bool)
        data = data.drop(data[data['空值处理'] == False].index)
        #————————————————————————————————————————临时处理方法
        #【清除左右字符串，默认为空格】匹配第一个和最后一个字符，分别看左边和有边有无指定字符，有则清除
        data['订单编号'].str.strip()
        
        #【去空】去掉揽件时间、订单号中的空值所在行
        data.dropna(axis = 0 ,how = 'any',inplace=True)
        data['订单编号'] = data['订单编号'].astype(str)
        data.drop(['空值处理'],axis= 1,inplace=True)
        
        data['发货日期'] = pd.to_datetime(data['发货时间'])
        data['发货日期'] = data['发货日期'].dt.date
        data['揽件日期'] = pd.to_datetime(data['揽件时间'])
        data['揽件日期'] = data['揽件日期'].dt.date
        #统一字段名称
        data.rename(columns={'订单编号':'订单编号'},inplace = True)
        判断表格名 = True


        
    elif 表格类型 == '售后表' :
        #判断文件类型，防止平台后期修改文件的保存格式
        if 文件类型 == '.xlsx' :
            data = pd.read_excel(文件所在位置,usecols=['订单号','商品单号','售后状态','售后类型','退商品金额（元）','售后申请时间','退款方式','商品ID'])
        elif 文件类型 == '.csv' :
            data = pd.read_csv(文件所在位置,usecols=['订单号','商品单号','售后状态','售后类型','退商品金额（元）','售后申请时间','退款方式','商品ID'])

        #将外部字段编号变为内部同一字段编号【蠢办法先】
        data.loc[data['售后状态'] == '待买家退货', ['售后状态']] = '待买家退货处理'


        #【筛选】
        data = data[~(data.售后状态.isin(['售后关闭'])|data.退款方式.isin(['无需退款']))]
        data = data[(data.售后状态.isin(['待买家退货'])|data.售后状态.isin(['待商家处理'])|data.售后状态.isin(['待商家收货'])|data.售后状态.isin(['同意退款，退款成功']))]
        #格式转换
        data['售后申请日期'] = pd.to_datetime(data['售后申请时间'])
        data['售后申请日期'] = data['售后申请日期'].dt.date
        data['订单号'] = data['订单号'].astype(str)
        data['商品单号'] = data['商品单号'].astype(str)
        data['商品ID'] = data['商品ID'].astype(str)
        # #【智能去重功能，根据商品单号去重，且只能放在筛选之后】
        # data = data.drop_duplicates('商品单号')
        
        #统一字段名称
        data.rename(columns={'订单号':'订单编号'},inplace = True)
        data.rename(columns={'退商品金额（元）':'实退款金额'},inplace = True)
        判断表格名 = True
        
    # elif 表格类型 == '成本表' :
    #     #判断文件类型，防止平台后期修改文件的保存格式
    #     if 文件类型 == '.xlsx' :
    #         data = pd.read_excel(文件所在位置)
    #     elif 文件类型 == '.csv' :
    #         data = pd.read_csv(文件所在位置)
            
    #     判断表格名 = True
        

    elif 表格类型 == '结算表' :
        if 文件类型 == '.xlsx' :
            data = pd.read_excel(文件所在位置,usecols=['结算金额','结算时间','下单时间','子订单号','订单号'])
        elif 文件类型 == '.csv' :
            try:       
                data = pd.read_csv(文件所在位置,usecols=['结算金额','结算时间','下单时间','子订单号','订单号'],dtype={"结算金额": str})
            except(UnicodeDecodeError):
                data = pd.read_csv(文件所在位置,usecols=['结算金额','结算时间','下单时间','子订单号','订单号'],dtype={"结算金额": str},encoding='GB18030')
                
        #先删除非表头的那一列
        data.drop([0],axis=0,inplace=True)
        data.reset_index(inplace=True,drop=True)
        
        #将时间戳转换为datetime格式,dt.date单位为天,str方便用户看
        data['下单日期'] = pd.to_datetime(data['下单时间'])
        data['下单日期'] = data['下单日期'].dt.date
        data['下单日期'] = data['下单日期'].astype(str)
        data['结算日期'] = pd.to_datetime(data['结算时间'])
        data['结算日期'] = data['结算日期'].dt.date
        data['结算日期'] = data['结算日期'].astype(str)
        data['结算金额'] = data['结算金额'].astype(float)
        # data = data[(data['结算金额'] >= 0)]
        #数据清理掉无用数据
        data.dropna(axis = 0 ,how = 'any',inplace=True)
        
        #统一字段名称
        data.rename(columns={'下单时间':'订单创建时间'},inplace = True)
        data.rename(columns={'下单日期':'订单创建日期'},inplace = True)
        data.rename(columns={'结算时间':'实际结算时间'},inplace = True)
        data.rename(columns={'结算日期':'实际结算日期'},inplace = True)
        data.rename(columns={'子订单号':'商品单号'},inplace = True)
        data.rename(columns={'订单号':'订单编号'},inplace = True)
        data.rename(columns={'结算金额':'实际结算金额(元)'},inplace = True) 

        判断表格名 = True
  
    elif 表格类型 == '账单表' :
        if 文件类型 == '.xlsx' :
            data = pd.read_excel(文件所在位置,usecols=['动帐流水号','动账金额','动账时间','下单时间','动账方向','备注','子订单号','订单号','商品ID', '运费实付', '订单退款'])
        elif 文件类型 == '.csv' :
            try:       
                data = pd.read_csv(文件所在位置,usecols=['动帐流水号','动账金额','动账时间','下单时间','动账方向','备注','子订单号','订单号','商品ID', '运费实付', '订单退款'])
            except(UnicodeDecodeError):
                data = pd.read_csv(文件所在位置,usecols=['动帐流水号','动账金额','动账时间','下单时间','动账方向','备注','子订单号','订单号','商品ID','运费实付', '订单退款'],encoding='GB18030')
        
        """
        账单表整理分享： 退回给用户的形式在账单表中有两种——
        第一种（已结算型）：订单结算+74%，服务费返还+26%，已退款or原路退-100%。
        第二种（未结算型）：极速退款分账+100%，已退款or原路退-100%。
        """

        data.rename(columns={'备注':'动账摘要'},inplace = True)
        #将时间戳转换为datetime格式,dt.date单位为天,str方便用户看
        data['下单日期'] = pd.to_datetime(data['下单时间'])
        data['下单日期'] = data['下单日期'].dt.date
        data['下单日期'] = data['下单日期'].fillna("")
        data['下单日期'] = data['下单日期'].astype(str)
        data['动账日期'] = pd.to_datetime(data['动账时间'])
        data['动账日期'] = data['动账日期'].dt.date
        data['动账日期'] = data['动账日期'].astype(str)

        data['商品ID'] = data['商品ID'].fillna("")
        data['商品ID'] = data['商品ID'].astype(str)
        data['商品ID'] = data['商品ID'].str.strip('\'')
        data['订单号'] = data['订单号'].astype(str)
        data['订单号'] = data['订单号'].str.strip('\'')
        data = data[~data.子订单号.isna()]
        # data = data[(data.动账方向.isin(['入账']))]
         
        # #入账中只需要订单结算，服务费返还,极速退款分账
        # #出账中的状态只保留原路退和已退款
        # data = data[data['动账摘要'].isin(['极速退款分账'])|data['动账摘要'].isin(['订单结算'])|data['动账摘要'].isin(['原路退'])|data['动账摘要'].isin(['已退款'])|data['动账摘要'].isin(['服务费返还'])]


        #处理动账金额
        # data['收支金额'] = 0
        data_in = data[data['动账方向'].isin(['入账'])]
        data_out = data[data['动账方向'].isin(['出账'])]
        
        data_in['收支金额'] = data_in['动账金额']
        data_out['收支金额'] = - data_out['动账金额']
        data = pd.concat([data_in,data_out])
        
        data.reset_index(inplace=True,drop=True)
        # #数据清理掉无用数据
        # data.dropna(axis = 0 ,how = 'any',inplace=True)
        #【智能去重功能，根据动账流水号去重，且只能放在筛选之后】
        data = data.drop_duplicates('动帐流水号')
        data = data.loc[:,['动帐流水号','订单号','子订单号','下单日期','动账日期','动账摘要','收支金额','下单时间','动账时间','商品ID','动账方向','运费实付','订单退款']]
        #统一字段名称
        data.rename(columns={'下单时间':'订单创建时间'},inplace = True)
        data.rename(columns={'下单日期':'订单创建日期'},inplace = True)
        data.rename(columns={'动账时间':'实际结算时间'},inplace = True)
        data.rename(columns={'动账日期':'实际结算日期'},inplace = True)
        data.rename(columns={'子订单号':'商品单号'},inplace = True)
        data.rename(columns={'订单号':'订单编号'},inplace = True)
        data.rename(columns={'收支金额':'实际结算金额(元)'},inplace = True)
        data["商品单号"] = data["商品单号"].apply(lambda x:str(x).replace("'",""))
        判断表格名 = True
        
    elif 表格类型 == '联盟表':
        if 文件类型 == '.xlsx':
            data = pd.read_excel(文件所在位置,usecols=['订单id','预估佣金支出','商品id'])
        elif 文件类型 == '.csv':
            try:       
                data = pd.read_csv(文件所在位置,usecols=['订单id','预估佣金支出','商品id'])
            except(UnicodeDecodeError):
                data = pd.read_csv(文件所在位置,usecols=['订单id','预估佣金支出','商品id'],encoding='GB18030')
        #防止订单id过长而导致数据失真      
        data['订单id'] = data['订单id'].astype(str)
        data['商品id'] = data['商品id'].astype(str)
        #数字格式转换
        data['预估佣金支出'] = data['预估佣金支出'].astype(float)
        #数字保留一位小数
        data['预估佣金支出'] = np.round(data['预估佣金支出'],1)   
        
        #统一字段名称
        data.rename(columns={'订单id':'商品单号'},inplace = True)
        data.rename(columns={'预估佣金支出':'联盟佣金'},inplace = True)
            
        判断表格名 = True
 
            
    elif 表格类型 == '团长表' :
        if 文件类型 == '.xlsx' :
            data = pd.read_excel(文件所在位置,usecols=['订单id','预估服务费收入','商品id','出单机构'])
        elif 文件类型 == '.csv' :
            try:       
                data = pd.read_csv(文件所在位置,usecols=['订单id','预估服务费收入','商品id','出单机构'])
            except(UnicodeDecodeError):
                data = pd.read_csv(文件所在位置,usecols=['订单id','预估服务费收入','商品id','出单机构'],encoding='GB18030')
                
        #防止订单id过长而导致数据失真
        data['订单id'] = data['订单id'].astype(str)
        data['商品id'] = data['商品id'].astype(str)
        #数字格式转换
        data['预估服务费收入'] = data['预估服务费收入'].astype(float)
        #数字保留一位小数
        data['预估服务费收入'] = np.round(data['预估服务费收入'],1)
        #统一字段名称
        data.rename(columns={'订单id':'商品单号'},inplace = True)
        data.rename(columns={'预估服务费收入':'团长佣金'},inplace = True)
        
        判断表格名 = True

    return (data,判断表格名)

#———————————————————————————————————————————————————————————————上抖音，下快手————————————————————————————————————————————————————————————————    
def 快手处理模块(文件所在位置,文件类型,表格类型):
    
    判断表格名 = False
    def timeformat(timestamp):
        
        change = datetime.datetime.strptime(str(timestamp),'%Y/%m/%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        
        return change
     
    if 表格类型 == '订单表' :
        #读取文件
        #判断文件类型，防止平台后期修改文件的保存格式
        if 文件类型 == '.xlsx' :
            try:
                data = pd.read_excel(文件所在位置,usecols=['订单号','订单创建时间','订单状态','实付款','预估推广佣金','商品名称','商品ID','成交数量','售后状态','SKU编码','CPS达人ID','CPS达人昵称','商品单价','团长ID','发货时间','快递单号','快递公司'])
                data['预估推广佣金'] = data['预估推广佣金'].astype(str)
                data['预估推广佣金'] = data['预估推广佣金'].astype('float')
                # data.rename(columns={'预估推广佣金':'订单佣金'},inplace = True)
            except(ValueError):
                data = pd.read_excel(文件所在位置,usecols=['订单号','订单创建时间','订单状态','实付款','商品名称','商品ID','成交数量','售后状态','SKU编码','CPS达人ID','CPS达人昵称','商品单价','团长ID','发货时间','快递单号','快递公司'])
                
        elif 文件类型 == '.csv' :          
            try:       
                try:
                    data = pd.read_csv(文件所在位置,usecols=['订单号','订单创建时间','订单状态','实付款','预估推广佣金','商品名称','商品ID','成交数量','售后状态','SKU编码','CPS达人ID','CPS达人昵称','商品单价','团长ID','发货时间','快递单号','快递公司'])
                    data['预估推广佣金'] = data['预估推广佣金'].astype(str)
                    data['预估推广佣金'] = data['预估推广佣金'].astype('float')
                    # data.rename(columns={'预估推广佣金':'订单佣金'},inplace = True)
                except(ValueError):
                    data = pd.read_csv(文件所在位置,usecols=['订单号','订单创建时间','订单状态','实付款','商品名称','商品ID','成交数量','售后状态','SKU编码','CPS达人ID','CPS达人昵称','商品单价','团长ID','发货时间','快递单号','快递公司'])
                    
            except(UnicodeDecodeError):
                try:
                    data = pd.read_csv(文件所在位置,usecols=['订单号','订单创建时间','订单状态','实付款','预估推广佣金','商品名称','商品ID','成交数量','售后状态','SKU编码','CPS达人ID','CPS达人昵称','商品单价','团长ID','发货时间','快递单号','快递公司'],encoding='GB18030')
                    data['预估推广佣金'] = data['预估推广佣金'].astype(str)
                    data['预估推广佣金'] = data['预估推广佣金'].astype('float')
                    # data.rename(columns={'预估推广佣金':'订单佣金'},inplace = True)
                except(ValueError):
                    data = pd.read_csv(文件所在位置,usecols=['订单号','订单创建时间','订单状态','实付款','商品名称','商品ID','成交数量','售后状态','SKU编码','CPS达人ID','CPS达人昵称','商品单价','团长ID','发货时间','快递单号','快递公司'],encoding='GB18030')

        data.rename(columns={'售后状态':'退货退款'},inplace = True)
        #删除无用记录，交易关闭且退货退款为空的订单是未支付订单
        data = data[~(data.订单状态.isin(['交易关闭'])&data.退货退款.isnull())]
        data = data[data['订单状态'] != '待付款']
        #去除符号转换为可以计算的数字格式
        data['实付款'] = data['实付款'].astype(str)
        data['实付款'] = data['实付款'].str.replace('¥','')                       
        data['实付款'] = data['实付款'].astype('float')

        #避免订单号位数过长丢失数据
        data['订单号'] = data['订单号'].astype(str)
        data['商品ID'] = data['商品ID'].astype(str)
        #时间格式转换模块：从时间戳转换成时间组件
        data['订单创建日期'] = pd.to_datetime(data['订单创建时间'])
        data['订单创建日期'] = data['订单创建日期'].dt.date
        data['订单创建日期'] = data['订单创建日期'].astype(str)

        data['CPS达人ID'] = data['CPS达人ID'].astype('Int64')
        data['CPS达人ID'].fillna(value=0, axis=0, inplace=True)
        data['CPS达人ID'] = data['CPS达人ID'].astype(str)
        data['CPS达人ID'] = data['CPS达人ID'].replace('0', '')



        #统一字段的名称
        data.rename(columns={'订单号':'订单编号'},inplace = True)
        # data.rename(columns={'退货退款':'售后状态'},inplace = True)
        data.rename(columns={'实付款':'订单应付金额'},inplace = True)
        data.rename(columns={'SKU编码':'商家编码'}, inplace=True)
        # 判断表格名 = True


        data['发货日期'] = pd.to_datetime(data['发货时间'])
        data['发货日期'] = data['发货日期'].dt.date
        # 避免订单号位数过长丢失数据
        data['快递单号'] = data['快递单号'].astype(str)

        data = data.sort_values(by='发货时间', ascending=True)

        # 统一字段的名称
        # data.rename(columns={'订单号': '订单编号'}, inplace=True)
        data.rename(columns={'快递单号': '运单号'}, inplace=True)
        判断表格名 = True
        
    elif 表格类型 == '运单表' :
        #读取文件
        #判断文件类型，防止平台后期修改文件的保存格式
        def 删除无用尾缀(string):
            lit = string.split('.')
            return lit[0]
        
        try:
            if 文件类型 == '.xlsx' :
                data = pd.read_excel(文件所在位置,usecols=['发货/揽收/末条中转/派件/待取件/签收时间','订单编号','物流单号'])
            elif 文件类型 == '.xls' :
                data = pd.read_excel(文件所在位置,usecols=['发货/揽收/末条中转/派件/待取件/签收时间','订单编号','物流单号'])
            elif 文件类型 == '.csv' :
                data = pd.read_csv(文件所在位置,usecols=['发货/揽收/末条中转/派件/待取件/签收时间','订单编号','物流单号'])
            data['物流单号'] = data['物流单号'].astype(str)       
            #统一字段的名称
            data.rename(columns={'物流单号':'运单号'},inplace = True)
            data.rename(columns={'发货/揽收/末条中转/派件/待取件/签收时间':'发货时间'},inplace = True) #下载内容的本质是揽收就是揽收
            
        except:
            if 文件类型 == '.xlsx' :
                data = pd.read_excel(文件所在位置,usecols=['发货时间','订单编号','快递单号'])
            elif 文件类型 == '.csv' :
                data = pd.read_csv(文件所在位置,usecols=['发货时间','订单编号','快递单号'])
            data['快递单号'] = data['快递单号'].astype(str)
            #统一字段的名称
            data.rename(columns={'快递单号':'运单号'},inplace = True)

        #避免订单号位数过长丢失数据
        data.dropna(axis = 0 ,subset=['订单编号'],how = 'any',inplace=True)
        data.dropna(axis = 0 ,subset=['发货时间'],how = 'any',inplace=True)
        data['订单编号'] = data['订单编号'].astype(np.int64)
        data['订单编号'] = data['订单编号'].astype(str)
        data['订单编号'] = data['订单编号'].map(删除无用尾缀)
        
        try:
            data['发货时间'] = data['发货时间'].map(timeformat)
        except:
            pass
        data['发货日期'] = pd.to_datetime(data['发货时间'])
        data['发货日期'] = data['发货日期'].dt.date
       

        判断表格名 = True

    # elif 表格类型 == '仓运单表' :
    #     #读取文件
    #     #判断文件类型，防止平台后期修改文件的保存格式
    #     if 文件类型 == '.xlsx' :
    #         data = pd.read_excel(文件所在位置,usecols=['发货时间','订单号','快递单号','仓库名称','快递公司'])
    #     elif 文件类型 == '.csv' :
    #         data = pd.read_csv(文件所在位置,usecols=['发货时间','订单号','快递单号','仓库名称','快递公司'])
    #
    #     #避免订单号位数过长丢失数据
    #     data['发货时间'] = data['发货时间'].map(timeformat)
    #     data['发货日期'] = pd.to_datetime(data['发货时间'])
    #     data['发货日期'] = data['发货日期'].dt.date
    #     data['订单号'] = data['订单号'].astype(str)
    #     data['快递单号'] = data['快递单号'].astype(str)
    #
    #     data = data.sort_values(by='发货时间', ascending=True)
    #     data = data.drop_duplicates(subset=['订单号'],keep='first')
    #
    #     #统一字段的名称
    #     data.rename(columns={'订单号':'订单编号'},inplace = True)
    #     data.rename(columns={'快递单号':'运单号'},inplace = True)
    #     判断表格名 = True

    elif 表格类型 == '售后表' :
        #读取文件
        #判断文件类型，防止平台后期修改文件的保存格式
        if 文件类型 == '.xlsx' :
            try:
                data = pd.read_excel(文件所在位置,usecols=['订单编号','售后状态','售后类型','售后申请时间','退款金额'])
                data['售后申请日期'] = pd.to_datetime(data['售后申请时间'])
                data['售后申请日期'] = data['售后申请日期'].dt.date
            except(ValueError):
                data = pd.read_excel(文件所在位置,usecols=['订单编号','售后状态','售后类型','申请时间','退款金额'])
                data.rename(columns={'申请时间':'售后申请时间'},inplace = True)
                data['售后申请日期'] = pd.to_datetime(data['售后申请时间'])
                data['售后申请日期'] = data['售后申请日期'].dt.date
        elif 文件类型 == '.csv' :
            try:
                data = pd.read_csv(文件所在位置,usecols=['订单编号','售后状态','售后类型','售后申请时间','退款金额'])
                data['售后申请日期'] = pd.to_datetime(data['售后申请时间'])
                data['售后申请日期'] = data['售后申请日期'].dt.date
            except(ValueError):
                data = pd.read_csv(文件所在位置,usecols=['订单编号','售后状态','售后类型','申请时间','退款金额'])
                data.rename(columns={'申请时间':'售后申请时间'},inplace = True)
                data['售后申请日期'] = pd.to_datetime(data['售后申请时间'])
                data['售后申请日期'] = data['售后申请日期'].dt.date
        #删除无用记录，只留下退款成功
        data = data[~(data.售后状态.isin(['售后失败','售后关闭']))]

        #【待更新算法】 可以把去掉售后关闭后的，依然还重复的订单号，金额上求和，申请日期保留最早那个
        data = data.sort_values(by='退款金额', ascending=False)
        data = data.drop_duplicates(subset=['订单编号'],keep='first')


        #去除符号转换为可以计算的数字格式
        data['退款金额'] = data['退款金额'].astype(str)
        data['退款金额'] = data['退款金额'].str.replace('¥','')
        data['退款金额'] = data['退款金额'].astype('float')  
        #格式转换

        # #时间格式转换模块：从时间戳转换成时间组件
        # data['订单创建日期'] = pd.to_datetime(data['订单创建时间'])
        # data['订单创建日期'] = data['订单创建日期'].dt.date
        # data['订单创建日期'] = data['订单创建日期'].astype(str)   
        # #将退款金额改名，防止后面冲突
        # data.rename(columns = {'退款金额':'应退款金额'},inplace = True)
        #一定要将多位数的订单编号转成字符串
        data['订单编号'] = data['订单编号'].astype(str)
        #data['申请时间'] = data['申请时间'].astype(str)
        
        #统一字段名称
        data.rename(columns={'退款金额':'实退款金额'},inplace = True)


        判断表格名 = True
        
    elif 表格类型 == '账单表':
        if 文件类型 == '.xlsx' :
            data = pd.read_excel(文件所在位置,usecols=['订单号','实际结算时间','订单创建时间',"合计收入(元)","合计支出(元)"])
        elif 文件类型 == '.csv' :            
            try:       
                data = pd.read_csv(文件所在位置,usecols=['订单号','实际结算时间','订单创建时间',"合计收入(元)","合计支出(元)"])
            except(UnicodeDecodeError):
                data = pd.read_csv(文件所在位置,usecols=['订单号','实际结算时间','订单创建时间',"合计收入(元)","合计支出(元)"],encoding='GB18030')
                
        #将时间戳转换为datetime格式,dt.date单位为天,str方便用户看
        data['订单创建日期'] = pd.to_datetime(data['订单创建时间'])
        data['订单创建日期'] = data['订单创建日期'].dt.date
        data['订单创建日期'] = data['订单创建日期'].astype(str)
        data['实际结算日期'] = pd.to_datetime(data['实际结算时间'])
        data['实际结算日期'] = data['实际结算日期'].dt.date
        data['实际结算日期'] = data['实际结算日期'].astype(str)

        data['合计收入(元)'] = data['合计收入(元)'].astype(float)
        data['合计支出(元)'] = data['合计支出(元)'].astype(float)
        data['实际结算金额(元)'] = data['合计收入(元)'] - data['合计支出(元)']
        
        data['订单号'] = data['订单号'].astype(str)  
        #统一字段的名称
        data.rename(columns={'订单号':'订单编号'},inplace = True)
        判断表格名 = True
        
    else :
        print('文件命名错误(订单表，运单表，售后表)')
        
        
    return (data,判断表格名)

#———————————————————————————————————————————————————————————————上快手，下拼多多———————————————————————————————————————————————————————————————— 

# def 拼多多处理模块(文件所在位置,文件类型,表格类型):
#     判断表格名 = False
#     if 表格类型 == '订单表' :
#         #判断文件类型，防止平台后期修改文件的保存格式
#         if 文件类型 == '.xlsx' :
#             data = pd.read_excel(文件所在位置,usecols=['订单号','样式ID','商品数量(件)','商家实收金额(元)','订单成交时间','订单状态','售后状态'])
#         elif 文件类型 == '.csv' :
#             data = pd.read_csv(文件所在位置,usecols=['订单号','样式ID','商品数量(件)','商家实收金额(元)','订单成交时间','订单状态','售后状态'])
#         #筛选去除不重要的数据
#         data = data[~(data.订单状态.isin(['待支付'])|data.订单状态.isin(['已取消'])|data.订单状态.isin(['已取消，退款成功']))]
#
#         #数据的某一列=数据的某一列进行格式转换，来达成清除前后空格
#         data['订单成交时间'] = data['订单成交时间'].astype('datetime64[ns]')
#         #超过4位数会有逗号，需要统一转换为str使用replace去除
#         data['商家实收金额(元)'] = data['商家实收金额(元)'].astype(str)
#         data['商家实收金额(元)'] = data['商家实收金额(元)'].str.replace(',','')
#
#         data['商家实收金额(元)'] = data['商家实收金额(元)'].astype(float)
#         data['样式ID'] = data['样式ID'].astype(str)
#         data['订单号'] = data['订单号'].astype(str)
#         data['订单成交日期'] = pd.to_datetime(data['订单成交时间'])
#         data['订单成交日期'] = data['订单成交日期'].dt.date
#
#         # #统一字段的名称
#         data.rename(columns={'订单号':'订单编号'},inplace = True)
#         data.rename(columns={'订单成交时间':'订单创建时间'},inplace = True)
#         data.rename(columns={'订单成交日期':'订单创建日期'},inplace = True)
#         data.rename(columns={'商品数量(件)':'成交数量'},inplace = True)
#         data.rename(columns={'商家实收金额(元)':'订单应付金额'},inplace = True)
#         data.rename(columns={'样式ID':'商品名称'},inplace = True)
#         判断表格名 = True
#
#     elif 表格类型 == '运单表' :
#         #判断文件类型，防止平台后期修改文件的保存格式
#         #一共需要里面的【发货时间、订单号、运单号、包裹状态】
#         if 文件类型 == '.xlsx' :
#             data = pd.read_excel(文件所在位置)
#         elif 文件类型 == '.csv' :
#             data = pd.read_csv(文件所在位置)
#
#         #【重要】将该死的\t符号干掉
#         data['运单号'] = data['运单号'].str.strip('\t')
#
#         #【清除左右字符串，默认为空格】匹配第一个和最后一个字符，分别看左边和有边有无指定字符，有则清除
#         data['运单号'].str.strip()
#         data['运单号'] = data['运单号'].astype(str)
#         #统一字段名称
#         data.rename(columns={'订单号':'订单编号'},inplace = True)
#         判断表格名 = True
#     return (data,判断表格名)

#———————————————————————————————————————————————————————————————上拼多多，下京东———————————————————————————————————————————————————————————————— 

def 京东处理模块(文件所在位置,文件类型,表格类型):
    
    判断表格名 = False
    if 表格类型 == '订单表' :
        #判断文件类型，防止平台后期修改文件的保存格式
        if 文件类型 == '.xlsx' :
            data = pd.read_excel(文件所在位置,usecols=['订单号','商品ID','商品名称','订购数量','结算金额','下单时间','订单状态'])
        elif 文件类型 == '.csv' :
            try:
                data = pd.read_csv(文件所在位置,usecols=['订单号','商品ID','商品名称','订购数量','结算金额','下单时间','订单状态'])
            except(UnicodeDecodeError):
                data = pd.read_csv(文件所在位置,usecols=['订单号','商品ID','商品名称','订购数量','结算金额','下单时间','订单状态'],encoding='GB18030')
            
        #筛选去除不重要的数据
        data = data[~(data.订单状态.isin(['(删除)延迟付款确认'])|data.订单状态.isin(['(删除)等待付款确认'])|data.订单状态.isin(['调度中']))]
        
        #数据的某一列=数据的某一列进行格式转换，来达成清除前后空格
        data['下单时间'] = data['下单时间'].astype('datetime64[ns]')
        #超过4位数会有逗号，需要统一转换为str使用replace去除
        data['结算金额'] = data['结算金额'].astype(str)
        data['结算金额'] = data['结算金额'].str.replace(',','')
        
        data['结算金额'] = data['结算金额'].astype(float)
        data['商品ID'] = data['商品ID'].astype(str)
        data['订单号'] = data['订单号'].astype(str)
        data['下单日期'] = pd.to_datetime(data['下单时间'])
        data['下单日期'] = data['下单日期'].dt.date
        
        #数据处理，京东需要去重
        data = data.drop_duplicates('订单号')
        
        # #统一字段的名称
        data.rename(columns={'订单号':'订单编号'},inplace = True)
        data.rename(columns={'下单时间':'订单创建时间'},inplace = True)
        data.rename(columns={'下单日期':'订单创建日期'},inplace = True)
        data.rename(columns={'订购数量':'成交数量'},inplace = True)
        data.rename(columns={'结算金额':'订单应付金额'},inplace = True)
        # data.rename(columns={'商品ID':'商品编号'},inplace = True)
        判断表格名 = True
        
    elif 表格类型 == '账单表' :
        
        if 文件类型 == '.xlsx' :
            data = pd.read_excel(文件所在位置,usecols=['订单编号','费用结算时间','金额','单据类型','费用项','收支方向'])
        elif 文件类型 == '.csv' :            
            try:       
                data = pd.read_csv(文件所在位置,usecols=['订单编号','费用结算时间','金额','单据类型','费用项','收支方向'])
            except(ValueError):
                #京东的账单表，无法匹配出usecols，报错ValueError: Usecols do not match columns, columns expected but not found: ['金额', '费用结算时间', '订单编号', '单据类型', '收支方向', '费用项']
                data = pd.read_csv(文件所在位置,usecols=['订单编号','费用结算时间','金额','单据类型','费用项','收支方向'],encoding='GB18030')
                
        data['费用结算时间'] = data['费用结算时间'].astype('datetime64[ns]')
        #将时间戳转换为datetime格式,dt.date单位为天,str方便用户看
        data['费用结算日期'] = pd.to_datetime(data['费用结算时间'])
        data['费用结算日期'] = data['费用结算日期'].dt.date
        data['费用结算日期'] = data['费用结算日期'].astype(str)
        # #统一字段的名称
        data.rename(columns={'订单号':'订单编号'},inplace = True)
        data.rename(columns={'金额':'实际结算金额(元)'},inplace = True)
        data.rename(columns={'费用结算时间':'实际结算时间'},inplace = True)
        data.rename(columns={'费用结算日期':'实际结算日期'},inplace = True)
        判断表格名 = True
        
    return (data,判断表格名) 

#———————————————————————————————————————————————————————————————上京东，下天猫———————————————————————————————————————————————————————————————— 

def 天猫处理模块(文件所在位置,文件类型,表格类型):
    
    def 提取最长数字串(strings): 
        try:
            #匹配2-10位字母与数字组成的子串，返回一个数组（列表）
            ret = re.search("\d+",strings)
        except(TypeError):
            #因为有可能商家编码为空值
            return 'Empty'
                    
        return ret.group() #用group返回对象中的值
    判断表格名 = False
    if 表格类型 == '订单表' :
        #判断文件类型，防止平台后期修改文件的保存格式
        #注意天猫的物流单号有空格
        if 文件类型 == '.xlsx' :
            data = pd.read_excel(文件所在位置,usecols=['主订单编号','子订单编号','买家应付货款','标题','订单状态','订单创建时间','物流单号','物流公司','购买数量','退款状态','退款金额','发货时间'])
        elif 文件类型 == '.csv' :
            try:
                data = pd.read_csv(文件所在位置,usecols=['主订单编号','子订单编号','买家应付货款','标题','订单状态','订单创建时间','物流单号','物流公司','购买数量','退款状态','退款金额','发货时间'])
            except(UnicodeDecodeError):
                data = pd.read_csv(文件所在位置,usecols=['主订单编号','子订单编号','买家应付货款','标题','订单状态','订单创建时间','物流单号','物流公司','购买数量','退款状态','退款金额','发货时间'],encoding='GB18030')

        # 主订单编号使用replace去除=与""
        data['主订单编号'] = data['主订单编号'].astype(str)
        data['主订单编号'] = data['主订单编号'].str.replace('=', '')
        data['主订单编号'] = data['主订单编号'].str.replace('"', '')
        # 子订单编号使用replace去除=与""
        data['子订单编号'] = data['子订单编号'].astype(str)
        data['子订单编号'] = data['子订单编号'].str.replace('=', '')
        data['子订单编号'] = data['子订单编号'].str.replace('"', '')

        data['退款金额'] = data['退款金额'].astype(str)
        data['退款金额'] = data['退款金额'].str.replace('无退款申请', '0')
        data['退款金额'] = data['退款金额'].astype(float)
        # 数据的某一列=数据的某一列进行格式转换，来达成清除前后空格
        data['订单创建时间'] = data['订单创建时间'].astype('datetime64[ns]')
        data['发货时间'] = data['发货时间'].astype('datetime64[ns]')

        data['订单创建日期'] = pd.to_datetime(data['订单创建时间'])
        data['订单创建日期'] = data['订单创建日期'].dt.date

        data['发货日期'] = pd.to_datetime(data['发货时间'])
        data['发货日期'] = data['发货日期'].dt.date

        # #统一字段的名称
        data.rename(columns={'主订单编号': '订单编号'}, inplace=True)
        data.rename(columns={'子订单编号': '商品单号'}, inplace=True)
        data.rename(columns={'物流单号': '运单号'}, inplace=True)
        data.rename(columns={'购买数量': '成交数量'}, inplace=True)
        data.rename(columns={'买家应付货款': '订单应付金额'}, inplace=True)
        data.rename(columns={'退款金额': '退货退款金额'}, inplace=True)
        data.rename(columns={'退款状态': '售后状态'}, inplace=True)
        data.rename(columns={'标题': '商品名称'}, inplace=True)

        判断表格名 = True
        
        return (data,判断表格名)

    elif 表格类型 == '售后表' :
        if 文件类型 == '.xls' or 文件类型 == '.xlsx' :
            data = pd.read_excel(文件所在位置,usecols=['订单编号','退款的申请时间','宝贝标题'])
        
        data['退款的申请时间'] = data['退款的申请时间'].astype('datetime64[ns]')
        data['退款的申请时间日期'] = pd.to_datetime(data['退款的申请时间'])
        data['退款的申请时间日期'] = data['退款的申请时间日期'].dt.date
        
        data['订单编号'] = data['订单编号'].astype(str)
        data['宝贝标题'] = data['宝贝标题'].astype(str)
        
        # #统一字段的名称
        data.rename(columns={'退款的申请时间':'售后申请时间'},inplace = True)  
        data.rename(columns={'退款的申请时间日期':'售后申请日期'},inplace = True)
        data.rename(columns={'宝贝标题':'商品名称'},inplace = True)
        
        判断表格名 = True
        
        return (data,判断表格名)    

    elif 表格类型 == '账单表' :
        #只允许天猫淘宝的账单表的格式为xlsx
        data = pd.DataFrame()

        for i in range(1,8):
            """
            1、外层选择用try把未知数量的sheet分别打开再合并
            2、if语句用于将第一个sheet中的无关信息读取时忽略掉
            """
            try:
                if i == 1 :
                    #为了删除前两行的无关信息，所以header=2
                    temp_data = pd.read_excel(文件所在位置,sheet_name=f'账务组合查询{i}',header=2,usecols=[1,5,6,7,9,13,16,17,20])
                    col_name = temp_data.columns.tolist() #提取表头城列表
                    print(i)
                else:
                    temp_data = pd.read_excel(文件所在位置,sheet_name=f'账务组合查询{i}',header=None,usecols=[1,5,6,7,9,13,16,17,20])
                    temp_data.columns = col_name #为其他sheet添加表头
                    print(i)
                data = pd.concat([data,temp_data],axis=0,ignore_index=True)
                # 删除temp_data释放内存，但这不会删除对象，只会删名字

            except:
                #打开完所有的sheet后会跳转到此2语句，跳出循环
                break

        del temp_data
        gc.collect()
        print(data)
        data.reset_index(inplace=True,drop=True)
        #干掉最后一行垃圾数据
        data.drop([len(data)-1],inplace=True)
        
        """
        测算总结：淘宝天猫的待结算测算，其实就只考虑交易收款即可，是待结算的唯一出口。
        之前抖音是平台扣点、佣金是结算前就扣除了，所以需要考虑，但天猫是结算后再扣除
        计费总结：货款结算 - 佣金 - 服务费
        """
        #清空前后字符串
        data['业务描述'] = data['业务描述'].str.strip()
        data['业务描述'] = data['业务描述'].astype(str)
        data['收入（+元）'] = data['收入（+元）'].astype(str)
        data['支出（-元）'] = data['支出（-元）'].astype(str)
        #格式转换
        data['入账时间'] = data['入账时间'].astype('datetime64[ns]')
        data['实际结算日期'] = pd.to_datetime(data['入账时间'])
        data['实际结算日期'] = data['实际结算日期'].dt.date
        
        #清空前后字符串
        data['收入（+元）'] = data['收入（+元）'].str.strip()
        data['支出（-元）'] = data['支出（-元）'].str.strip()
        # data['服务费（元）'] = data['服务费（元）'].str.strip()
        #清除字符串后才能将空值填充
        data['收入（+元）'] = data['收入（+元）'].replace('','0')
        data['支出（-元）'] = data['支出（-元）'].replace('','0')
        data['服务费（元）'] = data['服务费（元）'].replace('','0')
        #将字符串转换为可以计算的float类型
        data['收入（+元）'] = data['收入（+元）'].astype(float)
        data['支出（-元）'] = data['支出（-元）'].astype(float)
        data['服务费（元）'] = data['服务费（元）'].astype(float)
        
        #先删除收费，因为想要订单本身
        data = data[~data.账务类型.isin(['收费'])]
        #在筛选其中需要的行数据
        data1 = data[(data.业务描述.isin(['']))]
        data2 = data[~(data.业务描述.isin(['']))]
        
        #先对业务描述列进行空值处理
        data1['业务描述'] = data1['业务描述'].str.replace('','无描述')
        #筛选无业务描述的，无业务描述中：在线支付大于0的，转账中转给官方的，其他中全部
        data1 = data1[data1.账务类型.isin(['转账','其它','在线支付'])]
        data1 = data1[~(data1.账务类型.isin(['在线支付'])&data1['收入（+元）'].isin([0]))]
        data1 = data1[~(data1.账务类型.isin(['转账'])&~(data1.对方名称.isin(['阿里巴巴华南技术有限公司广东第一分公司','浙江天猫技术有限公司','杭州阿里妈妈软件服务有限公司','阿里巴巴华南技术有限公司'])))]
        data1 = data1[~(data1.账务类型.isin(['其它'])&~(data1.备注.isin(['网商贷-放款','网商贷-还款'])))]
        # #筛选有业务描述的
        # data2 = data2[~(data2.账务类型.isin(['退款（交易退款）']))]
        #合并
        data = pd.concat([data1,data2])
        data.reset_index(inplace=True,drop=True)
        

        #运算
        data['实际结算金额(元)'] = data['收入（+元）'] - data['支出（-元）'] - data['服务费（元）']

        data = data.loc[:,['业务基础订单号','实际结算金额(元)','入账时间','实际结算日期','备注','账务类型','业务描述']]

        #统一字段名称
        data.rename(columns={'业务基础订单号' : '订单编号'},inplace = True)
        data.rename(columns={'入账时间': '实际结算时间'}, inplace=True)

        判断表格名 = True
        
        return (data,判断表格名)
    
    elif 表格类型 == '淘客表' :
        if 文件类型 == '.xlsx' :
            data = pd.read_excel(文件所在位置,usecols=['淘宝主订单号','淘宝子订单号','预估佣金','商品名称','商品ID','达人昵称','订单创建时间'])
        elif 文件类型 == '.csv' :
            try:
                data = pd.read_csv(文件所在位置,usecols=['淘宝主订单号','淘宝子订单号','预估佣金','商品名称','商品ID','达人昵称','订单创建时间'])
            except(UnicodeDecodeError):
                data = pd.read_csv(文件所在位置,usecols=['淘宝主订单号','淘宝子订单号','预估佣金','商品名称','商品ID','达人昵称','订单创建时间'],encoding='GB18030')
        
        data['淘宝主订单号'] = data['淘宝主订单号'].astype(str)
        data['淘宝子订单号'] = data['淘宝子订单号'].astype(str)
        data['商品ID'] = data['商品ID'].astype(str)
        data['预估佣金'] = data['预估佣金'].astype(float)

        
        #统一字段名称
        data.rename(columns={'淘宝主订单号':'订单编号'},inplace = True)
        data.rename(columns={'淘宝子订单号':'商品单号'},inplace = True)
        
        判断表格名 = True
         
        return (data,判断表格名)
    
    elif 表格类型 == '宝贝表' :
        if 文件类型 == '.xlsx' :
            data = pd.read_excel(文件所在位置,usecols=['主订单编号','子订单编号','商家编码','订单状态','订单创建时间','购买数量','买家应付货款','退款状态','标题'])
        elif 文件类型 == '.csv' :
            try:
                data = pd.read_csv(文件所在位置,usecols=['主订单编号','子订单编号','商家编码','订单状态','订单创建时间','购买数量','买家应付货款','退款状态','标题'])
            except(UnicodeDecodeError):
                data = pd.read_csv(文件所在位置,usecols=['主订单编号','子订单编号','商家编码','订单状态','订单创建时间','购买数量','买家应付货款','退款状态','标题'],encoding='GB18030')
        
        #筛选去除不重要的数据
        data = data[~(data.订单状态.isin(['等待买家付款']))]
        data = data[~(data.买家应付货款.isin([0]))]
        #数据的某一列=数据的某一列进行格式转换，来达成清除前后空格
        data['订单创建时间'] = data['订单创建时间'].astype('datetime64[ns]')
    
        data['标题'] = data['标题'].astype(str)
        data['主订单编号'] = data['主订单编号'].astype(str)
        data['子订单编号'] = data['子订单编号'].astype(str)
        data['主订单编号'] = data['主订单编号'].map(提取最长数字串)
        data['子订单编号'] = data['子订单编号'].map(提取最长数字串)
        data['买家应付货款'] = data['买家应付货款'].astype(float)
        data['订单创建日期'] = pd.to_datetime(data['订单创建时间'])
        data['订单创建日期'] = data['订单创建日期'].dt.date
        
        #统一字段名称
        data.rename(columns={'主订单编号':'订单编号'},inplace = True)
        data.rename(columns={'子订单编号':'商品单号'},inplace = True)
        data.rename(columns={'购买数量':'成交数量'},inplace = True)
        data.rename(columns={'买家应付货款':'订单应付金额'},inplace = True)
        data.rename(columns={'标题':'商品名称'},inplace = True)

        判断表格名 = True
         
        return (data,判断表格名)


def 视频号处理模块(文件所在位置, 文件类型, 表格类型):
    判断表格名 = False

    def timeformat(timestamp):
        change = datetime.datetime.strptime(str(timestamp), '%Y/%m/%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        return change

    if 表格类型 == '订单表':
        # 读取文件
        # 判断文件类型，防止平台后期修改文件的保存格式
        if 文件类型 == '.xlsx':
            try:
                data = pd.read_excel(文件所在位置,
                                     usecols=['订单号', '订单创建时间', '订单状态', '实付款', '预估推广佣金', '商品名称', '商品ID', '成交数量', '售后状态',
                                              'SKU编码', 'CPS达人ID', 'CPS达人昵称', '商品单价', '团长ID', '发货时间', '快递单号', '快递公司'])
                data['预估推广佣金'] = data['预估推广佣金'].astype(str)
                data['预估推广佣金'] = data['预估推广佣金'].astype('float')
                # data.rename(columns={'预估推广佣金':'订单佣金'},inplace = True)
            except(ValueError):
                data = pd.read_excel(文件所在位置,
                                     usecols=['订单号', '订单创建时间', '订单状态', '实付款', '商品名称', '商品ID', '成交数量', '售后状态', 'SKU编码',
                                              'CPS达人ID', 'CPS达人昵称', '商品单价', '团长ID', '发货时间', '快递单号', '快递公司'])

        elif 文件类型 == '.csv':
            try:
                try:
                    data = pd.read_csv(文件所在位置,
                                       usecols=['订单号', '订单创建时间', '订单状态', '实付款', '预估推广佣金', '商品名称', '商品ID', '成交数量',
                                                '售后状态', 'SKU编码', 'CPS达人ID', 'CPS达人昵称', '商品单价', '团长ID', '发货时间', '快递单号',
                                                '快递公司'])
                    data['预估推广佣金'] = data['预估推广佣金'].astype(str)
                    data['预估推广佣金'] = data['预估推广佣金'].astype('float')
                    # data.rename(columns={'预估推广佣金':'订单佣金'},inplace = True)
                except(ValueError):
                    data = pd.read_csv(文件所在位置,
                                       usecols=['订单号', '订单创建时间', '订单状态', '实付款', '商品名称', '商品ID', '成交数量', '售后状态', 'SKU编码',
                                                'CPS达人ID', 'CPS达人昵称', '商品单价', '团长ID', '发货时间', '快递单号', '快递公司'])

            except(UnicodeDecodeError):
                try:
                    data = pd.read_csv(文件所在位置,
                                       usecols=['订单号', '订单创建时间', '订单状态', '实付款', '预估推广佣金', '商品名称', '商品ID', '成交数量',
                                                '售后状态', 'SKU编码', 'CPS达人ID', 'CPS达人昵称', '商品单价', '团长ID', '发货时间', '快递单号',
                                                '快递公司'], encoding='GB18030')
                    data['预估推广佣金'] = data['预估推广佣金'].astype(str)
                    data['预估推广佣金'] = data['预估推广佣金'].astype('float')
                    # data.rename(columns={'预估推广佣金':'订单佣金'},inplace = True)
                except(ValueError):
                    data = pd.read_csv(文件所在位置,
                                       usecols=['订单号', '订单创建时间', '订单状态', '实付款', '商品名称', '商品ID', '成交数量', '售后状态', 'SKU编码',
                                                'CPS达人ID', 'CPS达人昵称', '商品单价', '团长ID', '发货时间', '快递单号', '快递公司'],
                                       encoding='GB18030')

        data.rename(columns={'售后状态': '退货退款'}, inplace=True)
        # 删除无用记录，交易关闭且退货退款为空的订单是未支付订单
        data = data[~(data.订单状态.isin(['交易关闭']) & data.退货退款.isnull())]
        data = data[data['订单状态'] != '待付款']
        # 去除符号转换为可以计算的数字格式
        data['实付款'] = data['实付款'].astype(str)
        data['实付款'] = data['实付款'].str.replace('¥', '')
        data['实付款'] = data['实付款'].astype('float')

        # 避免订单号位数过长丢失数据
        data['订单号'] = data['订单号'].astype(str)
        data['商品ID'] = data['商品ID'].astype(str)
        # 时间格式转换模块：从时间戳转换成时间组件
        data['订单创建日期'] = pd.to_datetime(data['订单创建时间'])
        data['订单创建日期'] = data['订单创建日期'].dt.date
        data['订单创建日期'] = data['订单创建日期'].astype(str)

        data['CPS达人ID'] = data['CPS达人ID'].astype('Int64')
        data['CPS达人ID'].fillna(value=0, axis=0, inplace=True)
        data['CPS达人ID'] = data['CPS达人ID'].astype(str)
        data['CPS达人ID'] = data['CPS达人ID'].replace('0', '')

        # 统一字段的名称
        data.rename(columns={'订单号': '订单编号'}, inplace=True)
        # data.rename(columns={'退货退款':'售后状态'},inplace = True)
        data.rename(columns={'实付款': '订单应付金额'}, inplace=True)
        data.rename(columns={'SKU编码': '商家编码'}, inplace=True)
        # 判断表格名 = True

        data['发货日期'] = pd.to_datetime(data['发货时间'])
        data['发货日期'] = data['发货日期'].dt.date
        # 避免订单号位数过长丢失数据
        data['快递单号'] = data['快递单号'].astype(str)

        data = data.sort_values(by='发货时间', ascending=True)

        # 统一字段的名称
        # data.rename(columns={'订单号': '订单编号'}, inplace=True)
        data.rename(columns={'快递单号': '运单号'}, inplace=True)
        判断表格名 = True

    elif 表格类型 == '运单表':
        # 读取文件
        # 判断文件类型，防止平台后期修改文件的保存格式
        def 删除无用尾缀(string):
            lit = string.split('.')
            return lit[0]

        try:
            if 文件类型 == '.xlsx':
                data = pd.read_excel(文件所在位置, usecols=['发货/揽收/末条中转/派件/待取件/签收时间', '订单编号', '物流单号'])
            elif 文件类型 == '.xls':
                data = pd.read_excel(文件所在位置, usecols=['发货/揽收/末条中转/派件/待取件/签收时间', '订单编号', '物流单号'])
            elif 文件类型 == '.csv':
                data = pd.read_csv(文件所在位置, usecols=['发货/揽收/末条中转/派件/待取件/签收时间', '订单编号', '物流单号'])
            data['物流单号'] = data['物流单号'].astype(str)
            # 统一字段的名称
            data.rename(columns={'物流单号': '运单号'}, inplace=True)
            data.rename(columns={'发货/揽收/末条中转/派件/待取件/签收时间': '发货时间'}, inplace=True)  # 下载内容的本质是揽收就是揽收

        except:
            if 文件类型 == '.xlsx':
                data = pd.read_excel(文件所在位置, usecols=['发货时间', '订单编号', '快递单号'])
            elif 文件类型 == '.csv':
                data = pd.read_csv(文件所在位置, usecols=['发货时间', '订单编号', '快递单号'])
            data['快递单号'] = data['快递单号'].astype(str)
            # 统一字段的名称
            data.rename(columns={'快递单号': '运单号'}, inplace=True)

        # 避免订单号位数过长丢失数据
        data.dropna(axis=0, subset=['订单编号'], how='any', inplace=True)
        data.dropna(axis=0, subset=['发货时间'], how='any', inplace=True)
        data['订单编号'] = data['订单编号'].astype(np.int64)
        data['订单编号'] = data['订单编号'].astype(str)
        data['订单编号'] = data['订单编号'].map(删除无用尾缀)

        try:
            data['发货时间'] = data['发货时间'].map(timeformat)
        except:
            pass
        data['发货日期'] = pd.to_datetime(data['发货时间'])
        data['发货日期'] = data['发货日期'].dt.date

        判断表格名 = True

    # elif 表格类型 == '仓运单表' :
    #     #读取文件
    #     #判断文件类型，防止平台后期修改文件的保存格式
    #     if 文件类型 == '.xlsx' :
    #         data = pd.read_excel(文件所在位置,usecols=['发货时间','订单号','快递单号','仓库名称','快递公司'])
    #     elif 文件类型 == '.csv' :
    #         data = pd.read_csv(文件所在位置,usecols=['发货时间','订单号','快递单号','仓库名称','快递公司'])
    #
    #     #避免订单号位数过长丢失数据
    #     data['发货时间'] = data['发货时间'].map(timeformat)
    #     data['发货日期'] = pd.to_datetime(data['发货时间'])
    #     data['发货日期'] = data['发货日期'].dt.date
    #     data['订单号'] = data['订单号'].astype(str)
    #     data['快递单号'] = data['快递单号'].astype(str)
    #
    #     data = data.sort_values(by='发货时间', ascending=True)
    #     data = data.drop_duplicates(subset=['订单号'],keep='first')
    #
    #     #统一字段的名称
    #     data.rename(columns={'订单号':'订单编号'},inplace = True)
    #     data.rename(columns={'快递单号':'运单号'},inplace = True)
    #     判断表格名 = True

    elif 表格类型 == '售后表':
        # 读取文件
        # 判断文件类型，防止平台后期修改文件的保存格式
        if 文件类型 == '.xlsx':
            try:
                data = pd.read_excel(文件所在位置, usecols=['订单编号', '售后状态', '售后类型', '售后申请时间', '退款金额'])
                data['售后申请日期'] = pd.to_datetime(data['售后申请时间'])
                data['售后申请日期'] = data['售后申请日期'].dt.date
            except(ValueError):
                data = pd.read_excel(文件所在位置, usecols=['订单编号', '售后状态', '售后类型', '申请时间', '退款金额'])
                data.rename(columns={'申请时间': '售后申请时间'}, inplace=True)
                data['售后申请日期'] = pd.to_datetime(data['售后申请时间'])
                data['售后申请日期'] = data['售后申请日期'].dt.date
        elif 文件类型 == '.csv':
            try:
                data = pd.read_csv(文件所在位置, usecols=['订单编号', '售后状态', '售后类型', '售后申请时间', '退款金额'])
                data['售后申请日期'] = pd.to_datetime(data['售后申请时间'])
                data['售后申请日期'] = data['售后申请日期'].dt.date
            except(ValueError):
                data = pd.read_csv(文件所在位置, usecols=['订单编号', '售后状态', '售后类型', '申请时间', '退款金额'])
                data.rename(columns={'申请时间': '售后申请时间'}, inplace=True)
                data['售后申请日期'] = pd.to_datetime(data['售后申请时间'])
                data['售后申请日期'] = data['售后申请日期'].dt.date
        # 删除无用记录，只留下退款成功
        data = data[~(data.售后状态.isin(['售后失败', '售后关闭']))]

        # 【待更新算法】 可以把去掉售后关闭后的，依然还重复的订单号，金额上求和，申请日期保留最早那个
        data = data.sort_values(by='退款金额', ascending=False)
        data = data.drop_duplicates(subset=['订单编号'], keep='first')

        # 去除符号转换为可以计算的数字格式
        data['退款金额'] = data['退款金额'].astype(str)
        data['退款金额'] = data['退款金额'].str.replace('¥', '')
        data['退款金额'] = data['退款金额'].astype('float')
        # 格式转换

        # #时间格式转换模块：从时间戳转换成时间组件
        # data['订单创建日期'] = pd.to_datetime(data['订单创建时间'])
        # data['订单创建日期'] = data['订单创建日期'].dt.date
        # data['订单创建日期'] = data['订单创建日期'].astype(str)
        # #将退款金额改名，防止后面冲突
        # data.rename(columns = {'退款金额':'应退款金额'},inplace = True)
        # 一定要将多位数的订单编号转成字符串
        data['订单编号'] = data['订单编号'].astype(str)
        # data['申请时间'] = data['申请时间'].astype(str)

        # 统一字段名称
        data.rename(columns={'退款金额': '实退款金额'}, inplace=True)

        判断表格名 = True

    elif 表格类型 == '账单表':
        if 文件类型 == '.xlsx':
            data = pd.read_excel(文件所在位置, usecols=['订单号', '实际结算金额(元)', '实际结算时间', '订单创建时间'])
        elif 文件类型 == '.csv':
            try:
                data = pd.read_csv(文件所在位置, usecols=['订单号', '实际结算金额(元)', '实际结算时间', '订单创建时间'])
            except(UnicodeDecodeError):
                data = pd.read_csv(文件所在位置, usecols=['订单号', '实际结算金额(元)', '实际结算时间', '订单创建时间'], encoding='GB18030')

        # 将时间戳转换为datetime格式,dt.date单位为天,str方便用户看
        data['订单创建日期'] = pd.to_datetime(data['订单创建时间'])
        data['订单创建日期'] = data['订单创建日期'].dt.date
        data['订单创建日期'] = data['订单创建日期'].astype(str)
        data['实际结算日期'] = pd.to_datetime(data['实际结算时间'])
        data['实际结算日期'] = data['实际结算日期'].dt.date
        data['实际结算日期'] = data['实际结算日期'].astype(str)

        data['订单号'] = data['订单号'].astype(str)
        # 统一字段的名称
        data.rename(columns={'订单号': '订单编号'}, inplace=True)
        判断表格名 = True

    else:
        print('文件命名错误(订单表，运单表，售后表)')

    return (data, 判断表格名)

from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog, QWidget
from ui_CleanTool import Ui_Form



class Clean(QWidget):

    def __init__(self):
        super().__init__()
        # 使用ui_Clean文件导入界面定义类
        self.ui = Ui_Form()
        self.ui.setupUi(self)  # 传入QWidget对象
        self.ui.retranslateUi(self)

        # 实例变量
        self.输入路径 = ''
        self.输出路径 = ''
        self.操作人 = ''
        self.客户名称 = ''
        self.temp = ''  # 用于保存打开文件的路径
        self.判断表格名 = False
        
        #按钮
        self.ui.InputButton.clicked.connect(self.getInputDir)
        self.ui.OutputButton.clicked.connect(self.getOutputDir)
        self.ui.RunButton.clicked.connect(self.handleClean)
        
        
        
    def getInputDir(self):  # 获取InputButton的返回路径
        self.temp = QFileDialog.getExistingDirectory(self, "选择输入路径")  # 不是self.ui
        if self.temp != '':
            self.输入路径 = self.temp
            self.ui.InputDir.setText(self.输入路径)  # 显示路径

    def getOutputDir(self):  # 获取OutputButton的返回路径
        self.temp = QFileDialog.getExistingDirectory(self, "选择输出路径")
        if self.temp != '':
            self.输出路径 = self.temp
            self.ui.OutputDir.setText(self.输出路径)
        
    def handleClean(self):

        # 获取输入值
        self.操作人 = self.ui.User.text()
        self.客户名称 = self.ui.Customer.text()
        # 输入为空的情况
        if self.输入路径 == '':
            QMessageBox.about(self, "报错！", '输入文件夹为空')
            return
        if self.输出路径 == '':
            QMessageBox.about(self, "报错！", '输出文件夹为空')
            return
        if self.操作人 == '':
            QMessageBox.about(self, "报错！", '请输入操作人')
            return
        if self.客户名称 == '':
            QMessageBox.about(self, "报错！", '请输入客户名称')
            return

        # 获取一个文件夹下的所有文件名
        所有文件名列表 = os.listdir(self.输入路径)

        for 文件名 in 所有文件名列表:
            # 平台类型-表格类型-备注
            # 自动获取：平台类型-0、表格类型-1、备注-2、
            # 用户输入：操作人、客户名称

            # 获取到形如：抖音-订单表-备注.xlsx 或者是 抖音-订单表.xlsx
            文件名后缀 = os.path.splitext(文件名)[1]  # 【以最右边的.作为分割】包括.
            文件名前缀 = os.path.splitext(文件名)[0]
            文件类型 = 文件名后缀  # 包括.
            文件所在位置 = self.输入路径 + '\\' + 文件名
            # 根据文件名前缀来执行不同的逻辑模块（还要区分快手抖音）
            平台类型 = 文件名前缀.split('-')[0]  # if
            表格类型 = 文件名前缀.split('-')[1]  # if

            # 【识别平台模块】
            if 平台类型 == '快手':
                数据表,self.判断表格名 = 快手处理模块(文件所在位置, 文件类型, 表格类型)
            elif 平台类型 == '抖音':
                数据表,self.判断表格名 = 抖音处理模块(文件所在位置, 文件类型, 表格类型)
            elif 平台类型 == '拼多多':
                数据表 = 拼多多理模块(self.输入路径,文件名)
                self.判断表格名 = True
            elif 平台类型 == '京东':
                数据表,self.判断表格名 = 京东处理模块(文件所在位置,文件类型,表格类型)
            elif 平台类型 == '天猫':
                数据表,self.判断表格名 = 天猫处理模块(文件所在位置,文件类型,表格类型)
            elif 平台类型 == '淘宝':
                #淘宝的逻辑暂时等同于天猫
                数据表,self.判断表格名 = 天猫处理模块(文件所在位置,文件类型,表格类型)
            else:
                # print('命名格式错误：平台类型')
                QMessageBox.about(self, "报错！", "命名格式错误：平台类型")  # 不是self.ui
                return  # 直接返回函数，所有该函数体内的代码（包括循环体）都不会再执行。

            # 【备注模块】查看是否有备注
            查看长度 = 文件名前缀.split('-')
            if len(查看长度) == 3:
                备注 = 文件名前缀.split('-')[2]
            elif len(查看长度) > 3:
                # print('命名格式错误：“-”符号不得超于3个')
                QMessageBox.about(self, "报错！", '命名格式错误：“-”符号不得超于3个')
                return
            else:
                备注 = '无备注'

            输出文件名格式 = f'\\{self.客户名称}-{平台类型}-{表格类型}-{self.操作人}-{备注}.xlsx'
            文件保存路径 = self.输出路径 + 输出文件名格式
            #输出
            数据表.to_excel(文件保存路径, index=False)
            
            if self.判断表格名 == False:
                QMessageBox.about(self, "报错！", '请输入正确的表格名称')
                return
            
        QMessageBox.about(self, "表格处理结果", f'成功！\n请于“{self.输出路径}”查看结果文件')

if __name__ == '__main__':
    app = QApplication([])
    window = Clean()
    window.show()
    app.exec_()
