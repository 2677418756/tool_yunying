import pandas as pd
import os

def read_file(path):
    """根据文件扩展名选择读取方法"""
    if path.endswith('.xlsx'):
        return pd.read_excel(path)
    elif path.endswith('.csv'):
        return pd.read_csv(path)
    else:
        raise ValueError("Unsupported file format. Please use .xlsx or .csv.")


def 售后表清洗(path):
    # 根据文件扩展名读取数据集
    data = read_file(path)
    # 将DataFrame中的所有列转换为字符串类型
    data = data.astype(str)
    # 筛选'售后状态'为'退款成功'的行
    data_refund_success = data[data['售后状态'] == '退款成功']
    return data_refund_success

def 账单表清洗(path):
    data = read_file(path)
    # 根据文件扩展名读取数据集
    data = data.astype(str)
    return data

def 订单表清洗(path):
    data=read_file(path)
    data['订单成交时间'] = data['订单成交时间'].str.strip('\t')
    data['订单成交时间'] = pd.to_datetime(data['订单成交时间'])
    data.dropna(subset=['订单成交时间'], inplace=True)
    return data

def 推广表清洗(path):
    # 根据文件扩展名读取数据集
    data = read_file(path)
    # 将DataFrame中的所有列转换为字符串类型
    data = data.astype(str)
    data = data[data['订单状态'] != '推广失败']
    return

if __name__ == '__main__':
    #售后表
    # input_path = r"C:\Users\huanglipan\Desktop\拼多多-MVAV鞋服工厂店\拼多多-MVAV鞋服工厂店\1、源数据\拼多多-售后表.xlsx"
    # cleaned_data = 售后表清洗(input_path)
    # 账单表
    # input_path = r"C:\Users\huanglipan\Desktop\拼多多-MVAV鞋服工厂店\拼多多-MVAV鞋服工厂店\1、源数据\拼多多-账单表.csv"
    # cleaned_data = 账单表清洗(input_path)


    input_path = r"C:\Users\huanglipan\Desktop\拼多多-MVAV鞋服工厂店\拼多多-MVAV鞋服工厂店\1、源数据\拼多多-订单表.csv"
    cleaned_data = 订单表清洗(input_path)
    output_folder = r"C:\Users\huanglipan\Desktop\拼多多-MVAV鞋服工厂店\拼多多-MVAV鞋服工厂店\2、清洗后"
    # 使用os.path.basename获取文件名，不包括路径
    file_name_only = os.path.basename(input_path)
    output_path = os.path.join(output_folder, file_name_only)  # 使用os.path.join更安全地拼接路径
    cleaned_data.to_csv(output_path, index=False)
    # cleaned_data.to_excel(output_path, index=False)
    print(f"清洗后的数据已保存至：{output_path}")

