# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DB_Update.ui'
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
        Form.resize(676, 493)
        Form.setMinimumSize(QSize(676, 493))
        font = QFont()
        font.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font.setPointSize(10)
        Form.setFont(font)
        self.verticalLayout_8 = QVBoxLayout(Form)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setSpacing(12)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(30, 30, 30, 30)
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(30)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.splitter_2 = QSplitter(Form)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Vertical)
        self.splitter = QSplitter(self.splitter_2)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_2)

        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_3)

        self.splitter.addWidget(self.layoutWidget)
        self.layoutWidget1 = QWidget(self.splitter)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setSpacing(26)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.InputFile = QLineEdit(self.layoutWidget1)
        self.InputFile.setObjectName(u"InputFile")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.InputFile.sizePolicy().hasHeightForWidth())
        self.InputFile.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.InputFile)

        self.InputDay = QLineEdit(self.layoutWidget1)
        self.InputDay.setObjectName(u"InputDay")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.InputDay.sizePolicy().hasHeightForWidth())
        self.InputDay.setSizePolicy(sizePolicy2)

        self.verticalLayout_2.addWidget(self.InputDay)

        self.Today = QDateEdit(self.layoutWidget1)
        self.Today.setObjectName(u"Today")
        sizePolicy1.setHeightForWidth(self.Today.sizePolicy().hasHeightForWidth())
        self.Today.setSizePolicy(sizePolicy1)
        self.Today.setDateTime(QDateTime(QDate(2022, 9, 20), QTime(0, 0, 0)))
        self.Today.setMaximumDateTime(QDateTime(QDate(2025, 12, 31), QTime(23, 59, 59)))
        self.Today.setMinimumDateTime(QDateTime(QDate(2021, 1, 1), QTime(0, 0, 0)))

        self.verticalLayout_2.addWidget(self.Today)

        self.splitter.addWidget(self.layoutWidget1)
        self.splitter_2.addWidget(self.splitter)
        self.horizontalLayoutWidget = QWidget(self.splitter_2)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayout_4 = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.UpdateButton = QPushButton(self.horizontalLayoutWidget)
        self.UpdateButton.setObjectName(u"UpdateButton")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.UpdateButton.sizePolicy().hasHeightForWidth())
        self.UpdateButton.setSizePolicy(sizePolicy3)

        self.horizontalLayout_4.addWidget(self.UpdateButton)

        self.InsertButton = QPushButton(self.horizontalLayoutWidget)
        self.InsertButton.setObjectName(u"InsertButton")
        sizePolicy3.setHeightForWidth(self.InsertButton.sizePolicy().hasHeightForWidth())
        self.InsertButton.setSizePolicy(sizePolicy3)

        self.horizontalLayout_4.addWidget(self.InsertButton)

        self.splitter_2.addWidget(self.horizontalLayoutWidget)

        self.horizontalLayout_5.addWidget(self.splitter_2)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(10, 10, 12, 10)
        self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.verticalLayout_5.addItem(self.verticalSpacer)

        self.InputButton = QPushButton(Form)
        self.InputButton.setObjectName(u"InputButton")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(1)
        sizePolicy4.setHeightForWidth(self.InputButton.sizePolicy().hasHeightForWidth())
        self.InputButton.setSizePolicy(sizePolicy4)

        self.verticalLayout_5.addWidget(self.InputButton)

        self.textBrowser = QTextBrowser(Form)
        self.textBrowser.setObjectName(u"textBrowser")
        sizePolicy5 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(10)
        sizePolicy5.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy5)

        self.verticalLayout_5.addWidget(self.textBrowser)


        self.horizontalLayout_5.addLayout(self.verticalLayout_5)


        self.verticalLayout_6.addLayout(self.horizontalLayout_5)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        sizePolicy6 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(2)
        sizePolicy6.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy6)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_6.addWidget(self.line)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(28)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        sizePolicy7 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy7.setHorizontalStretch(1)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy7)
        self.label_4.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_4)

        self.OutputFile = QLineEdit(Form)
        self.OutputFile.setObjectName(u"OutputFile")
        sizePolicy8 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy8.setHorizontalStretch(3)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.OutputFile.sizePolicy().hasHeightForWidth())
        self.OutputFile.setSizePolicy(sizePolicy8)
        self.OutputFile.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.OutputFile)

        self.OutputButton = QPushButton(Form)
        self.OutputButton.setObjectName(u"OutputButton")
        sizePolicy3.setHeightForWidth(self.OutputButton.sizePolicy().hasHeightForWidth())
        self.OutputButton.setSizePolicy(sizePolicy3)

        self.horizontalLayout.addWidget(self.OutputButton)

        self.label_7 = QLabel(Form)
        self.label_7.setObjectName(u"label_7")
        sizePolicy9 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy9.setHorizontalStretch(1)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy9)
        self.label_7.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_7)

        self.comboBox = QComboBox(Form)
        self.comboBox.setObjectName(u"comboBox")
        sizePolicy10 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy10.setHorizontalStretch(1)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy10)

        self.horizontalLayout.addWidget(self.comboBox)

        self.horizontalSpacer_2 = QSpacerItem(10, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")
        sizePolicy11 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy11.setHorizontalStretch(2)
        sizePolicy11.setVerticalStretch(0)
        sizePolicy11.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy11)
        self.label_5.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_5)

        self.StartTime = QDateTimeEdit(Form)
        self.StartTime.setObjectName(u"StartTime")
        sizePolicy8.setHeightForWidth(self.StartTime.sizePolicy().hasHeightForWidth())
        self.StartTime.setSizePolicy(sizePolicy8)
        self.StartTime.setDateTime(QDateTime(QDate(2022, 9, 1), QTime(0, 0, 0)))

        self.horizontalLayout_2.addWidget(self.StartTime)

        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")
        sizePolicy7.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy7)
        self.label_6.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_6)

        self.EndTime = QDateTimeEdit(Form)
        self.EndTime.setObjectName(u"EndTime")
        sizePolicy8.setHeightForWidth(self.EndTime.sizePolicy().hasHeightForWidth())
        self.EndTime.setSizePolicy(sizePolicy8)
        self.EndTime.setDateTime(QDateTime(QDate(2022, 9, 30), QTime(23, 59, 59)))

        self.horizontalLayout_2.addWidget(self.EndTime)

        self.horizontalSpacer = QSpacerItem(100, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_8 = QLabel(Form)
        self.label_8.setObjectName(u"label_8")
        sizePolicy11.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy11)
        self.label_8.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_8)

        self.settlementDate = QDateEdit(Form)
        self.settlementDate.setObjectName(u"settlementDate")
        sizePolicy11.setHeightForWidth(self.settlementDate.sizePolicy().hasHeightForWidth())
        self.settlementDate.setSizePolicy(sizePolicy11)
        self.settlementDate.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.settlementDate.setDateTime(QDateTime(QDate(2022, 9, 20), QTime(0, 0, 0)))
        self.settlementDate.setMaximumDateTime(QDateTime(QDate(2025, 12, 31), QTime(23, 59, 59)))
        self.settlementDate.setMinimumDateTime(QDateTime(QDate(2022, 1, 1), QTime(0, 0, 0)))

        self.horizontalLayout_3.addWidget(self.settlementDate)

        self.horizontalSpacer_5 = QSpacerItem(25, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)

        self.ReadButton = QPushButton(Form)
        self.ReadButton.setObjectName(u"ReadButton")
        sizePolicy11.setHeightForWidth(self.ReadButton.sizePolicy().hasHeightForWidth())
        self.ReadButton.setSizePolicy(sizePolicy11)

        self.horizontalLayout_3.addWidget(self.ReadButton)

        self.horizontalSpacer_3 = QSpacerItem(230, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)


        self.verticalLayout_6.addLayout(self.verticalLayout_4)


        self.verticalLayout_7.addLayout(self.verticalLayout_6)


        self.verticalLayout_8.addLayout(self.verticalLayout_7)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u6570\u636e\u5e93\u66f4\u65b0\u4e0e\u8bfb\u53d6", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u8f93\u5165\u8ba2\u5355\u72b6\u6001\u8868:", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u5929\u6570:", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u5f53\u5929\u65e5\u671f:", None))
        self.InputFile.setPlaceholderText(QCoreApplication.translate("Form", u"\u8bf7\u8bbe\u7f6e\u8868\u683c\u8def\u5f84", None))
        self.InputDay.setPlaceholderText(QCoreApplication.translate("Form", u"\u9ed8\u8ba4\u4e3a30\u5929", None))
        self.UpdateButton.setText(QCoreApplication.translate("Form", u"\u66f4\u65b0", None))
        self.InsertButton.setText(QCoreApplication.translate("Form", u"\u6388\u4fe1\u63d2\u5165", None))
        self.InputButton.setText(QCoreApplication.translate("Form", u"\u6253\u5f00", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u6700\u65b0\u8ba2\u5355\u72b6\u6001\u8868:", None))
        self.OutputFile.setPlaceholderText(QCoreApplication.translate("Form", u"\u8bbe\u7f6e\u4fdd\u5b58\u6587\u4ef6\u8def\u5f84", None))
        self.OutputButton.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"\u5e97\u94fa\u540d\u79f0:", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u8ba2\u5355\u521b\u5efa\u65f6\u95f4:", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\u81f3", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"\u7cfb\u7edf\u7ed3\u7b97\u65e5\u671f:", None))
        self.ReadButton.setText(QCoreApplication.translate("Form", u"\u63d0\u53d6", None))
    # retranslateUi


