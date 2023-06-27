
# 读取清洗后的订单表、账单表，输出名称放在备注
# 根据客户-商品关系表对订单表和账单表进行切片
import pandas as pd
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

def 按列提取内容(待去重,列名称):

    去重后 = 待去重.drop_duplicates(f'{列名称}')

    列表 = []
    for i in 去重后.loc[:,f'{列名称}']:
        列表.append(i)
    return 列表

from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog, QWidget
from ui_DivideClient import Ui_Form


class Window(QWidget):

    def __init__(self):
        super().__init__()
        # 使用ui_Clean文件导入界面定义类
        self.ui = Ui_Form()
        self.ui.setupUi(self)  # 传入QWidget对象
        self.ui.retranslateUi(self)

        # 实例变量
        self.客户关系表绝对路径 = ''
        self.清洗后文件夹 = ''
        self.保存文件绝对路径 = ''

        self.temp = ''  # 用于保存打开文件的路径

        self.ui.InputButton_1.clicked.connect(self.getClientRelations)
        self.ui.InputButton_2.clicked.connect(self.getInputDir)
        self.ui.OutputButton.clicked.connect(self.getOutputDir)
        self.ui.RunButton.clicked.connect(self.handel)

    def getClientRelations(self):
        self.temp, _ = QFileDialog.getOpenFileName(self, "选择关系表", '', "Forms(*.xlsx *.csv)")
        if self.temp != '':
            self.客户关系表绝对路径 = self.temp
            self.ui.InputFile_1.setText(self.客户关系表绝对路径)  # 显示路径

    def getInputDir(self):
        self.temp = QFileDialog.getExistingDirectory(self, "选择输入文件夹")
        if self.temp != '':
            self.清洗后文件夹 = self.temp
            self.ui.InputFile_2.setText(self.清洗后文件夹)  # 显示路径

    def getOutputDir(self):
        self.temp = QFileDialog.getExistingDirectory(self, "选择保存路径")  # 使用本地对话框
        # self.temp = QFileDialog.getExistingDirectory(self, "选择保存路径", '', QFileDialog.DontUseNativeDialog)  # 不使用本地对话框，可以查看文件夹内文件
        if self.temp != '':
            self.保存文件绝对路径 = self.temp
            self.ui.OutputDir.setText(self.保存文件绝对路径)

    def handel(self):

        需打开表格名列表 = ['订单表', '账单表']
        # 实例化对象,调用方法
        自动提取文件 = AutoExtractFiles(self.清洗后文件夹, 需打开表格名列表)
        需打开表格字典 = 自动提取文件.handle()
        # 【在前端提前避免一些错误，如空值检测】
        # 输入值为空时
        if self.客户关系表绝对路径 == '':
            QMessageBox.about(self, "报错！", '请选择客户关系表绝对路径')
            return
        if self.清洗后文件夹 == '':
            QMessageBox.about(self, "报错！", '请输入清洗后文件夹')
            return
        if self.保存文件绝对路径 == '':
            QMessageBox.about(self, "报错！", '请选择保存路径')
            return

        客户关系表 = pd.read_excel(self.客户关系表绝对路径,usecols=['商品ID', '客户名称'])
        客户关系表['商品ID'] = 客户关系表['商品ID'].astype(str)

        # 设置两个空的datafrmae是为了抖音两个表格之间做比较时，防止无对象传入
        for k, v in 需打开表格字典.items():
            if k == '订单表':
                data = pd.read_excel(v)
                文件名 = os.path.basename(需打开表格字典[k])  # loose-天猫-账单表-清洗后.xlsx
                文件名前缀 = os.path.splitext(文件名)[0]  # loose-天猫-账单表-清洗后

                data['订单编号'] = data['订单编号'].astype(str)
                data['商品单号'] = data['商品单号'].astype(str)
                data['商品ID'] = data['商品ID'].astype(str)
            elif k == '账单表':
                data = pd.read_excel(v)
                文件名 = os.path.basename(需打开表格字典[k])  # loose-天猫-账单表-清洗后.xlsx
                文件名前缀 = os.path.splitext(文件名)[0]  # loose-天猫-账单表-清洗后

                data['订单编号'] = data['订单编号'].astype(str)
                data['商品单号'] = data['商品单号'].astype(str)
                data['商品ID'] = data['商品ID'].astype(str)

            操作人 = 文件名前缀.split('-')[3]
            表格类型 = 文件名前缀.split('-')[2]
            平台类型 = 文件名前缀.split('-')[1]  # loose-【天猫】-账单表-清洗后
            客户名称 = 文件名前缀.split('-')[0]  # 【loose】-天猫-账单表-清洗后
            原始长度 = len(data)
            累计长度 = 0

            # ——————————————————————————————————————————————【业务逻辑】
            # 先将关系表按客户做切片，然后再循环切片订单表
            去重 = 客户关系表.copy()
            提取 = 客户关系表.copy()
            横切用N列表 = 按列提取内容(去重, '客户名称')

            for 细分客户名称 in 横切用N列表:
                # 按列表的值进行循环切片
                横切表 = 提取[(提取['客户名称'] == 细分客户名称)]
                # 保持商品ID的唯一性再进行合并
                横切表 = 横切表.drop_duplicates('商品ID')
                输出切片 = pd.merge(data, 横切表, how='inner', on='商品ID')
                切片长度 = len(输出切片)

                输出文件名格式 = f'\\{客户名称}-{平台类型}-{表格类型}-{操作人}-{细分客户名称}.xlsx'
                输出路径 = self.保存文件绝对路径 + 输出文件名格式

                累计长度 = 累计长度 + 切片长度

                writer = pd.ExcelWriter(输出路径)
                输出切片.to_excel(writer,index=False)
                writer.save()
                # 不用删掉，不然文件短时间内不能编辑，只能读取
                writer.close()


            # 判断某一个表格是否充分被切分
            if 原始长度 != 累计长度:
                QMessageBox.about(self, "处理结果", f'{表格类型}切分不充分！\n“{原始长度 - 累计长度}”条记录未被识别')
            else:
                QMessageBox.about(self, "处理结果", f'{表格类型}切分成功！\n请于“{self.保存文件绝对路径}”查看结果文件')




if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec_()
