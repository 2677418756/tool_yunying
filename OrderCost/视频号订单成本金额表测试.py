import numpy as np
import pandas as pd


def 订单成本金额表测试():
    订单表 = pd.read_excel("D:/work/运营/视频号/视频号-MVAV鞋服工厂店/2、清洗后/MVAV鞋服工厂店-视频号-订单表-a-无备注.xlsx",dtype=str)
    售后表 = pd.read_excel("D:/work/运营/视频号/视频号-MVAV鞋服工厂店/2、清洗后/MVAV鞋服工厂店-视频号-售后表-a-无备注.xlsx",dtype=str)
    订单流水表 = pd.read_excel("D:/work/运营/视频号/视频号-MVAV鞋服工厂店/2、清洗后/MVAV鞋服工厂店-视频号-订单流水表-a-无备注.xlsx",dtype=str)


    合并 = pd.merge(订单表[["订单号","订单创建日期","订单实际支付金额","商品数量"]],售后表[["订单编号","退款金额"]],left_on ='订单号',right_on ='订单编号',how ='left')
    合并 = pd.merge(合并,订单流水表[["订单号","达人佣金","团长佣金"]],left_on ='订单号',right_on ='订单号',how ='left')
    合并 = 合并.fillna(0)
    合并[["订单实际支付金额","退款金额","商品数量","达人佣金","团长佣金"]] = 合并[["订单实际支付金额","退款金额","商品数量","达人佣金","团长佣金"]].astype(float)
    合并["剩余销售金额"] = 合并["订单实际支付金额"] - 合并["退款金额"]
    处理 = pd.pivot_table(
        合并,
        index='订单创建日期',
        values=['剩余销售金额', '达人佣金', '团长佣金', '商品数量','订单实际支付金额'],
        aggfunc={'剩余销售金额': np.sum, '达人佣金': np.sum, '团长佣金': np.sum, '商品数量': np.sum,'订单实际支付金额': np.sum}
    )
    处理 = 处理.reset_index()
    处理["商品数量"] = 处理["商品数量"] * 6
    处理.rename(columns={'商品数量': '运费'}, inplace=True)
    处理.rename(columns={'达人佣金': '联盟佣金'}, inplace=True)
    处理["资金成本"] = 处理["订单实际支付金额"] * 0.05
    处理["平台扣点"] = 处理["剩余销售金额"] * 0.06

    处理 = 处理[["订单创建日期","剩余销售金额","联盟佣金","团长佣金","运费","资金成本","平台扣点"]]

    合并.to_excel("D:/test.xlsx")
    处理.to_excel("D:/test1.xlsx")







if __name__ == "__main__":
    订单成本金额表测试()


