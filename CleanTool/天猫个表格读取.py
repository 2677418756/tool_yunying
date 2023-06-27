import pandas as pd
import warnings
warnings.filterwarnings('ignore')

文件所在位置 = r'C:\Users\Wind_Aleady_Here\Desktop\给毅华的打包文件夹\天猫-账单表.xlsx'
输出位置 = r'C:\Users\Wind_Aleady_Here\Desktop\给毅华的打包文件夹\天猫-账单表清洗后.xlsx'
# data = pd.read_excel(文件所在位置,usecols=['主订单编号','子订单编号','买家应付货款','标题','订单状态','订单创建时间','物流单号','物流公司','购买数量','退款状态','发货时间'])

data = pd.DataFrame()

for i in range(1, 8):
    """
    1、外层选择用try把未知数量的sheet分别打开再合并
    2、if语句用于将第一个sheet中的无关信息读取时忽略掉
    """
    try:
        if i == 1:
            # 为了删除前两行的无关信息，所以header=2
            temp_data = pd.read_excel(文件所在位置, sheet_name=f'账务组合查询{i}', header=2,
                                      usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
            col_name = temp_data.columns.tolist()  # 提取表头城列表
        else:
            temp_data = pd.read_excel(文件所在位置, sheet_name=f'账务组合查询{i}', header=None,
                                      usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
            temp_data.columns = col_name  # 为其他sheet添加表头
        data = pd.concat([data, temp_data], axis=0, ignore_index=True)
    except:
        # 打开完所有的sheet后会跳转到此2语句，跳出循环
        break



data.reset_index(inplace=True, drop=True)
# 干掉最后一行垃圾数据
data.drop([len(data) - 1], inplace=True)

data.to_excel(输出位置,index=False)

# 清空前后字符串
data['业务描述'] = data['业务描述'].str.strip()
data['业务描述'] = data['业务描述'].astype(str)

# 格式转换
data['入账时间'] = data['入账时间'].astype('datetime64[ns]')
data['实际结算日期'] = pd.to_datetime(data['入账时间'])
data['实际结算日期'] = data['实际结算日期'].dt.date

# 清空前后字符串
data['收入（+元）'] = data['收入（+元）'].str.strip()
data['支出（-元）'] = data['支出（-元）'].str.strip()
# data['服务费（元）'] = data['服务费（元）'].str.strip()
# 清除字符串后才能将空值填充
data['收入（+元）'] = data['收入（+元）'].replace('', '0')
data['支出（-元）'] = data['支出（-元）'].replace('', '0')
data['服务费（元）'] = data['服务费（元）'].replace('', '0')
# 将字符串转换为可以计算的float类型
data['收入（+元）'] = data['收入（+元）'].astype(float)
data['支出（-元）'] = data['支出（-元）'].astype(float)
data['服务费（元）'] = data['服务费（元）'].astype(float)

# 先删除收费，因为想要订单本身
data = data[~data.账务类型.isin(['收费'])]
# 在筛选其中需要的行数据
data1 = data[(data.业务描述.isin(['']))]
data2 = data[~(data.业务描述.isin(['']))]

# 先对业务描述列进行空值处理
data1['业务描述'] = data1['业务描述'].str.replace('', '无描述')
# 筛选无业务描述的，无业务描述中：在线支付大于0的，转账中转给官方的，其他中全部
data1 = data1[data1.账务类型.isin(['转账', '其它', '在线支付'])]
data1 = data1[~(data1.账务类型.isin(['在线支付']) & data1['收入（+元）'].isin([0]))]
data1 = data1[~(data1.账务类型.isin(['转账']) & ~(data1.对方名称.isin(
    ['阿里巴巴华南技术有限公司广东第一分公司', '浙江天猫技术有限公司', '杭州阿里妈妈软件服务有限公司',
     '阿里巴巴华南技术有限公司'])))]
data1 = data1[~(data1.账务类型.isin(['其它']) & ~(data1.备注.isin(['网商贷-放款', '网商贷-还款'])))]
# #筛选有业务描述的
# data2 = data2[~(data2.账务类型.isin(['退款（交易退款）']))]
# 合并
data = pd.concat([data1, data2])
data.reset_index(inplace=True, drop=True)

# 运算
data['实际结算金额(元)'] = data['收入（+元）'] - data['支出（-元）'] - data['服务费（元）']

# 统一字段名称
data.rename(columns={'业务基础订单号': '订单编号'}, inplace=True)


# # 主订单编号使用replace去除=与""
# data['主订单编号'] = data['主订单编号'].astype(str)
# data['主订单编号'] = data['主订单编号'].str.replace('=', '')
# data['主订单编号'] = data['主订单编号'].str.replace('"', '')
# # 子订单编号使用replace去除=与""
# data['子订单编号'] = data['子订单编号'].astype(str)
# data['子订单编号'] = data['子订单编号'].str.replace('=', '')
# data['子订单编号'] = data['子订单编号'].str.replace('"', '')
#
#
# # 数据的某一列=数据的某一列进行格式转换，来达成清除前后空格
# data['订单创建时间'] = data['订单创建时间'].astype('datetime64[ns]')
# data['发货时间'] = data['发货时间'].astype('datetime64[ns]')
#
# data['订单创建日期'] = pd.to_datetime(data['订单创建时间'])
# data['订单创建日期'] = data['订单创建日期'].dt.date
#
# data['发货日期'] = pd.to_datetime(data['发货时间'])
# data['发货日期'] = data['发货日期'].dt.date
#
# # #统一字段的名称
# data.rename(columns={'物流单号 ': '运单号'}, inplace=True)
# data.rename(columns={'购买数量': '成交数量'}, inplace=True)
# data.rename(columns={'买家应付货款': '订单应付金额'}, inplace=True)
# # data.rename(columns={'退款金额': '退货退款金额'}, inplace=True)
# data.rename(columns={'退款状态': '售后状态'}, inplace=True)
# data.rename(columns={'标题 ': '商品名称'}, inplace=True)