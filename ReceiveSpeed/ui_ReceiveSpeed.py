# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ReceiveSpeed.ui'
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
        Form.resize(667, 434)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(667, 434))
        Form.setMaximumSize(QSize(800, 434))
        Form.setAcceptDrops(False)
        Form.setLayoutDirection(Qt.LeftToRight)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(7)
        self.gridLayout.setContentsMargins(30, 30, 30, 30)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 20, -1, 20)
        self.OutputDir = QLineEdit(Form)
        self.OutputDir.setObjectName(u"OutputDir")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.OutputDir.sizePolicy().hasHeightForWidth())
        self.OutputDir.setSizePolicy(sizePolicy1)
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

        self.gridLayout.addLayout(self.horizontalLayout_2, 4, 1, 1, 1)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 10, 0, 1, 3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, 20, -1, 20)
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.label_4)

        self.User = QLineEdit(Form)
        self.User.setObjectName(u"User")
        sizePolicy1.setHeightForWidth(self.User.sizePolicy().hasHeightForWidth())
        self.User.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.User)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_6)

        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.label_5)

        self.Remark = QLineEdit(Form)
        self.Remark.setObjectName(u"Remark")
        sizePolicy1.setHeightForWidth(self.Remark.sizePolicy().hasHeightForWidth())
        self.Remark.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.Remark)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_7)

        self.horizontalLayout_5.setStretch(0, 2)
        self.horizontalLayout_5.setStretch(1, 3)
        self.horizontalLayout_5.setStretch(2, 1)
        self.horizontalLayout_5.setStretch(3, 2)
        self.horizontalLayout_5.setStretch(4, 3)
        self.horizontalLayout_5.setStretch(5, 1)

        self.gridLayout.addLayout(self.horizontalLayout_5, 9, 0, 1, 2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 0, -1, 5)
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_3)

        self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_2)

        self.verticalLayout_3.setStretch(0, 5)
        self.verticalLayout_3.setStretch(1, 5)
        self.verticalLayout_3.setStretch(3, 5)

        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 6, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, 20, -1, 20)
        self.RunButton = QPushButton(Form)
        self.RunButton.setObjectName(u"RunButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.RunButton.sizePolicy().hasHeightForWidth())
        self.RunButton.setSizePolicy(sizePolicy2)

        self.horizontalLayout_4.addWidget(self.RunButton)


        self.gridLayout.addLayout(self.horizontalLayout_4, 11, 0, 1, 3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(7)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 20, -1, 20)
        self.InputFile_1 = QLineEdit(Form)
        self.InputFile_1.setObjectName(u"InputFile_1")
        sizePolicy1.setHeightForWidth(self.InputFile_1.sizePolicy().hasHeightForWidth())
        self.InputFile_1.setSizePolicy(sizePolicy1)
        self.InputFile_1.setReadOnly(True)

        self.horizontalLayout.addWidget(self.InputFile_1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.InputButton_1 = QPushButton(Form)
        self.InputButton_1.setObjectName(u"InputButton_1")
        sizePolicy.setHeightForWidth(self.InputButton_1.sizePolicy().hasHeightForWidth())
        self.InputButton_1.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.InputButton_1)

        self.horizontalLayout.setStretch(0, 11)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 4)

        self.gridLayout.addLayout(self.horizontalLayout, 0, 1, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 20, -1, 20)
        self.InputFile_2 = QLineEdit(Form)
        self.InputFile_2.setObjectName(u"InputFile_2")
        sizePolicy1.setHeightForWidth(self.InputFile_2.sizePolicy().hasHeightForWidth())
        self.InputFile_2.setSizePolicy(sizePolicy1)
        self.InputFile_2.setReadOnly(True)

        self.horizontalLayout_3.addWidget(self.InputFile_2)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        self.InputButton_2 = QPushButton(Form)
        self.InputButton_2.setObjectName(u"InputButton_2")
        sizePolicy.setHeightForWidth(self.InputButton_2.sizePolicy().hasHeightForWidth())
        self.InputButton_2.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.InputButton_2)

        self.horizontalLayout_3.setStretch(0, 11)
        self.horizontalLayout_3.setStretch(1, 1)
        self.horizontalLayout_3.setStretch(2, 4)

        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 1, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u63fd\u6536\u901f\u5ea6\u8868", None))
        self.OutputDir.setPlaceholderText(QCoreApplication.translate("Form", u"\u9009\u62e9\u8f93\u51fa\u6587\u4ef6\u5939", None))
        self.OutputButton.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u64cd\u4f5c\u4eba:", None))
        self.User.setPlaceholderText(QCoreApplication.translate("Form", u"\u8f93\u5165\u64cd\u4f5c\u4eba", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u7cbe\u786e\u5929\u6570:", None))
        self.Remark.setText("")
        self.Remark.setPlaceholderText(QCoreApplication.translate("Form", u"\u9ed8\u8ba4\u7cbe\u786e\u5929\u6570\u4e3a10", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u8ba2\u5355\u8868\u8def\u5f84:", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u8fd0\u5355\u8868\u8def\u5f84:", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58\u81f3\u6587\u4ef6\u5939:", None))
        self.RunButton.setText(QCoreApplication.translate("Form", u"\u751f\u6210", None))
        self.InputFile_1.setPlaceholderText(QCoreApplication.translate("Form", u"\u9009\u62e9\u8def\u5f84", None))
        self.InputButton_1.setText(QCoreApplication.translate("Form", u"\u6253\u5f00", None))
        self.InputFile_2.setPlaceholderText(QCoreApplication.translate("Form", u"\u9009\u62e9\u8def\u5f84", None))
        self.InputButton_2.setText(QCoreApplication.translate("Form", u"\u6253\u5f00", None))
    # retranslateUi

