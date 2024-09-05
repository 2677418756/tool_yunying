import os
from tkinter import messagebox

import numpy as np
import pandas as pd


def 抖发_函数(订单表):
    订单表['订单应付金额'] = 订单表['订单应付金额'].astype(float)
    抖发 = pd.pivot_table(
        订单表,
        index=['订单创建日期'],
        columns=['发货用时'],
        values=['订单应付金额'],
        aggfunc=[np.sum]
    )

    抖发.columns = 抖发.columns.droplevel(0)
    抖发.columns = 抖发.columns.droplevel(0)
    抖发 = 抖发.reset_index()
    抖发["订单创建日期"] = 抖发["订单创建日期"].apply(lambda x: str(x)[:10])
    抖发 = 抖发.fillna(0)
    return 抖发


def 抖团_函数(订单表):
    订单表_筛选 = 订单表[~订单表.团长.isin(["无"])]
    抖团 = pd.pivot_table(
        订单表_筛选,
        index=['订单创建日期'],
        values=['订单应付金额'],
        aggfunc={'订单应付金额': np.sum}
    )
    抖团.reset_index()

    max_indexes = 订单表_筛选.groupby('订单创建日期')['订单应付金额'].idxmax()
    # 根据找到的索引筛选出对应的行
    抖团_团长 = 订单表_筛选.loc[max_indexes]
    抖团_团长 = 抖团_团长[["订单创建日期", "团长"]]

    抖团 = pd.merge(抖团, 抖团_团长[["订单创建日期", "团长"]], how='left', left_on='订单创建日期',
                    right_on='订单创建日期')
    抖团["订单创建日期"] = 抖团["订单创建日期"].apply(lambda x: str(x)[:10])

    return 抖团


def 抖商_函数(订单表):
    抖商 = pd.pivot_table(
        订单表,
        index=['订单创建日期'],
        values=['订单应付金额'],
        aggfunc={'订单应付金额': np.sum}
    )
    抖商.reset_index()

    max_indexes = 订单表.groupby('订单创建日期')['订单应付金额'].idxmax()
    # 根据找到的索引筛选出对应的行
    抖商_商品 = 订单表.loc[max_indexes]
    抖商_商品 = 抖商_商品[["订单创建日期", "商品编码"]]

    抖商 = pd.merge(抖商, 抖商_商品[["订单创建日期", "商品编码"]], how='left', left_on='订单创建日期',
                    right_on='订单创建日期')
    抖商["订单创建日期"] = 抖商["订单创建日期"].apply(lambda x: str(x)[:10])
    抖商.rename(columns={'商品编码': '款号'}, inplace=True)
    return 抖商


