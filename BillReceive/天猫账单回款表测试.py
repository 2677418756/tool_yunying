import pandas as pd

import pandas as pd
import datetime as datetime
import numpy as np
import os


class AutoExtractFiles():

    def __init__(self, 文件夹路径, 需打开表格名列表):
        # 实例变量初始化
        self.输出字典 = {}
        self.文件夹路径 = 文件夹路径
        self.需打开表格名列表 = 需打开表格名列表

    def handle(self):

        所有文件名列表 = os.listdir(self.文件夹路径)
        计数满足 = len(self.需打开表格名列表)

        for file in 所有文件名列表:
            # 判断列表中元素是否存在，若存在则打开
            文件名前缀 = os.path.splitext(file)[0]
            表格类型 = 文件名前缀.split('-')[2]  # FOLA旗舰店-抖音-剩余金额表-2022-05-14.xlsx
            for need_workbook in self.需打开表格名列表:
                if 表格类型 == need_workbook:
                    # 记录需打开的文件名，最后返回
                    计数满足 = 计数满足 - 1  # 若所需文件全部都存在，则最后计数为0
                    temp = self.文件夹路径 + '\\' + file
                    self.输出字典[表格类型] = temp

        return self.输出字典


def 函数_提取日期(去重后, 字符串日期):
    近20天日期列表 = []
    for 订单创建日期 in 去重后.loc[:, f'{字符串日期}']:
        近20天日期列表.append(订单创建日期)
    return 近20天日期列表


def 函数_计算日期差值(订单创建日期, 对应实际结算日期列表):
    存放空间 = []
    创建日期 = datetime.datetime.strptime(订单创建日期, '%Y-%m-%d')
    for 实际结算日期 in 对应实际结算日期列表:
        结算日期 = datetime.datetime.strptime(实际结算日期, '%Y-%m-%d')

        差值 = 结算日期 - 创建日期

        存放空间.append(差值.days + 1)

    存放空间.sort()

    return 存放空间


def 抖音求和对比(账单表, 结算表):
    sum1 = 账单表['实际结算金额(元)'].sum()
    sum2 = 结算表['实际结算金额(元)'].sum()
    if sum1 >= sum2:
        final_dataframe = 账单表
    elif sum1 < sum2:
        final_dataframe = 结算表

    return final_dataframe


def one_decimal(x_data):
    # 【浮点数先转字符串，再转浮点数】让数据保留一位小数，且自动四舍五入
    x_str = '%.1f' % x_data  # 变成字符串来保留一位小数了
    return float(x_str)


def two_decimal(x_data):
    # 【浮点数先转字符串，再转浮点数】让数据保留一位小数，且自动四舍五入
    x_str = '%.2f' % x_data  # 变成字符串来保留一位小数了
    return float(x_str)

