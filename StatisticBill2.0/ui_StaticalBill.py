# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'StaticalBill.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.setEnabled(True)
        Form.resize(800, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(667, 400))
        Form.setMaximumSize(QSize(2200, 1400))
        Form.setAcceptDrops(False)
        Form.setLayoutDirection(Qt.LeftToRight)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(7)
        self.gridLayout.setContentsMargins(30, 30, 30, 30)
        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName(u"tabWidget")
        self.TabCreate = QWidget()
        self.TabCreate.setObjectName(u"TabCreate")
        self.gridLayout_2 = QGridLayout(self.TabCreate)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 0, -1, 5)
        self.label = QLabel(self.TabCreate)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_4)

        self.label_3 = QLabel(self.TabCreate)
        self.label_3.setObjectName(u"label_3")
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_3)

        self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.label_2 = QLabel(self.TabCreate)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_2)

        self.verticalLayout_3.setStretch(0, 20)
        self.verticalLayout_3.setStretch(1, 1)
        self.verticalLayout_3.setStretch(2, 20)
        self.verticalLayout_3.setStretch(3, 2)
        self.verticalLayout_3.setStretch(4, 20)

        self.gridLayout_2.addLayout(self.verticalLayout_3, 0, 0, 3, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(7)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 20, -1, 20)
        self.C_InputFile_1 = QLineEdit(self.TabCreate)
        self.C_InputFile_1.setObjectName(u"C_InputFile_1")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.C_InputFile_1.sizePolicy().hasHeightForWidth())
        self.C_InputFile_1.setSizePolicy(sizePolicy1)
        self.C_InputFile_1.setReadOnly(True)

        self.horizontalLayout.addWidget(self.C_InputFile_1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.C_InputButton_1 = QPushButton(self.TabCreate)
        self.C_InputButton_1.setObjectName(u"C_InputButton_1")
        sizePolicy.setHeightForWidth(self.C_InputButton_1.sizePolicy().hasHeightForWidth())
        self.C_InputButton_1.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.C_InputButton_1)

        self.horizontalLayout.setStretch(0, 11)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 4)

        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 1, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 20, -1, 20)
        self.C_InputFile_2 = QLineEdit(self.TabCreate)
        self.C_InputFile_2.setObjectName(u"C_InputFile_2")
        sizePolicy1.setHeightForWidth(self.C_InputFile_2.sizePolicy().hasHeightForWidth())
        self.C_InputFile_2.setSizePolicy(sizePolicy1)
        self.C_InputFile_2.setReadOnly(True)

        self.horizontalLayout_3.addWidget(self.C_InputFile_2)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        self.C_InputButton_2 = QPushButton(self.TabCreate)
        self.C_InputButton_2.setObjectName(u"C_InputButton_2")
        sizePolicy.setHeightForWidth(self.C_InputButton_2.sizePolicy().hasHeightForWidth())
        self.C_InputButton_2.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.C_InputButton_2)

        self.horizontalLayout_3.setStretch(0, 11)
        self.horizontalLayout_3.setStretch(1, 1)
        self.horizontalLayout_3.setStretch(2, 4)

        self.gridLayout_2.addLayout(self.horizontalLayout_3, 1, 1, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 20, -1, 20)
        self.C_OutputDir = QLineEdit(self.TabCreate)
        self.C_OutputDir.setObjectName(u"C_OutputDir")
        sizePolicy1.setHeightForWidth(self.C_OutputDir.sizePolicy().hasHeightForWidth())
        self.C_OutputDir.setSizePolicy(sizePolicy1)
        self.C_OutputDir.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.C_OutputDir)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.C_OutputButton = QPushButton(self.TabCreate)
        self.C_OutputButton.setObjectName(u"C_OutputButton")
        sizePolicy.setHeightForWidth(self.C_OutputButton.sizePolicy().hasHeightForWidth())
        self.C_OutputButton.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.C_OutputButton)

        self.horizontalLayout_2.setStretch(0, 11)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 4)

        self.gridLayout_2.addLayout(self.horizontalLayout_2, 2, 1, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, 20, -1, 20)
        self.label_4 = QLabel(self.TabCreate)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.label_4)

        self.C_User = QLineEdit(self.TabCreate)
        self.C_User.setObjectName(u"C_User")
        sizePolicy1.setHeightForWidth(self.C_User.sizePolicy().hasHeightForWidth())
        self.C_User.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.C_User)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_6)

        self.label_5 = QLabel(self.TabCreate)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.label_5)

        self.C_Date = QDateEdit(self.TabCreate)
        self.C_Date.setObjectName(u"C_Date")
        self.C_Date.setDateTime(QDateTime(QDate(2022, 5, 1), QTime(0, 0, 0)))
        self.C_Date.setMaximumDateTime(QDateTime(QDate(2028, 12, 31), QTime(23, 59, 59)))
        self.C_Date.setMinimumDateTime(QDateTime(QDate(2010, 1, 1), QTime(0, 0, 0)))

        self.horizontalLayout_5.addWidget(self.C_Date)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_7)

        self.horizontalLayout_5.setStretch(0, 2)
        self.horizontalLayout_5.setStretch(1, 3)
        self.horizontalLayout_5.setStretch(2, 1)
        self.horizontalLayout_5.setStretch(3, 2)
        self.horizontalLayout_5.setStretch(5, 1)

        self.gridLayout_2.addLayout(self.horizontalLayout_5, 3, 0, 1, 2)

        self.line = QFrame(self.TabCreate)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line, 4, 0, 1, 2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, 20, -1, 20)
        self.C_RunButton = QPushButton(self.TabCreate)
        self.C_RunButton.setObjectName(u"C_RunButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.C_RunButton.sizePolicy().hasHeightForWidth())
        self.C_RunButton.setSizePolicy(sizePolicy2)

        self.horizontalLayout_4.addWidget(self.C_RunButton)


        self.gridLayout_2.addLayout(self.horizontalLayout_4, 5, 0, 1, 2)

        self.tabWidget.addTab(self.TabCreate, "")
        self.TabMaintain = QWidget()
        self.TabMaintain.setObjectName(u"TabMaintain")
        self.gridLayout_4 = QGridLayout(self.TabMaintain)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(-1, 0, -1, 5)
        self.label_13 = QLabel(self.TabMaintain)
        self.label_13.setObjectName(u"label_13")
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_13)

        self.verticalSpacer_5 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_5)

        self.label_14 = QLabel(self.TabMaintain)
        self.label_14.setObjectName(u"label_14")
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_14)

        self.verticalSpacer_3 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_3)

        self.label_15 = QLabel(self.TabMaintain)
        self.label_15.setObjectName(u"label_15")
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_15)

        self.verticalLayout_5.setStretch(0, 20)
        self.verticalLayout_5.setStretch(1, 1)
        self.verticalLayout_5.setStretch(2, 20)
        self.verticalLayout_5.setStretch(3, 2)
        self.verticalLayout_5.setStretch(4, 20)

        self.gridLayout_4.addLayout(self.verticalLayout_5, 0, 0, 3, 1)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setSpacing(7)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(-1, 20, -1, 20)
        self.M_InputFile_1 = QLineEdit(self.TabMaintain)
        self.M_InputFile_1.setObjectName(u"M_InputFile_1")
        sizePolicy1.setHeightForWidth(self.M_InputFile_1.sizePolicy().hasHeightForWidth())
        self.M_InputFile_1.setSizePolicy(sizePolicy1)
        self.M_InputFile_1.setReadOnly(True)

        self.horizontalLayout_14.addWidget(self.M_InputFile_1)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_15)

        self.M_InputButton_1 = QPushButton(self.TabMaintain)
        self.M_InputButton_1.setObjectName(u"M_InputButton_1")
        sizePolicy.setHeightForWidth(self.M_InputButton_1.sizePolicy().hasHeightForWidth())
        self.M_InputButton_1.setSizePolicy(sizePolicy)

        self.horizontalLayout_14.addWidget(self.M_InputButton_1)

        self.horizontalLayout_14.setStretch(0, 11)
        self.horizontalLayout_14.setStretch(1, 1)
        self.horizontalLayout_14.setStretch(2, 4)

        self.gridLayout_4.addLayout(self.horizontalLayout_14, 0, 1, 1, 1)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(-1, 20, -1, 20)
        self.M_InputFile_2 = QLineEdit(self.TabMaintain)
        self.M_InputFile_2.setObjectName(u"M_InputFile_2")
        sizePolicy1.setHeightForWidth(self.M_InputFile_2.sizePolicy().hasHeightForWidth())
        self.M_InputFile_2.setSizePolicy(sizePolicy1)
        self.M_InputFile_2.setReadOnly(True)

        self.horizontalLayout_15.addWidget(self.M_InputFile_2)

        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_16)

        self.M_InputButton_2 = QPushButton(self.TabMaintain)
        self.M_InputButton_2.setObjectName(u"M_InputButton_2")
        sizePolicy.setHeightForWidth(self.M_InputButton_2.sizePolicy().hasHeightForWidth())
        self.M_InputButton_2.setSizePolicy(sizePolicy)

        self.horizontalLayout_15.addWidget(self.M_InputButton_2)

        self.horizontalLayout_15.setStretch(0, 11)
        self.horizontalLayout_15.setStretch(1, 1)
        self.horizontalLayout_15.setStretch(2, 4)

        self.gridLayout_4.addLayout(self.horizontalLayout_15, 1, 1, 1, 1)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(-1, 20, -1, 20)
        self.M_OutputDir = QLineEdit(self.TabMaintain)
        self.M_OutputDir.setObjectName(u"M_OutputDir")
        sizePolicy1.setHeightForWidth(self.M_OutputDir.sizePolicy().hasHeightForWidth())
        self.M_OutputDir.setSizePolicy(sizePolicy1)
        self.M_OutputDir.setReadOnly(True)

        self.horizontalLayout_12.addWidget(self.M_OutputDir)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_14)

        self.M_OutputButton = QPushButton(self.TabMaintain)
        self.M_OutputButton.setObjectName(u"M_OutputButton")
        sizePolicy.setHeightForWidth(self.M_OutputButton.sizePolicy().hasHeightForWidth())
        self.M_OutputButton.setSizePolicy(sizePolicy)

        self.horizontalLayout_12.addWidget(self.M_OutputButton)

        self.horizontalLayout_12.setStretch(0, 11)
        self.horizontalLayout_12.setStretch(1, 1)
        self.horizontalLayout_12.setStretch(2, 4)

        self.gridLayout_4.addLayout(self.horizontalLayout_12, 2, 1, 1, 1)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(-1, 20, -1, 20)
        self.label_11 = QLabel(self.TabMaintain)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_11.addWidget(self.label_11)

        self.M_User = QLineEdit(self.TabMaintain)
        self.M_User.setObjectName(u"M_User")
        sizePolicy1.setHeightForWidth(self.M_User.sizePolicy().hasHeightForWidth())
        self.M_User.setSizePolicy(sizePolicy1)

        self.horizontalLayout_11.addWidget(self.M_User)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_12)

        self.label_12 = QLabel(self.TabMaintain)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_11.addWidget(self.label_12)

        self.M_Date = QDateEdit(self.TabMaintain)
        self.M_Date.setObjectName(u"M_Date")
        self.M_Date.setDateTime(QDateTime(QDate(2022, 5, 1), QTime(0, 0, 0)))
        self.M_Date.setMaximumDateTime(QDateTime(QDate(2025, 12, 31), QTime(23, 59, 59)))
        self.M_Date.setMinimumDateTime(QDateTime(QDate(2010, 9, 14), QTime(0, 0, 0)))

        self.horizontalLayout_11.addWidget(self.M_Date)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_13)

        self.horizontalLayout_11.setStretch(0, 2)
        self.horizontalLayout_11.setStretch(1, 3)
        self.horizontalLayout_11.setStretch(2, 1)
        self.horizontalLayout_11.setStretch(3, 2)
        self.horizontalLayout_11.setStretch(5, 1)

        self.gridLayout_4.addLayout(self.horizontalLayout_11, 3, 0, 1, 2)

        self.line_3 = QFrame(self.TabMaintain)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.gridLayout_4.addWidget(self.line_3, 4, 0, 1, 2)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(-1, 20, -1, 20)
        self.M_RunButton = QPushButton(self.TabMaintain)
        self.M_RunButton.setObjectName(u"M_RunButton")
        sizePolicy2.setHeightForWidth(self.M_RunButton.sizePolicy().hasHeightForWidth())
        self.M_RunButton.setSizePolicy(sizePolicy2)

        self.horizontalLayout_13.addWidget(self.M_RunButton)


        self.gridLayout_4.addLayout(self.horizontalLayout_13, 5, 0, 1, 2)

        self.tabWidget.addTab(self.TabMaintain, "")

        self.gridLayout.addWidget(self.tabWidget, 3, 0, 1, 1)


        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u66f4\u65b0\u4e0e\u7ef4\u62a4\u8ba1\u8d39\u8868", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u6628\u65e5\u8ba1\u8d39\u8868:", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u4e2d\u53f0\u6587\u4ef6\u5939:", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58\u81f3\u6587\u4ef6\u5939:", None))
        self.C_InputFile_1.setPlaceholderText(QCoreApplication.translate("Form", u"\u9009\u62e9\u6587\u4ef6", None))
        self.C_InputButton_1.setText(QCoreApplication.translate("Form", u"\u6253\u5f00", None))
        self.C_InputFile_2.setPlaceholderText(QCoreApplication.translate("Form", u"\u9009\u62e9\u4e2d\u53f0\u6587\u4ef6\u5939", None))
        self.C_InputButton_2.setText(QCoreApplication.translate("Form", u"\u6253\u5f00", None))
        self.C_OutputDir.setPlaceholderText(QCoreApplication.translate("Form", u"\u9009\u62e9\u8f93\u51fa\u6587\u4ef6\u5939", None))
        self.C_OutputButton.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u64cd\u4f5c\u4eba:", None))
        self.C_User.setPlaceholderText(QCoreApplication.translate("Form", u"\u8f93\u5165\u64cd\u4f5c\u4eba", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u5f53\u5929\u65e5\u671f:", None))
        self.C_RunButton.setText(QCoreApplication.translate("Form", u"\u751f\u6210", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.TabCreate), QCoreApplication.translate("Form", u"\u66f4\u65b0\u8ba1\u8d39\u8868", None))
        self.label_13.setText(QCoreApplication.translate("Form", u"\u4eca\u65e5\u8ba1\u8d39\u8868:", None))
        self.label_14.setText(QCoreApplication.translate("Form", u"\u7279\u6b8a\u56de\u6b3e\u8868:", None))
        self.label_15.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58\u81f3\u6587\u4ef6\u5939:", None))
        self.M_InputFile_1.setPlaceholderText(QCoreApplication.translate("Form", u"\u9009\u62e9\u6587\u4ef6", None))
        self.M_InputButton_1.setText(QCoreApplication.translate("Form", u"\u6253\u5f00", None))
        self.M_InputFile_2.setPlaceholderText(QCoreApplication.translate("Form", u"\u9009\u62e9\u6587\u4ef6", None))
        self.M_InputButton_2.setText(QCoreApplication.translate("Form", u"\u6253\u5f00", None))
        self.M_OutputDir.setPlaceholderText(QCoreApplication.translate("Form", u"\u9009\u62e9\u8f93\u51fa\u6587\u4ef6\u5939", None))
        self.M_OutputButton.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"\u64cd\u4f5c\u4eba:", None))
        self.M_User.setPlaceholderText(QCoreApplication.translate("Form", u"\u8f93\u5165\u64cd\u4f5c\u4eba", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"\u5f53\u5929\u65e5\u671f:", None))
        self.M_RunButton.setText(QCoreApplication.translate("Form", u"\u751f\u6210", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.TabMaintain), QCoreApplication.translate("Form", u"\u7ef4\u62a4\u8ba1\u8d39\u8868", None))
    # retranslateUi