def dy_chuli(path,sku_path):
    shop_name = str(path).split("-")[1]
    files = os.listdir(path + "/2、清洗后")
    for file in files:
        if "订单表" in file:
            订单表 = pd.read_excel(path + "/2、清洗后/" + file, dtype=str)
            订单表["商家编码"] = 订单表["商家编码"].apply(lambda x:str(x).strip().replace("\t",""))
        elif "售后表" in file:
            售后表 = pd.read_excel(path + "/2、清洗后/" + file, dtype=str)
        elif "运单表" in file:
            运单表 = pd.read_excel(path + "/2、清洗后/" + file, dtype=str)
        elif "团长表" in file:
            团长表 = pd.read_excel(path + "/2、清洗后/" + file, dtype=str)

    files = os.listdir(path + "/3、中台表格")
    for file in files:
        if "订单金额表" in file:
            订单金额表 = pd.read_excel(path + "/3、中台表格/" + file, dtype=str)
        elif "订单成本金额表" in file:
            订单成本金额表 = pd.read_excel(path + "/3、中台表格/" + file, dtype=str)

    sku_file = pd.read_excel(sku_path, dtype=str)

    # ①售后类型
    售后表_合并 = pd.merge(订单表, 售后表[["订单编号", "售后类型"]], how='left', left_on='订单编号',
                           right_on='订单编号')
    售后表_合并["售后类型"] = 售后表_合并["售后类型"].fillna(0)
    订单表["售后类型"] = 售后表_合并["售后类型"]
    # ①抖订【辰丰】
    # 发货时间
    运单表_合并 = pd.merge(订单表, 运单表[["订单编号", "揽件日期"]], how='left', left_on='订单编号',
                           right_on='订单编号')
    运单表_合并["揽件日期"] = 运单表_合并["揽件日期"].fillna("未发货")
    订单表["发货时间"] = 运单表_合并["揽件日期"].apply(lambda x: x[:10])

    # 发货用时
    订单表_已发货 = 订单表[~订单表.发货时间.isin(["未发货"])]
    订单表_已发货["发货时间"] = pd.to_datetime(订单表_已发货["发货时间"])
    订单表_已发货["订单创建日期"] = pd.to_datetime(订单表_已发货["订单创建日期"])
    订单表_已发货["发货用时"] = 订单表_已发货["发货时间"] - 订单表_已发货["订单创建日期"]
    订单表_已发货["发货用时"] = 订单表_已发货["发货用时"].apply(lambda x: int(str(x).split(" ")[0]))
    订单表_已发货['发货用时'] = np.where(订单表_已发货.发货用时 > 7, "7天以上", 订单表_已发货.发货用时)
    订单表 = pd.merge(订单表, 订单表_已发货[["订单编号", "发货用时"]], how='left', left_on='订单编号',
                      right_on='订单编号')
    订单表["发货用时"] = 订单表["发货用时"].fillna("未发货")

    # 团长
    团长表_合并 = pd.merge(订单表, 团长表[["商品单号", "出单机构"]], how='left', left_on='商品单号',
                           right_on='商品单号')
    团长表_合并["出单机构"] = 团长表_合并["出单机构"].fillna("无")
    订单表["团长"] = 团长表_合并["出单机构"]

    # 商品匹配
    订单表 = pd.merge(订单表, sku_file[["规格编码", "商品编码"]], how='left', left_on='商家编码',
                           right_on='规格编码')

    # ②抖发
    订单表_筛选 = 订单表[~订单表.售后类型.isin(['未发货仅退款'])]
    抖发 = 抖发_函数(订单表_筛选)

    # ②抖团
    抖团 = 抖团_函数(订单表_筛选)

    # ②抖商
    抖商 = 抖商_函数(订单表_筛选)

    抖团 = pd.merge(抖团, 抖商[["订单创建日期", "款号"]], how='left', left_on='订单创建日期',
                           right_on='订单创建日期')
    订单成本金额表["联盟佣金"] = 订单成本金额表["联盟佣金"].astype(float)
    订单成本金额表["团长佣金"] = 订单成本金额表["团长佣金"].astype(float)
    订单成本金额表["总佣金"] = 订单成本金额表["联盟佣金"] + 订单成本金额表["团长佣金"]

    订单金额表["平台"] = "抖音"

    return table_calculate(抖发, 抖团, 订单成本金额表, 订单金额表, shop_name)


