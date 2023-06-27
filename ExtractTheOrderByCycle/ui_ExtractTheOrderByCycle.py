# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ExtractTheOrderByCycle.ui'
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
        Form.setMaximumSize(QSize(2200, 1350))
        Form.setAcceptDrops(False)
        Form.setLayoutDirection(Qt.LeftToRight)
        self.horizontalLayout_7 = QHBoxLayout(Form)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(40, 40, 40, 40)
        self.splitter_3 = QSplitter(Form)
        self.splitter_3.setObjectName(u"splitter_3")
        self.splitter_3.setOrientation(Qt.Vertical)
        self.layoutWidget = QWidget(self.splitter_3)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.horizontalLayout_6 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, 0, -1)
        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_3)

        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_2)


        self.horizontalLayout_6.addLayout(self.verticalLayout)

        self.splitter = QSplitter(self.layoutWidget)
        self.splitter.setObjectName(u"splitter")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(2)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy2)
        self.splitter.setOrientation(Qt.Vertical)
        self.layoutWidget1 = QWidget(self.splitter)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.InputDir = QLineEdit(self.layoutWidget1)
        self.InputDir.setObjectName(u"InputDir")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(3)
        sizePolicy3.setVerticalStretch(1)
        sizePolicy3.setHeightForWidth(self.InputDir.sizePolicy().hasHeightForWidth())
        self.InputDir.setSizePolicy(sizePolicy3)
        self.InputDir.setReadOnly(True)

        self.horizontalLayout_3.addWidget(self.InputDir)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        self.InputButton = QPushButton(self.layoutWidget1)
        self.InputButton.setObjectName(u"InputButton")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(1)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.InputButton.sizePolicy().hasHeightForWidth())
        self.InputButton.setSizePolicy(sizePolicy4)

        self.horizontalLayout_3.addWidget(self.InputButton)

        self.splitter.addWidget(self.layoutWidget1)
        self.layoutWidget2 = QWidget(self.splitter)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.OutputDir = QLineEdit(self.layoutWidget2)
        self.OutputDir.setObjectName(u"OutputDir")
        sizePolicy3.setHeightForWidth(self.OutputDir.sizePolicy().hasHeightForWidth())
        self.OutputDir.setSizePolicy(sizePolicy3)
        self.OutputDir.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.OutputDir)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.OutputButton = QPushButton(self.layoutWidget2)
        self.OutputButton.setObjectName(u"OutputButton")
        sizePolicy4.setHeightForWidth(self.OutputButton.sizePolicy().hasHeightForWidth())
        self.OutputButton.setSizePolicy(sizePolicy4)

        self.horizontalLayout_2.addWidget(self.OutputButton)

        self.splitter.addWidget(self.layoutWidget2)

        self.horizontalLayout_6.addWidget(self.splitter)

        self.splitter_3.addWidget(self.layoutWidget)
        self.splitter_2 = QSplitter(self.splitter_3)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Vertical)
        self.layoutWidget3 = QWidget(self.splitter_2)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.horizontalLayout_4 = QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 10, 0, 5)
        self.label_5 = QLabel(self.layoutWidget3)
        self.label_5.setObjectName(u"label_5")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(1)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy5)
        self.label_5.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_5)

        self.dateEdit = QDateEdit(self.layoutWidget3)
        self.dateEdit.setObjectName(u"dateEdit")
        self.dateEdit.setDateTime(QDateTime(QDate(2022, 5, 1), QTime(0, 0, 0)))
        self.dateEdit.setMaximumDate(QDate(2025, 12, 31))
        self.dateEdit.setMinimumDate(QDate(2022, 1, 1))

        self.horizontalLayout_4.addWidget(self.dateEdit)

        self.horizontalSpacer_5 = QSpacerItem(58, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_5)

        self.label_4 = QLabel(self.layoutWidget3)
        self.label_4.setObjectName(u"label_4")
        sizePolicy5.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy5)
        self.label_4.setTextFormat(Qt.AutoText)
        self.label_4.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_4)

        self.CycleDays = QLineEdit(self.layoutWidget3)
        self.CycleDays.setObjectName(u"CycleDays")
        sizePolicy6 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(1)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.CycleDays.sizePolicy().hasHeightForWidth())
        self.CycleDays.setSizePolicy(sizePolicy6)

        self.horizontalLayout_4.addWidget(self.CycleDays)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.splitter_2.addWidget(self.layoutWidget3)
        self.line = QFrame(self.splitter_2)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.splitter_2.addWidget(self.line)
        self.horizontalLayoutWidget = QWidget(self.splitter_2)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayout_5 = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.RunButton = QPushButton(self.horizontalLayoutWidget)
        self.RunButton.setObjectName(u"RunButton")
        sizePolicy7 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.RunButton.sizePolicy().hasHeightForWidth())
        self.RunButton.setSizePolicy(sizePolicy7)

        self.horizontalLayout_5.addWidget(self.RunButton)

        self.splitter_2.addWidget(self.horizontalLayoutWidget)
        self.splitter_3.addWidget(self.splitter_2)

        self.horizontalLayout_7.addWidget(self.splitter_3)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u6309\u65e5\u671f\u63d0\u53d6\u8ba2\u5355\u8868", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u5ba2\u6237-\u65f6\u95f4\u6587\u4ef6\u5939:", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58\u81f3\u6587\u4ef6\u5939:", None))
        self.InputDir.setPlaceholderText(QCoreApplication.translate("Form", u"\u9009\u62e9\u8f93\u5165\u6587\u4ef6\u5939", None))
        self.InputButton.setText(QCoreApplication.translate("Form", u"\u6253\u5f00", None))
        self.OutputDir.setPlaceholderText(QCoreApplication.translate("Form", u"\u9009\u62e9\u8f93\u51fa\u6587\u4ef6\u5939", None))
        self.OutputButton.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u5f53\u5929\u65e5\u671f:", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u5468\u671f\u5929\u6570:", None))
        self.CycleDays.setPlaceholderText(QCoreApplication.translate("Form", u"\u9ed8\u8ba4\u5468\u671f\u5929\u6570\u4e3a20\u5929", None))
        self.RunButton.setText(QCoreApplication.translate("Form", u"\u751f\u6210", None))
    # retranslateUi


