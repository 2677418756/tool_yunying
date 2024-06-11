from CommonUtil import CommonUtil


def 售后表清洗(路径,文件名):
    # 根据文件扩展名读取数据集
    data = CommonUtil().读取表格(path=路径,name=文件名)
    # 将DataFrame中的所有列转换为字符串类型
    data = data.astype(str)
    # 筛选'售后状态'为'退款成功'的行
    data_refund_success = data[data['售后状态'] == '退款成功']
    return data_refund_success

def 订单表清洗(路径,文件名):
    data =   CommonUtil().读取表格(path=路径,name=文件名)
    # 根据文件扩展名读取数据集
    data = data.astype(str)
    return data

def 账单表清洗(路径,文件名):
    data =  CommonUtil().读取表格(path=路径,name=文件名)
    # 根据文件扩展名读取数据集
    data = data.astype(str)
    return data

def 推广表清洗(路径,文件名):
    # 根据文件扩展名读取数据集
    data =  CommonUtil().读取表格(path=路径,name=文件名)
    # 将DataFrame中的所有列转换为字符串类型
    data = data.astype(str)
    data = data[data['订单状态'] != '推广失败']
    return data

def 拼多多理模块(文件所在位置, 文件名):
    if '订单表' in 文件名:
        return 订单表清洗(文件所在位置,文件名)
    elif '售后表' in 文件名:
        return 售后表清洗(文件所在位置,文件名)
    elif ('佣金表' in 文件名) or ('推广表' in 文件名):
        return 推广表清洗(文件所在位置,文件名)
    elif '账单表' in 文件名:
        return 账单表清洗(文件所在位置,文件名)