def ks_chuli(path,sku_path):
    shop_name = str(path).split("-")[1]
    files = os.listdir(path + "/1、源文件")
    for file in files:
        if "订单表" in file:
            if ".xlsx" in file:
                原订单表 = pd.read_excel(path + "/1、源文件/" + file, dtype=str)
            elif ".csv" in file:
                原订单表 = pd.read_csv(path + "/1、源文件/" + file, dtype=str)

    files = os.listdir(path + "/2、清洗后")
    for file in files:
        if "订单表" in file:
            订单表 = pd.read_excel(path + "/2、清洗后/" + file, dtype=str)
        elif "售后表" in file:
            售后表 = pd.read_excel(path + "/2、清洗后/" + file, dtype=str)

    files = os.listdir(path + "/3、中台表格")
    for file in files:
        if "订单金额表" in file:
            订单金额表 = pd.read_excel(path + "/3、中台表格/" + file, dtype=str)
        elif "订单成本金额表" in file:
            订单成本金额表 = pd.read_excel(path + "/3、中台表格/" + file, dtype=str)

    sku_file = pd.read_excel(sku_path, dtype=str)

    # ①【快手（MVAV辰名店）】
    # 售后类型
    售后表_合并 = pd.merge(订单表, 售后表[["订单编号", "售后类型"]], how='left', left_on='订单编号',
                           right_on='订单编号')
    售后表_合并["售后类型"] = 售后表_合并["售后类型"].fillna(0)
    订单表["售后类型"] = 售后表_合并["售后类型"]

    # 发货时间
    订单表["发货时间"] = "未发货"
    订单表['发货时间'] = np.where(订单表.发货日期.isna(), 订单表.发货时间, 订单表.发货日期)
    订单表['发货时间'] = 订单表['发货时间'].apply(lambda x: str(x)[:10])

    # 发货用时
    订单表_已发货 = 订单表[~订单表.发货时间.isin(["未发货"])]
    订单表_已发货["发货时间"] = pd.to_datetime(订单表_已发货["发货时间"])
    订单表_已发货["订单创建日期"] = pd.to_datetime(订单表_已发货["订单创建日期"])
    订单表_已发货["发货用时"] = 订单表_已发货["发货时间"] - 订单表_已发货["订单创建日期"]
    订单表_已发货["发货用时"] = 订单表_已发货["发货用时"].apply(lambda x: int(str(x).split(" ")[0]))
    订单表_已发货['发货用时'] = np.where(订单表_已发货.发货用时 > 7, "7天以上", 订单表_已发货.发货用时)
    订单表 = pd.merge(订单表, 订单表_已发货[["订单编号", "发货用时"]], how='left', left_on='订单编号',
                      right_on='订单编号')
    订单表["发货用时"] = 订单表["发货用时"].fillna("未发货")

    # 团长
    订单表 = pd.merge(订单表, 原订单表[["订单号", "团长昵称"]], how='left', left_on='订单编号',
                      right_on='订单号')
    订单表.rename(columns={'团长昵称': '团长'}, inplace=True)

    # 商品匹配
    订单表 = pd.merge(订单表, sku_file[["规格编码", "商品编码"]], how='left', left_on='商家编码',
                           right_on='规格编码')

    # ②快发
    订单表_筛选 = 订单表[~订单表.售后类型.isin(['仅退款'])]
    快发 = 抖发_函数(订单表_筛选)

    # ②快团
    快团 = 抖团_函数(订单表_筛选)

    # ②快商
    快商 = 抖商_函数(订单表_筛选)

    快团 = pd.merge(快团, 快商[["订单创建日期", "款号"]], how='left', left_on='订单创建日期',
                           right_on='订单创建日期')

    订单成本金额表["剩余销售金额"] = 订单成本金额表["剩余销售金额"].astype(float)
    订单成本金额表["总佣金"] = 订单成本金额表["剩余销售金额"] * 0.4
    订单成本金额表["平台扣点"] = 订单成本金额表["剩余销售金额"] * 0.05

    订单金额表["平台"] = "快手"

    return table_calculate(快发, 快团, 订单成本金额表, 订单金额表, shop_name)


