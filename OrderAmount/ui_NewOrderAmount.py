# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'NewOrderAmount.ui'
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
        Form.resize(667, 434)
        Form.setMinimumSize(QSize(667, 434))
        Form.setMaximumSize(QSize(1600, 866))
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(50, 30, 50, 30)
        self.splitter_3 = QSplitter(Form)
        self.splitter_3.setObjectName(u"splitter_3")
        self.splitter_3.setFrameShape(QFrame.NoFrame)
        self.splitter_3.setOrientation(Qt.Vertical)
        self.layoutWidget1 = QWidget(self.splitter_3)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.horizontalLayout_6 = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_1 = QLabel(self.layoutWidget1)
        self.label_1.setObjectName(u"label_1")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.label_1.sizePolicy().hasHeightForWidth())
        self.label_1.setSizePolicy(sizePolicy)
        self.label_1.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_1)

        self.label_4 = QLabel(self.layoutWidget1)
        self.label_4.setObjectName(u"label_4")
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_4)


        self.horizontalLayout_6.addLayout(self.verticalLayout_2)

        self.splitter = QSplitter(self.layoutWidget1)
        self.splitter.setObjectName(u"splitter")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(2)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy1)
        self.splitter.setOrientation(Qt.Vertical)
        self.layoutWidget2 = QWidget(self.splitter)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.horizontalLayout = QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.InputDir = QLineEdit(self.layoutWidget2)
        self.InputDir.setObjectName(u"InputDir")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(3)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.InputDir.sizePolicy().hasHeightForWidth())
        self.InputDir.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.InputDir)

        self.horizontalSpacer_2 = QSpacerItem(30, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.InputButton = QPushButton(self.layoutWidget2)
        self.InputButton.setObjectName(u"InputButton")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.InputButton.sizePolicy().hasHeightForWidth())
        self.InputButton.setSizePolicy(sizePolicy3)

        self.horizontalLayout.addWidget(self.InputButton)

        self.splitter.addWidget(self.layoutWidget2)
        self.layoutWidget5 = QWidget(self.splitter)
        self.layoutWidget5.setObjectName(u"layoutWidget5")
        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.OutputDir = QLineEdit(self.layoutWidget5)
        self.OutputDir.setObjectName(u"OutputDir")
        sizePolicy2.setHeightForWidth(self.OutputDir.sizePolicy().hasHeightForWidth())
        self.OutputDir.setSizePolicy(sizePolicy2)

        self.horizontalLayout_3.addWidget(self.OutputDir)

        self.horizontalSpacer_4 = QSpacerItem(30, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        self.OutputButton = QPushButton(self.layoutWidget5)
        self.OutputButton.setObjectName(u"OutputButton")
        sizePolicy3.setHeightForWidth(self.OutputButton.sizePolicy().hasHeightForWidth())
        self.OutputButton.setSizePolicy(sizePolicy3)

        self.horizontalLayout_3.addWidget(self.OutputButton)

        self.splitter.addWidget(self.layoutWidget5)

        self.horizontalLayout_6.addWidget(self.splitter)

        self.splitter_3.addWidget(self.layoutWidget1)
        self.splitter_2 = QSplitter(self.splitter_3)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Vertical)
        self.layoutWidget6 = QWidget(self.splitter_2)
        self.layoutWidget6.setObjectName(u"layoutWidget6")
        self.horizontalLayout_4 = QHBoxLayout(self.layoutWidget6)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.layoutWidget6)
        self.label_5.setObjectName(u"label_5")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(1)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy4)
        self.label_5.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_5)

        self.User = QLineEdit(self.layoutWidget6)
        self.User.setObjectName(u"User")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(1)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.User.sizePolicy().hasHeightForWidth())
        self.User.setSizePolicy(sizePolicy5)

        self.horizontalLayout_4.addWidget(self.User)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.label_6 = QLabel(self.layoutWidget6)
        self.label_6.setObjectName(u"label_6")
        sizePolicy4.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy4)
        self.label_6.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_6)

        self.Remark = QLineEdit(self.layoutWidget6)
        self.Remark.setObjectName(u"Remark")

        self.horizontalLayout_4.addWidget(self.Remark)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_6)

        self.splitter_2.addWidget(self.layoutWidget6)
        self.line = QFrame(self.splitter_2)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.splitter_2.addWidget(self.line)
        self.horizontalLayoutWidget7 = QWidget(self.splitter_2)
        self.horizontalLayoutWidget7.setObjectName(u"horizontalLayoutWidget7")
        self.horizontalLayout_5 = QHBoxLayout(self.horizontalLayoutWidget7)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.RunButton = QPushButton(self.horizontalLayoutWidget7)
        self.RunButton.setObjectName(u"RunButton")
        sizePolicy6 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.RunButton.sizePolicy().hasHeightForWidth())
        self.RunButton.setSizePolicy(sizePolicy6)

        self.horizontalLayout_5.addWidget(self.RunButton)

        self.splitter_2.addWidget(self.horizontalLayoutWidget7)
        self.splitter_3.addWidget(self.splitter_2)

        self.verticalLayout.addWidget(self.splitter_3)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u8ba2\u5355\u91d1\u989d\u8868", None))
        self.label_1.setText(QCoreApplication.translate("Form", u"\u6e05\u6d17\u540e\u6587\u4ef6\u5939:", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58\u81f3\u6587\u4ef6\u5939:", None))
        self.InputDir.setPlaceholderText(QCoreApplication.translate("Form", u"\u9009\u62e9\u6e05\u6d17\u540e\u6587\u4ef6\u5939\u8def\u5f84", None))
        self.InputButton.setText(QCoreApplication.translate("Form", u"\u6253\u5f00", None))
        self.OutputDir.setPlaceholderText(QCoreApplication.translate("Form", u"\u9009\u62e9\u8f93\u51fa\u6587\u4ef6\u5939", None))
        self.OutputButton.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u64cd\u4f5c\u4eba:", None))
        self.User.setInputMask("")
        self.User.setPlaceholderText(QCoreApplication.translate("Form", u"\u8f93\u5165\u64cd\u4f5c\u4eba", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\u5907\u6ce8:", None))
        self.Remark.setPlaceholderText(QCoreApplication.translate("Form", u"\u8f93\u5165\u5907\u6ce8", None))
        self.RunButton.setText(QCoreApplication.translate("Form", u"\u751f\u6210", None))
    # retranslateUi

