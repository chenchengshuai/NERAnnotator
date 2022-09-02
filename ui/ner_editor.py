# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ner_editor.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import configparser
import json

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NEREditor(object):
    def setupUi(self, NEREditor):
        NEREditor.setObjectName("NEREditor")
        NEREditor.resize(1026, 807)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(NEREditor)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.openButton = QtWidgets.QPushButton(NEREditor)
        self.openButton.setObjectName("openButton")
        self.horizontalLayout_2.addWidget(self.openButton)
        self.reMapButton = QtWidgets.QPushButton(NEREditor)
        self.reMapButton.setObjectName("reMapButton")
        self.horizontalLayout_2.addWidget(self.reMapButton)
        self.newMapButton = QtWidgets.QPushButton(NEREditor)
        self.newMapButton.setObjectName("newMapButton")
        self.horizontalLayout_2.addWidget(self.newMapButton)
        self.fontSetButton = QtWidgets.QPushButton(NEREditor)
        self.fontSetButton.setObjectName("fontSetButton")
        self.horizontalLayout_2.addWidget(self.fontSetButton)
        self.quitButton = QtWidgets.QPushButton(NEREditor)
        self.quitButton.setObjectName("quitButton")
        self.horizontalLayout_2.addWidget(self.quitButton)
        self.useREButton = QtWidgets.QCheckBox(NEREditor)
        self.useREButton.setObjectName("useREButton")
        self.horizontalLayout_2.addWidget(self.useREButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.line = QtWidgets.QFrame(NEREditor)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_4.addWidget(self.line)
        self.splitter = QtWidgets.QSplitter(NEREditor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setMinimumSize(QtCore.QSize(100, 0))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.widget = QtWidgets.QWidget(self.splitter)
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.fileLabel = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileLabel.sizePolicy().hasHeightForWidth())
        self.fileLabel.setSizePolicy(sizePolicy)
        self.fileLabel.setObjectName("fileLabel")
        self.verticalLayout_3.addWidget(self.fileLabel)
        self.textEdit = QtWidgets.QTextEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_3.addWidget(self.textEdit)
        self.widget1 = QtWidgets.QWidget(self.splitter)
        self.widget1.setObjectName("widget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        
        
        self.groupBox = QtWidgets.QGroupBox(self.widget1)
        self.groupBox.setObjectName("groupBox")
        
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        
        self.initLabelMap(NEREditor)

        self.verticalLayout_2.addWidget(self.groupBox)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.line_2 = QtWidgets.QFrame(self.widget1)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.label_8 = QtWidgets.QLabel(self.widget1)
        self.label_8.setObjectName("label_8")
        self.verticalLayout.addWidget(self.label_8, 0, QtCore.Qt.AlignHCenter)
        self.configFileButton = QtWidgets.QComboBox(self.widget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.configFileButton.sizePolicy().hasHeightForWidth())
        self.configFileButton.setSizePolicy(sizePolicy)
        self.configFileButton.setMinimumSize(QtCore.QSize(0, 0))
        self.configFileButton.setMaximumSize(QtCore.QSize(91, 16777215))
        self.configFileButton.setMouseTracking(False)
        self.configFileButton.setObjectName("configFileButton")
        self.configFileButton.addItem("")
        self.verticalLayout.addWidget(self.configFileButton, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2.setStretch(0, 8)
        self.verticalLayout_2.setStretch(1, 2)
        self.verticalLayout_4.addWidget(self.splitter)
        self.verticalLayout_5.addLayout(self.verticalLayout_4)

        self.retranslateUi(NEREditor)
        QtCore.QMetaObject.connectSlotsByName(NEREditor)

    def retranslateUi(self, NEREditor):
        _translate = QtCore.QCoreApplication.translate
        NEREditor.setWindowTitle(_translate("NEREditor", "NERAnnotator 1.0"))
        self.openButton.setText(_translate("NEREditor", "open"))
        self.reMapButton.setText(_translate("NEREditor", "reMap"))
        self.newMapButton.setText(_translate("NEREditor", "newMap"))
        self.fontSetButton.setText(_translate("NEREditor", "font"))
        self.quitButton.setText(_translate("NEREditor", "quit"))
        self.useREButton.setText(_translate("NEREditor", "use RE model"))
        self.fileLabel.setText(_translate("NEREditor", "文件"))
        self.groupBox.setTitle(_translate("NEREditor", "命名实体标签"))
        self.label_8.setText(_translate("NEREditor", "标签配置文件"))
        self.configFileButton.setItemText(0, _translate("NEREditor", "default.config"))
        
    def initLabelMap(self, NEREditor, config_path='./config/default.config'):
        with open(config_path) as fin:
            config_json = json.load(fin)
            
        for idx, (shortcut, e_type) in enumerate(config_json.items()):
            # initialize label
            label = QtWidgets.QLabel(self.groupBox)
            label.setObjectName(f'{shortcut}')
            label.setText(f'{shortcut}')
            self.gridLayout.addWidget(label, idx, 0, 1, 1)

            # initialize lineedit
            lineEdit = QtWidgets.QLineEdit(self.groupBox)
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            font.setKerning(True)
            lineEdit.setFont(font)
            lineEdit.setText(f'{e_type}')
            lineEdit.setReadOnly(True)
            lineEdit.setObjectName("lineEdit")
            self.gridLayout.addWidget(lineEdit, idx, 1, 1, 1)