def table_calculate(抖发, 抖团, 订单成本金额表, 订单金额表, shop_name):
    # ③【抖订单金额】

    订单金额表 = pd.merge(订单金额表, 订单成本金额表[["订单创建日期", "总佣金", "平台扣点"]], how='left',
                          left_on='订单创建日期', right_on='订单创建日期')
    订单金额表["总佣金"] = 订单金额表["总佣金"].fillna(0)
    订单金额表["平台扣点"] = 订单金额表["平台扣点"].fillna(0)

    info = ["0", "1", "2", "3", "4", "5", "6", "7", "7天以上", "未发货"]
    for i in info:
        try:
            抖发[i] = 抖发[i]
        except:
            抖发[i] = 0

    订单金额表 = pd.merge(订单金额表,
                          抖发[["订单创建日期", "0", "1", "2", "3", "4", "5", "6", "7", "7天以上", "未发货"]],
                          how='left',
                          left_on='订单创建日期', right_on='订单创建日期')
    订单金额表 = pd.merge(订单金额表, 抖团[["订单创建日期","团长","款号"]], how='left', left_on='订单创建日期',
                          right_on='订单创建日期')
    订单金额表["团长"] = 订单金额表["团长"].fillna(0)
    订单金额表["款号"] = 订单金额表["款号"].fillna(0)
    订单金额表 = 订单金额表.fillna(0)
    # 订单金额表["0"] = 抖发["0"]

    订单金额表["店铺"] = shop_name
    订单金额表["发货总金额"] = 订单金额表["0"] + 订单金额表["1"] + 订单金额表["2"] + 订单金额表["3"] + 订单金额表["4"] + \
                               订单金额表["5"] + 订单金额表["6"] + 订单金额表["7"] + 订单金额表["7天以上"] + 订单金额表[
                                   "未发货"]
    订单金额表.rename(columns={'订单创建日期': '销售日期'}, inplace=True)
    订单金额表.rename(columns={'订单应付金额': '销售金额'}, inplace=True)
    订单金额表.rename(columns={'团长': '商务'}, inplace=True)
    订单金额表.rename(columns={'总佣金': '佣金金额'}, inplace=True)
    订单金额表.rename(columns={'平台扣点': '其他费用'}, inplace=True)
    订单金额表.rename(columns={'0': '当日发货'}, inplace=True)
    订单金额表.rename(columns={'1': '第一天发货'}, inplace=True)
    订单金额表.rename(columns={'2': '第二天发货'}, inplace=True)
    订单金额表.rename(columns={'3': '第三天发货'}, inplace=True)
    订单金额表.rename(columns={'4': '第四天发货'}, inplace=True)
    订单金额表.rename(columns={'5': '第五天发货'}, inplace=True)
    订单金额表.rename(columns={'6': '第六天发货'}, inplace=True)
    订单金额表.rename(columns={'7': '第七天发货'}, inplace=True)
    订单金额表.rename(columns={'未发货': '待发货金额'}, inplace=True)
    订单金额表["销售金额"] = 订单金额表["销售金额"].astype(float)
    订单金额表["退款金额"] = 订单金额表["退款金额"].astype(float)
    订单金额表["退货金额"] = 订单金额表["退货金额"].astype(float)
    订单金额表["佣金金额"] = 订单金额表["佣金金额"].astype(float)
    订单金额表["其他费用"] = 订单金额表["其他费用"].astype(float)
    订单金额表["实际成交金额"] = 订单金额表["销售金额"] - 订单金额表["退款金额"] - 订单金额表["退货金额"]
    订单金额表["平台预估结算金额"] = 订单金额表["实际成交金额"] - 订单金额表["佣金金额"] - 订单金额表["其他费用"]

    return 订单金额表[
        ["平台", "店铺", "销售日期", "商务", "款号", "销售金额", "退款金额", "退货金额", "实际成交金额", "佣金金额",
         "其他费用", "平台预估结算金额", "发货总金额", "当日发货", "第一天发货", "第二天发货", "第三天发货",
         "第四天发货", "第五天发货", "第六天发货", "第七天发货", "7天以上", "待发货金额"]
    ]


def generate_table(path_list,sku_path, output_path, out_filename):

    table_list = []
    for path in path_list:
        if path == "":
            continue
        平台 = str(path).split("/")[-1].split("-")[0]
        if 平台 != "抖音" and 平台 != "快手":
            messagebox.showinfo("提示", "第" + str(path_list.index(path) + 1) + "个路径选择有误")
            return

    for path in path_list:
        if path == "":
            continue
        平台 = str(path).split("/")[-1].split("-")[0]
        if 平台 == "抖音":
            table_list.append(dy_chuli(path,sku_path))
        elif 平台 == "快手":
            table_list.append(ks_chuli(path,sku_path))


    终表 = pd.concat(table_list)

    终表.to_excel(output_path+"/"+out_filename+".xlsx",index=False)


    messagebox.showinfo("提示", "已完成！")


if __name__ == "__main__":
    import main
