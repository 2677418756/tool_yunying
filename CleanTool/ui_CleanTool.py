# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Clean.ui'
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
        Form.resize(640, 422)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setAcceptDrops(False)
        Form.setLayoutDirection(Qt.LeftToRight)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(7)
        self.gridLayout.setContentsMargins(30, 30, 30, 30)
        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 4, 0, 1, 3)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 0, -1, 20)
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_2)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_3)

        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_4)


        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 4, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, 20, -1, 20)
        self.RunButton = QPushButton(Form)
        self.RunButton.setObjectName(u"RunButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.RunButton.sizePolicy().hasHeightForWidth())
        self.RunButton.setSizePolicy(sizePolicy1)

        self.horizontalLayout_4.addWidget(self.RunButton)


        self.gridLayout.addLayout(self.horizontalLayout_4, 5, 0, 1, 3)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(7)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 20, -1, 20)
        self.InputDir = QLineEdit(Form)
        self.InputDir.setObjectName(u"InputDir")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.InputDir.sizePolicy().hasHeightForWidth())
        self.InputDir.setSizePolicy(sizePolicy2)
        self.InputDir.setReadOnly(True)

        self.horizontalLayout.addWidget(self.InputDir)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.InputButton = QPushButton(Form)
        self.InputButton.setObjectName(u"InputButton")
        sizePolicy.setHeightForWidth(self.InputButton.sizePolicy().hasHeightForWidth())
        self.InputButton.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.InputButton)

        self.horizontalLayout.setStretch(0, 11)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 4)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 20, -1, 20)
        self.OutputDir = QLineEdit(Form)
        self.OutputDir.setObjectName(u"OutputDir")
        sizePolicy2.setHeightForWidth(self.OutputDir.sizePolicy().hasHeightForWidth())
        self.OutputDir.setSizePolicy(sizePolicy2)
        self.OutputDir.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.OutputDir)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.OutputButton = QPushButton(Form)
        self.OutputButton.setObjectName(u"OutputButton")
        sizePolicy.setHeightForWidth(self.OutputButton.sizePolicy().hasHeightForWidth())
        self.OutputButton.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.OutputButton)

        self.horizontalLayout_2.setStretch(0, 11)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 4)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 20, -1, 20)
        self.User = QLineEdit(Form)
        self.User.setObjectName(u"User")
        sizePolicy2.setHeightForWidth(self.User.sizePolicy().hasHeightForWidth())
        self.User.setSizePolicy(sizePolicy2)

        self.horizontalLayout_3.addWidget(self.User)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.horizontalLayout_3.setStretch(0, 11)
        self.horizontalLayout_3.setStretch(1, 6)

        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, 20, -1, 20)
        self.Customer = QLineEdit(Form)
        self.Customer.setObjectName(u"Customer")
        sizePolicy2.setHeightForWidth(self.Customer.sizePolicy().hasHeightForWidth())
        self.Customer.setSizePolicy(sizePolicy2)

        self.horizontalLayout_5.addWidget(self.Customer)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_6)

        self.horizontalLayout_5.setStretch(0, 11)
        self.horizontalLayout_5.setStretch(1, 6)

        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 1)

        self.gridLayout.addLayout(self.verticalLayout, 0, 2, 1, 1)

        self.gridLayout.setRowStretch(0, 1)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u6e05\u6d17\u5c0f\u5de5\u5177", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u6e05\u6d17\u6587\u4ef6\u5939:", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58\u81f3\u6587\u4ef6\u5939:", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u64cd\u4f5c\u4eba:", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u5ba2\u6237\u540d\u79f0:", None))
        self.RunButton.setText(QCoreApplication.translate("Form", u"\u751f\u6210", None))
        self.InputDir.setPlaceholderText(QCoreApplication.translate("Form", u"\u9009\u62e9\u8f93\u5165\u6587\u4ef6\u5939", None))
        self.InputButton.setText(QCoreApplication.translate("Form", u"\u6253\u5f00", None))
        self.OutputDir.setPlaceholderText(QCoreApplication.translate("Form", u"\u9009\u62e9\u8f93\u51fa\u6587\u4ef6\u5939", None))
        self.OutputButton.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58", None))
        self.User.setPlaceholderText(QCoreApplication.translate("Form", u"\u8f93\u5165\u64cd\u4f5c\u4eba", None))
        self.Customer.setText("")
        self.Customer.setPlaceholderText(QCoreApplication.translate("Form", u"\u8f93\u5165\u5ba2\u6237\u540d\u79f0", None))
    # retranslateUi