def 天猫账单回款表(订单表 ,账单表):

    # 先将账单回款总表做出
    用于合并 = pd.DataFrame()

    # 第一句将时间戳转换为datatime时间组件，第二句将短日期组件提取出来，第三句转换成str方便用户查看与程序使用
    订单表['订单创建日期'] = pd.to_datetime(订单表['订单创建日期'])
    订单表['订单创建日期'] = 订单表['订单创建日期'].dt.date
    订单表['订单创建日期'] = 订单表['订单创建日期'].astype(str)

    订单表['主订单编号'] = 订单表['主订单编号'].astype(str)
    账单表['订单编号'] = 账单表['订单编号'].astype(str)

    # 将浮点数按一位小数使用
    账单表['实际结算金额(元)'] = 账单表['实际结算金额(元)'].map(two_decimal)

    # 第一句将时间戳转换为datatime时间组件，第二句将短日期组件提取出来，第三句转换成str方便用户查看与程序使用
    账单表['实际结算日期'] = pd.to_datetime(账单表['实际结算日期'])
    账单表['实际结算日期'] = 账单表['实际结算日期'].dt.date
    账单表['实际结算日期'] = 账单表['实际结算日期'].astype(str)

    # 筛选
    #对订单表进行分组求和，对账单表进行筛选只保留订单结算和定金交易结算
    用于粗糙的计费表 = 账单表[账单表.业务描述.isin(['0010001|交易收款-交易收款' ,'0010002|交易收款-预售定金（买家责任不退还）'])]

    用于计费 = 账单表[~(账单表.备注.isin(['网商贷-放款' ,'网商贷-还款'] ) |账单表.账务类型.isin(['贷款还款']))]

    # 先将账单表的数据进行透析形成回款总表
    回款总表 = pd.pivot_table(用于计费 ,index=['实际结算日期'] ,values=['实际结算金额(元)'] ,aggfunc = [np.sum])

    # 给计费表用，只读取进账
    账单合并订单 = pd.merge(用于粗糙的计费表 ,订单表 ,how='left' ,left_on='订单编号' ,right_on = '主订单编号')
    账单合并订单.dropna(axis = 0 ,how='any', subset=['订单创建日期'], inplace=True)

    # 回款透析1 = pd.pivot_table(账单合并订单,index=['实际结算日期'],columns = ['订单创建日期'],values=['实际结算金额(元)'],aggfunc = [np.sum])
    # 回款透析1.columns = 回款透析1.columns.droplevel(0)
    # 回款透析2 = pd.pivot_table(账单合并订单,index=['订单创建日期'],columns = ['实际结算日期'],values=['实际结算金额(元)'],aggfunc = [np.sum])
    # 回款透析2.columns = 回款透析2.columns.droplevel(0)

    回款总表.columns = 回款总表.columns.droplevel(0)
    回款总表.rename(columns={'实际结算金额(元)': '总计金额'}, inplace=True)

    按订单创建日期回款表 = pd.pivot_table(账单合并订单, index=['订单创建日期'], values=['实际结算金额(元)'],
                                          aggfunc=[np.sum])
    按订单创建日期回款表.columns = 按订单创建日期回款表.columns.droplevel(0)
    按订单创建日期回款表.rename(columns={'实际结算金额(元)': '总计金额'}, inplace=True)
    # 提取账单表中所有订单创建日期，从小到大排序【切一条，透析一条，加入一条】
    # 将不同订单创建日期的数据从小到大切割出来，会对应不同的实际结算日期，进行透析（也就是分组求和），按照一定规则加入到新表中

    提取 = 账单合并订单.copy()
    去重 = 账单合并订单.copy()
    去重 = 去重.drop_duplicates('订单创建日期')
    横切用N列表 = 函数_提取日期(去重, '订单创建日期')
    # 排序，从小到大
    横切用N列表.sort()

    for 订单创建日期 in 横切用N列表:
        # 提取某一天执行操作
        横切表 = 提取[(提取['订单创建日期'] == 订单创建日期)]
        # 获取同一个订单日期有几个动账日期
        获取 = 横切表.copy()
        # 去除重复的动账日期
        获取 = 获取.drop_duplicates('实际结算日期')
        # 将实际结算日期提取出来，返回形式为列表
        对应实际结算日期列表 = 函数_提取日期(获取, '实际结算日期')
        # print(对应实际结算日期列表)
        # 再用每一个动账日期减去订单日期，得到一组整数
        数字列表 = 函数_计算日期差值(订单创建日期, 对应实际结算日期列表)

        # 【数据透析表】
        横切透析 = pd.pivot_table(横切表, index=['订单创建日期'], columns=['实际结算日期'], values=['实际结算金额(元)'],
                                  aggfunc=[np.sum])
        # 去除表头sum
        横切透析.columns = 横切透析.columns.droplevel(0)
        # 创造字典，最后再修改字典
        明细字典1 = {f'第{i}天': 0 for i in range(1, 91)}  # range 区间是左闭右开
        # 明细字典2 = {f'第{i+10}天': 0 for i in range(50)}
        # #【数字格式统一化】 01~09 10~30 两位数方便自动列排序
        # 明细字典1.update(明细字典2)
        # 利用整数
        # print(数字列表)
        计数 = 0
        for 天数 in 数字列表:
            # 在字典处定位需修改的地方，修改值为透析表中已经求和好的部分
            if 天数 >= 1:
                求和值 = 横切透析.iloc[0, 计数]
                计数 = 计数 + 1
                明细字典1[f'第{天数}天'] = float(求和值)

        某一天明细 = pd.Series(明细字典1)
        某一天明细.name = 订单创建日期
        # 不断合并统计好的日期
        用于合并 = 用于合并.append(某一天明细)

    用于列顺序维护 = list(明细字典1)
    用于合并 = 用于合并.loc[:, 用于列顺序维护]
    用于合并.index.name = "订单创建日期"

    回款总表.to_excel(r'')
    用于合并.to_excel(r'')
    按订单创建日期回款表.to_excel(r'')

data1 = pd.read_excel(r'')
data2 = pd.read_excel(r'')

天猫账单回款表(data1,data2)

