# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ner_editor.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_NEREditor(object):
    def setupUi(self, NEREditor):
        if not NEREditor.objectName():
            NEREditor.setObjectName(u"NEREditor")
        NEREditor.resize(927, 723)
        self.gridLayout_7 = QGridLayout(NEREditor)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.openButton = QPushButton(NEREditor)
        self.openButton.setObjectName(u"openButton")

        self.gridLayout.addWidget(self.openButton, 0, 0, 1, 1)

        self.exportButton = QPushButton(NEREditor)
        self.exportButton.setObjectName(u"exportButton")

        self.gridLayout.addWidget(self.exportButton, 0, 4, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(100, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 0, 3, 1, 1)

        self.fontSetButton = QPushButton(NEREditor)
        self.fontSetButton.setObjectName(u"fontSetButton")

        self.gridLayout.addWidget(self.fontSetButton, 0, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(100, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 1, 1, 1)

        self.quitButton = QPushButton(NEREditor)
        self.quitButton.setObjectName(u"quitButton")

        self.gridLayout.addWidget(self.quitButton, 0, 6, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(100, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 0, 5, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.line = QFrame(NEREditor)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout_3.addWidget(self.line, 1, 0, 1, 1)

        self.textEdit = QTextEdit(NEREditor)
        self.textEdit.setObjectName(u"textEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setReadOnly(True)

        self.gridLayout_3.addWidget(self.textEdit, 2, 0, 1, 1)


        self.gridLayout_6.addLayout(self.gridLayout_3, 0, 0, 1, 1)

        self.groupBox = QGroupBox(NEREditor)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy1)
        self.groupBox.setCheckable(False)
        self.widget = QWidget(self.groupBox)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(15, 33, 145, 147))
        self.labelGridLayout = QGridLayout(self.widget)
        self.labelGridLayout.setObjectName(u"labelGridLayout")
        self.labelGridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")

        self.labelGridLayout.addWidget(self.label_3, 0, 0, 1, 1)

        self.lineEdit = QLineEdit(self.widget)
        self.lineEdit.setObjectName(u"lineEdit")
        font = QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)
        self.lineEdit.setFont(font)
        self.lineEdit.setReadOnly(True)

        self.labelGridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)

        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")

        self.labelGridLayout.addWidget(self.label_4, 1, 0, 1, 1)

        self.lineEdit_2 = QLineEdit(self.widget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        font1 = QFont()
        font1.setBold(True)
        font1.setItalic(False)
        font1.setWeight(75)
        self.lineEdit_2.setFont(font1)
        self.lineEdit_2.setReadOnly(True)

        self.labelGridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)

        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")

        self.labelGridLayout.addWidget(self.label_5, 2, 0, 1, 1)

        self.lineEdit_3 = QLineEdit(self.widget)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setFont(font1)
        self.lineEdit_3.setReadOnly(True)

        self.labelGridLayout.addWidget(self.lineEdit_3, 2, 1, 1, 1)

        self.label_6 = QLabel(self.widget)
        self.label_6.setObjectName(u"label_6")

        self.labelGridLayout.addWidget(self.label_6, 3, 0, 1, 1)

        self.lineEdit_4 = QLineEdit(self.widget)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setFont(font1)
        self.lineEdit_4.setReadOnly(True)

        self.labelGridLayout.addWidget(self.lineEdit_4, 3, 1, 1, 1)

        self.label_7 = QLabel(self.widget)
        self.label_7.setObjectName(u"label_7")

        self.labelGridLayout.addWidget(self.label_7, 4, 0, 1, 1)

        self.lineEdit_5 = QLineEdit(self.widget)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setFont(font1)
        self.lineEdit_5.setReadOnly(True)

        self.labelGridLayout.addWidget(self.lineEdit_5, 4, 1, 1, 1)


        self.gridLayout_6.addWidget(self.groupBox, 0, 1, 1, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.line_2 = QFrame(NEREditor)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout_4.addWidget(self.line_2, 0, 0, 1, 2)

        self.label_8 = QLabel(NEREditor)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_4.addWidget(self.label_8, 1, 0, 1, 1)

        self.useREButton = QCheckBox(NEREditor)
        self.useREButton.setObjectName(u"useREButton")

        self.gridLayout_4.addWidget(self.useREButton, 1, 1, 1, 1)

        self.configFileButton = QComboBox(NEREditor)
        self.configFileButton.addItem("")
        self.configFileButton.setObjectName(u"configFileButton")
        self.configFileButton.setMinimumSize(QSize(8, 0))
        self.configFileButton.setMaximumSize(QSize(91, 16777215))
        self.configFileButton.setMouseTracking(False)

        self.gridLayout_4.addWidget(self.configFileButton, 2, 0, 1, 1)

        self.splitSentButton = QCheckBox(NEREditor)
        self.splitSentButton.setObjectName(u"splitSentButton")

        self.gridLayout_4.addWidget(self.splitSentButton, 2, 1, 1, 1)


        self.gridLayout_6.addLayout(self.gridLayout_4, 1, 1, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.lastFileButton = QPushButton(NEREditor)
        self.lastFileButton.setObjectName(u"lastFileButton")

        self.gridLayout_2.addWidget(self.lastFileButton, 0, 2, 1, 1)

        self.nextFileButton = QPushButton(NEREditor)
        self.nextFileButton.setObjectName(u"nextFileButton")

        self.gridLayout_2.addWidget(self.nextFileButton, 1, 2, 1, 1)

        self.progressButton = QLabel(NEREditor)
        self.progressButton.setObjectName(u"progressButton")

        self.gridLayout_2.addWidget(self.progressButton, 0, 0, 1, 1)

        self.fileLabel = QLabel(NEREditor)
        self.fileLabel.setObjectName(u"fileLabel")
        sizePolicy1.setHeightForWidth(self.fileLabel.sizePolicy().hasHeightForWidth())
        self.fileLabel.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.fileLabel, 1, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(400, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_4, 0, 1, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(400, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_5, 1, 1, 1, 1)


        self.gridLayout_6.addLayout(self.gridLayout_2, 1, 0, 1, 1)


        self.gridLayout_7.addLayout(self.gridLayout_6, 0, 0, 1, 1)


        self.retranslateUi(NEREditor)

        QMetaObject.connectSlotsByName(NEREditor)
    # setupUi

    def retranslateUi(self, NEREditor):
        NEREditor.setWindowTitle(QCoreApplication.translate("NEREditor", u"Form", None))
        self.openButton.setText(QCoreApplication.translate("NEREditor", u"open", None))
        self.exportButton.setText(QCoreApplication.translate("NEREditor", u"export", None))
        self.fontSetButton.setText(QCoreApplication.translate("NEREditor", u"font", None))
        self.quitButton.setText(QCoreApplication.translate("NEREditor", u"quit", None))
        self.groupBox.setTitle(QCoreApplication.translate("NEREditor", u"\u547d\u540d\u5b9e\u4f53\u6807\u7b7e", None))
        self.label_3.setText(QCoreApplication.translate("NEREditor", u"A", None))
        self.lineEdit.setText(QCoreApplication.translate("NEREditor", u"ORG", None))
        self.label_4.setText(QCoreApplication.translate("NEREditor", u"B", None))
        self.lineEdit_2.setText(QCoreApplication.translate("NEREditor", u"PER", None))
        self.label_5.setText(QCoreApplication.translate("NEREditor", u"C", None))
        self.lineEdit_3.setText(QCoreApplication.translate("NEREditor", u"LOC", None))
        self.label_6.setText(QCoreApplication.translate("NEREditor", u"D", None))
        self.lineEdit_4.setText(QCoreApplication.translate("NEREditor", u"TITLE", None))
        self.label_7.setText(QCoreApplication.translate("NEREditor", u"E", None))
        self.lineEdit_5.setText(QCoreApplication.translate("NEREditor", u"INDEPENDENT", None))
        self.label_8.setText(QCoreApplication.translate("NEREditor", u"\u6807\u7b7e\u914d\u7f6e\u6587\u4ef6", None))
        self.useREButton.setText(QCoreApplication.translate("NEREditor", u"\u63a8\u8350\u6a21\u578b", None))
        self.configFileButton.setItemText(0, QCoreApplication.translate("NEREditor", u"default.config", None))

        self.splitSentButton.setText(QCoreApplication.translate("NEREditor", u"\u5206\u53e5\u663e\u793a", None))
        self.lastFileButton.setText(QCoreApplication.translate("NEREditor", u"\u4e0a\u4e00\u4e2a", None))
        self.nextFileButton.setText(QCoreApplication.translate("NEREditor", u"\u4e0b\u4e00\u4e2a", None))
        self.progressButton.setText(QCoreApplication.translate("NEREditor", u"\u6807\u6ce8\u8fdb\u5ea6\uff1a0/0", None))
        self.fileLabel.setText(QCoreApplication.translate("NEREditor", u"\u6587\u4ef6", None))
    # retranslateUi

