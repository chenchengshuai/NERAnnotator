# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/mac/work/NERAnnotator/ui/ner_editor.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NEREditor(object):
    def setupUi(self, NEREditor):
        NEREditor.setObjectName("NEREditor")
        NEREditor.resize(910, 795)
        self.gridLayout_7 = QtWidgets.QGridLayout(NEREditor)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.splitter = QtWidgets.QSplitter(NEREditor)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.widget = QtWidgets.QWidget(self.splitter)
        self.widget.setObjectName("widget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.openButton = QtWidgets.QPushButton(self.widget)
        self.openButton.setObjectName("openButton")
        self.gridLayout.addWidget(self.openButton, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.fontSetButton = QtWidgets.QPushButton(self.widget)
        self.fontSetButton.setObjectName("fontSetButton")
        self.gridLayout.addWidget(self.fontSetButton, 0, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 3, 1, 1)
        self.exportButton = QtWidgets.QPushButton(self.widget)
        self.exportButton.setObjectName("exportButton")
        self.gridLayout.addWidget(self.exportButton, 0, 4, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 5, 1, 1)
        self.quitButton = QtWidgets.QPushButton(self.widget)
        self.quitButton.setObjectName("quitButton")
        self.gridLayout.addWidget(self.quitButton, 0, 6, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.widget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_3.addWidget(self.line, 1, 0, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setAutoFillBackground(False)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout_3.addWidget(self.textEdit, 2, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.progressButton = QtWidgets.QLabel(self.widget)
        self.progressButton.setObjectName("progressButton")
        self.gridLayout_2.addWidget(self.progressButton, 0, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(400, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 0, 1, 1, 1)
        self.lastFileButton = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lastFileButton.sizePolicy().hasHeightForWidth())
        self.lastFileButton.setSizePolicy(sizePolicy)
        self.lastFileButton.setObjectName("lastFileButton")
        self.gridLayout_2.addWidget(self.lastFileButton, 0, 2, 1, 1)
        self.fileLabel = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileLabel.sizePolicy().hasHeightForWidth())
        self.fileLabel.setSizePolicy(sizePolicy)
        self.fileLabel.setObjectName("fileLabel")
        self.gridLayout_2.addWidget(self.fileLabel, 1, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(400, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem4, 1, 1, 1, 1)
        self.nextFileButton = QtWidgets.QPushButton(self.widget)
        self.nextFileButton.setObjectName("nextFileButton")
        self.gridLayout_2.addWidget(self.nextFileButton, 1, 2, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 3, 0, 1, 1)
        self.widget1 = QtWidgets.QWidget(self.splitter)
        self.widget1.setObjectName("widget1")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.widget1)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.labelGroupBox = QtWidgets.QGroupBox(self.widget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelGroupBox.sizePolicy().hasHeightForWidth())
        self.labelGroupBox.setSizePolicy(sizePolicy)
        self.labelGroupBox.setMinimumSize(QtCore.QSize(20, 0))
        self.labelGroupBox.setAutoFillBackground(True)
        self.labelGroupBox.setCheckable(False)
        self.labelGroupBox.setObjectName("labelGroupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.labelGroupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_3 = QtWidgets.QLabel(self.labelGroupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout_4.addWidget(self.label_3, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.labelGroupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)
        self.lineEdit.setFont(font)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_4.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.labelGroupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout_4.addWidget(self.label_4, 1, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.labelGroupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_4.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.labelGroupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout_4.addWidget(self.label_5, 2, 0, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.labelGroupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setReadOnly(True)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout_4.addWidget(self.lineEdit_3, 2, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.labelGroupBox)
        self.label_6.setObjectName("label_6")
        self.gridLayout_4.addWidget(self.label_6, 3, 0, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.labelGroupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setReadOnly(True)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout_4.addWidget(self.lineEdit_4, 3, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.labelGroupBox)
        self.label_7.setObjectName("label_7")
        self.gridLayout_4.addWidget(self.label_7, 4, 0, 1, 1)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.labelGroupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.lineEdit_5.setFont(font)
        self.lineEdit_5.setReadOnly(True)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.gridLayout_4.addWidget(self.lineEdit_5, 4, 1, 1, 1)
        self.gridLayout_6.addWidget(self.labelGroupBox, 0, 0, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.widget1)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_6.addWidget(self.line_2, 1, 0, 1, 1)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_8 = QtWidgets.QLabel(self.widget1)
        self.label_8.setObjectName("label_8")
        self.gridLayout_5.addWidget(self.label_8, 0, 0, 1, 1)
        self.useREButton = QtWidgets.QCheckBox(self.widget1)
        self.useREButton.setObjectName("useREButton")
        self.gridLayout_5.addWidget(self.useREButton, 0, 1, 1, 1)
        self.configFileButton = QtWidgets.QComboBox(self.widget1)
        self.configFileButton.setMinimumSize(QtCore.QSize(8, 0))
        self.configFileButton.setMaximumSize(QtCore.QSize(91, 16777215))
        self.configFileButton.setMouseTracking(False)
        self.configFileButton.setObjectName("configFileButton")
        self.gridLayout_5.addWidget(self.configFileButton, 1, 0, 1, 1)
        self.splitSentButton = QtWidgets.QCheckBox(self.widget1)
        self.splitSentButton.setObjectName("splitSentButton")
        self.gridLayout_5.addWidget(self.splitSentButton, 1, 1, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_5, 2, 0, 1, 1)
        self.gridLayout_6.setRowStretch(0, 8)
        self.gridLayout_6.setRowStretch(2, 1)
        self.gridLayout_7.addWidget(self.splitter, 0, 0, 1, 1)

        self.retranslateUi(NEREditor)
        QtCore.QMetaObject.connectSlotsByName(NEREditor)

    def retranslateUi(self, NEREditor):
        _translate = QtCore.QCoreApplication.translate
        NEREditor.setWindowTitle(_translate("NEREditor", "NER Annotator 1.0"))
        self.openButton.setText(_translate("NEREditor", "open"))
        self.fontSetButton.setText(_translate("NEREditor", "font"))
        self.exportButton.setText(_translate("NEREditor", "export"))
        self.quitButton.setText(_translate("NEREditor", "quit"))
        self.progressButton.setText(_translate("NEREditor", "标注进度：0/0"))
        self.lastFileButton.setText(_translate("NEREditor", "上一个"))
        self.fileLabel.setText(_translate("NEREditor", "文件位置: "))
        self.nextFileButton.setText(_translate("NEREditor", "下一个"))
        self.labelGroupBox.setTitle(_translate("NEREditor", "命名实体标签"))
        self.label_3.setText(_translate("NEREditor", "A"))
        self.lineEdit.setText(_translate("NEREditor", "ORG"))
        self.label_4.setText(_translate("NEREditor", "B"))
        self.lineEdit_2.setText(_translate("NEREditor", "PER"))
        self.label_5.setText(_translate("NEREditor", "C"))
        self.lineEdit_3.setText(_translate("NEREditor", "LOC"))
        self.label_6.setText(_translate("NEREditor", "D"))
        self.lineEdit_4.setText(_translate("NEREditor", "TITLE"))
        self.label_7.setText(_translate("NEREditor", "E"))
        self.lineEdit_5.setText(_translate("NEREditor", "INDEPENDENT"))
        self.label_8.setText(_translate("NEREditor", "标签配置文件"))
        self.useREButton.setText(_translate("NEREditor", "推荐模型"))
        self.splitSentButton.setText(_translate("NEREditor", "分句显示"))
