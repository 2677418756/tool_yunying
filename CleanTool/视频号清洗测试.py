import pandas as pd


def 订单流水表():
    data = pd.read_excel("D:/work/运营/视频号/视频号-MVAV鞋服工厂店/1、源文件/视频号-订单流水表.xlsx", usecols=["订单号", "下单时间", "结算状态", "实付款", "商家结算", "商家结算状态",
                                                "商家结算时间", "技术服务费", "技术服务费结算状态", "退款",
                                                "运费险补贴", "运费险补贴发放状态", "支出服务项"], dtype=str)

    data["商家结算"] = data["商家结算"].apply(lambda x: float(str(x).replace("¥", "").replace("-", "")))
    data["技术服务费"] = data["技术服务费"].apply(lambda x: float(str(x).replace("¥", "").replace("-", "")))
    data["退款"] = data["退款"].apply(lambda x: float(str(x).replace("¥", "").replace("-", "")))
    data["运费险补贴"] = data["运费险补贴"].apply(lambda x: float(str(x).replace("¥", "").replace("-", "")))
    data["支出服务项"] = data["支出服务项"].apply(lambda x: str(x).replace("¥", "").replace("-", ""))
    data["实付款"] = data["实付款"].apply(lambda x: float(str(x).replace("¥", "").replace("-", "")))

    data["支出服务项_用于分割"] = data["支出服务项"] + "））"
    data["达人"] = data["支出服务项_用于分割"].apply(lambda x: str(x).split("）")[0])
    data["团长"] = data["支出服务项_用于分割"].apply(lambda x: str(x).split("）")[1])

    data["达人"] = data["达人"].apply(lambda x: str(x).replace("运费险保费：","").replace("，状态：","").replace("运费险补缴：",""))
    data["团长"] = data["团长"].apply(lambda x: str(x).replace("运费险保费：","").replace("，状态：","").replace("运费险补缴：",""))

    data["达人"] = data["达人"] + "：，0，"
    data["团长"] = data["团长"] + "：，0，"

    data["达人名称"] = data["达人"].apply(lambda x: str(x)[str(x).index("：") + 1:str(x).index("，")])
    data["达人佣金"] = data["达人"].apply(lambda x: float(str(x).split("，")[1].replace("-", "")))
    data["团长名称"] = data["团长"].apply(lambda x: str(x)[str(x).index("：") + 1:str(x).index("，")])
    data["团长佣金"] = data["团长"].apply(lambda x: float(str(x).split("，")[1].replace("-", "")))

    data.rename(columns={'商家结算': '实际结算金额'}, inplace=True)
    data = data.drop(['团长','达人','支出服务项_用于分割'], axis=1)
    data = data.set_index("订单号")


    data.to_excel("D:/work/运营/视频号/视频号-MVAV鞋服工厂店/2、清洗后/MVAV鞋服工厂店-视频号-订单流水表-aaa-无备注.xlsx")


def 售后表():
    data = pd.read_excel("D:/work/运营/视频号/视频号-MVAV鞋服工厂店/1、源文件/视频号-售后表.xlsx",
                         usecols=["售后单号","售后申请时间","订单编号","发货状态","商品名称","商品价格","购买数量","实付款","退款类型","退款金额","退款状态"], dtype=str)

    data = data[~data.退款状态.isin(["已取消"])]
    data["商品价格"] = data["商品价格"].apply(lambda x:float(str(x).replace("¥","")))
    data["退款金额"] = data["退款金额"].apply(lambda x:float(str(x).replace("¥","")))
    data["售后申请日期"] = data["售后申请时间"].apply(lambda x:str(x)[:10])
    data = data.set_index("售后单号")
    data["购买数量"] = data["购买数量"].astype(float)
    data["实付款"] = data["实付款"].astype(float)

    data.to_excel("D:/work/运营/视频号/视频号-MVAV鞋服工厂店/2、清洗后/MVAV鞋服工厂店-视频号-售后表-aaa-无备注.xlsx")


def 账单表():
    data = pd.read_excel("D:/work/运营/视频号/视频号-MVAV鞋服工厂店/1、源文件/视频号-售后表.xlsx",
                         usecols=["售后单号", "售后申请时间", "订单编号", "发货状态", "商品名称", "商品价格",
                                  "购买数量", "实付款", "退款类型", "退款金额", "退款状态"], dtype=str)
    data.to_excel("D:/work/运营/视频号/视频号-MVAV鞋服工厂店/2、清洗后/MVAV鞋服工厂店-视频号-售后表-aaa-无备注.xlsx")


if __name__ =="__main__":
    订单流水表()