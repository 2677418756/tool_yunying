# -*- coding: utf-8 -*-
"""
Created on Tue May 17 16:54:21 2022

@author: Admin
"""

from Creat_Statistic_Change import Create
from Special_Statistic import Maintain
from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog, QWidget
from ui_StaticalBill import Ui_Form


class Window(QWidget):

    def __init__(self):
        super().__init__()
        # 使用ui_Clean文件导入界面定义类
        self.ui = Ui_Form()
        self.ui.setupUi(self)  # 传入QWidget对象
        self.ui.retranslateUi(self)

        # 实例变量
        # 创建Tab实例
        self.C = Create('', '', '', '', '')
        self.M = Maintain('', '', '', '', '')

        # TabCreate的变量
        self.C_昨日计费表文件绝对路径 = ''
        self.C_中台文件夹绝对路径 = ''
        self.C_输出至文件夹 = ''
        self.C_当天日期 = ''  # 本质是订单创建日期 格式：2022-01-30
        self.C_操作人 = ''
        # TabMaintain的变量
        self.M_今日计费表文件绝对路径 = ''
        self.M_特殊回款表绝对路径 = ''
        self.M_输出至文件夹 = ''
        self.M_当天日期 = ''  # r'2022-02-12' #本质是订单创建日期 格式：2022-01-30
        self.M_操作人 = ''

        # 读取文件（夹）辅助变量
        self.temp = ''

        # 按钮功能
        # TabCreate
        self.ui.C_InputButton_1.clicked.connect(self.C_getStaticForm)
        self.ui.C_InputButton_2.clicked.connect(self.C_getMidDir)
        self.ui.C_OutputButton.clicked.connect(self.C_getOutputDir)
        self.ui.C_RunButton.clicked.connect(self.C_handle)

        # TabMaintain
        self.ui.M_InputButton_1.clicked.connect(self.M_getStaticForm)
        self.ui.M_InputButton_2.clicked.connect(self.M_getMSpecialForm)
        self.ui.M_OutputButton.clicked.connect(self.M_getOutputDir)
        self.ui.M_RunButton.clicked.connect(self.M_handle)

    # TabCreate的函数----------------------------------------------------
    def C_getStaticForm(self):
        self.temp, _ = QFileDialog.getOpenFileName(self, "选择昨日计费表", '', "Forms(*.xlsx *.csv)")  # 使用本地对话框
        if self.temp != '':
            self.C_昨日计费表文件绝对路径 = self.temp
            self.ui.C_InputFile_1.setText(self.C_昨日计费表文件绝对路径)  # 显示路径

    def C_getMidDir(self):
        self.temp = QFileDialog.getExistingDirectory(self, "选择中台文件夹")
        if self.temp != '':
            self.C_中台文件夹绝对路径 = self.temp
            self.ui.C_InputFile_2.setText(self.C_中台文件夹绝对路径)

    def C_getOutputDir(self):
        self.temp = QFileDialog.getExistingDirectory(self, "选择保存路径")  # 使用本地对话框
        if self.temp != '':
            self.C_输出至文件夹 = self.temp
            self.ui.C_OutputDir.setText(self.C_输出至文件夹)

    def C_handle(self):
        self.C_操作人 = self.ui.C_User.text()
        self.C_当天日期 = self.ui.C_Date.text()  # 本质是订单创建日期 格式：2022-01-30
        # 输入值为空时
        if self.C_昨日计费表文件绝对路径 == '':
            QMessageBox.about(self, "报错！", '请选择昨日计费表')
            return
        if self.C_中台文件夹绝对路径 == '':
            QMessageBox.about(self, "报错！", '请选择台文件夹')
            return
        if self.C_输出至文件夹 == '':
            QMessageBox.about(self, "报错！", '请选择保存路径')
            return
        if self.C_操作人 == '':
            QMessageBox.about(self, "报错！", '请输入操作人')
            return
        if self.C_当天日期 == '':
            QMessageBox.about(self, "报错！", '请输入日期')
            return
        self.C.__init__(self.C_昨日计费表文件绝对路径, self.C_中台文件夹绝对路径, self.C_输出至文件夹,
                        self.C_操作人, self.C_当天日期)
        self.C.create(self)
    # -------------------------------------------------------------

    # TabMaintain的函数---------------------------------------------
    def M_getStaticForm(self):
        self.temp, _ = QFileDialog.getOpenFileName(self, "选择今日计费表", '', "Forms(*.xlsx *.csv)")  # 使用本地对话框
        if self.temp != '':
            self.M_今日计费表文件绝对路径 = self.temp
            self.ui.M_InputFile_1.setText(self.M_今日计费表文件绝对路径)  # 显示路径

    def M_getMSpecialForm(self):
        self.temp, _ = QFileDialog.getOpenFileName(self, "选择特殊回款表", '', "Forms(*.xlsx *.csv)")  # 使用本地对话框
        if self.temp != '':
            self.M_特殊回款表绝对路径 = self.temp
            self.ui.M_InputFile_2.setText(self.M_特殊回款表绝对路径)

    def M_getOutputDir(self):
        self.temp = QFileDialog.getExistingDirectory(self, "选择保存路径")  # 使用本地对话框
        if self.temp != '':
            self.M_输出至文件夹 = self.temp
            self.ui.M_OutputDir.setText(self.M_输出至文件夹)

    def M_handle(self):
        self.M_操作人 = self.ui.M_User.text()
        self.M_当天日期 = self.ui.M_Date.text()  # 本质是订单创建日期 格式：2022-01-30
        # 输入值为空时
        if self.M_今日计费表文件绝对路径 == '':
            QMessageBox.about(self, "报错！", '请选择今日计费表')
            return
        if self.M_特殊回款表绝对路径 == '':
            QMessageBox.about(self, "报错！", '请选择特殊回款表')
            return
        if self.M_输出至文件夹 == '':
            QMessageBox.about(self, "报错！", '请选择保存路径')
            return
        if self.M_操作人 == '':
            QMessageBox.about(self, "报错！", '请输入操作人')
            return
        if self.M_当天日期 == '':
            QMessageBox.about(self, "报错！", '请输入日期')
            return
        self.M.__init__(self.M_今日计费表文件绝对路径, self.M_特殊回款表绝对路径, self.M_输出至文件夹,
                        self.M_操作人, self.M_当天日期)
        self.M.maintain(self)

    # -------------------------------------------------------------


if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec_()