#!/usr/bin/env python
# coding=utf-8
'''
Date         : 2022-08-27 09:55:05
LastEditors  : Chen Chengshuai
LastEditTime : 2022-09-07 22:19:02
FilePath     : /NERAnnotator/ner_annotator.py
Description  : 
'''


import os
import re
import sys
import json
from enum import Enum
from collections import deque
from xml.sax.handler import EntityResolver

from loguru import logger
from PyQt5.QtCore import (
    Qt,
    QFile,
    QEvent, 
    QRegExp, 
    QFileInfo, 
    QIODevice,
    QTextStream,
)
from PyQt5.QtGui import (
    QFont,
    QIcon,
    QColor,
    QTextCursor,
    QKeySequence,
    QTextCharFormat,
    QSyntaxHighlighter,
)
from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QAction,
    QLineEdit,
    QTextEdit,
    QFontDialog,
    QMessageBox,
    QFileDialog,
    QMainWindow,
    QApplication,
)

from ui.ner_editor import Ui_NEREditor
from utils.font_highlighter import FontHighlighter


logger.add(
    'log/ner_annotator_{time}.log',
    rotation='50MB',
    encoding='utf-8',
    enqueue=True,
    compression='zip',
    retention='1 month'
)



class TagEnum(Enum):
    TAGGEDENTITY     = r'\[\@.*?\#.*?\*\](?!\#)'
    RECOMMENDENTITY  = r'\[\$.*?\#.*?\*\](?!\#)'


class NEREditor(QWidget):
    
    configRootDir = './config'
    
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        
        self.ui = Ui_NEREditor()
        self.ui.setupUi(self)

        self.allFileNum = 0
        self.filename = None
        self.allFilePathCache = []
        self.currentFilePathIndex = -1
        self.backup = deque(maxlen=20)

        self.pressCommand = {}
        
        # 标注快捷键
        self.allKey = {
            Qt.Key_0: 0, Qt.Key_1: 1, Qt.Key_2: 2, 
            Qt.Key_3: 3, Qt.Key_4: 4, Qt.Key_5: 5, 
            Qt.Key_6: 6, Qt.Key_7: 7, Qt.Key_8: 8, 
            Qt.Key_9: 9, Qt.Key_A: 'a', Qt.Key_B: 'b', 
            Qt.Key_C: 'c', Qt.Key_D: 'd', Qt.Key_E: 'e',
            Qt.Key_F: 'f', Qt.Key_G: 'g', Qt.Key_H: 'h', 
            Qt.Key_I: 'i', Qt.Key_J: 'j', Qt.Key_K: 'k', 
            Qt.Key_L: 'l', Qt.Key_M: 'm', Qt.Key_N: 'n', 
            Qt.Key_O: 'o', Qt.Key_P: 'p', Qt.Key_Q: 'q', 
            Qt.Key_R: 'r', Qt.Key_S: 's', Qt.Key_T: 't', 
            Qt.Key_U: 'u', Qt.Key_V: 'v', Qt.Key_W: 'w', 
            Qt.Key_X: 'x', Qt.Key_Y: 'y', Qt.Key_Z: 'z',
        }

        self.setCursor(Qt.UpArrowCursor)                                    # 指针样式
        self.ui.textEdit.setFontFamily('黑体')                               # 字体设置
        self.ui.textEdit.setFontPointSize(18)                               # 字号设置
        self.ui.textEdit.setPlaceholderText('文本标注区')                     # 标注区
        self.ui.configFileButton.addItems(self._loadConfigFiles())          # 配置文件
        self.highlighter = FontHighlighter(self.ui.textEdit.document())     # 字体高亮
        self.ui.textEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)   # 滚动条显示

        self.ui.quitButton.clicked.connect(self.quit)                       # 退出按钮
        self.ui.openButton.clicked.connect(self.onOpen)                     # 打开按钮
        self.ui.fontSetButton.clicked.connect(self.setFont)                 # 字体设置按钮
        self.ui.splitSentButton.clicked.connect(self.splitSent)             # 分句按钮
        self.ui.lastFileButton.clicked.connect(self.loadLastFile)           # 上一个文件
        self.ui.nextFileButton.clicked.connect(self.loadNextFile)           # 下一个文件
        self.ui.useREButton.stateChanged.connect(self.REButtonInfo)         # 推荐按钮
        self.ui.configFileButton.activated.connect(self._initConfig)        # 配置文件
        self.ui.exportButton.clicked.connect(self.generateSequenceFile)     # 文件导出按钮

        self._initConfig()
    
    def _initConfig(self):
        """ 初始化 """

        logger.debug(f'Action Track: _initConfig.')
        
        filename = self.ui.configFileButton.currentText()
        try:
            with open(os.path.join(self.configRootDir, filename)) as fin:
                self.pressCommand = json.load(fin)
        except json.decoder.JSONDecodeError as e:
            QMessageBox.critical(
                self,
                '配置文件格式错误',
                f'配置文件{filename}格式错误，请检查: \n{e}',
                QMessageBox.Ok,
                QMessageBox.Ok
            )
            exit()
            
        self._checkConfig()
        self._clearGridLayout()
        self._initGridLayout()
    
    def _loadConfigFiles(self):
        """ 加载标签配置文件名称 """
        
        logger.debug(f'Action Track: _loadConfigFiles.')
        
        return sorted(os.listdir(self.configRootDir))

    def _checkConfig(self):
        """ 检查配置文件 """

        logger.debug(f'Action Track: _checkConfig.')
        
        excluded_tags = {'y', 'q'}
        for shortname, _ in self.pressCommand.items():
            if shortname in excluded_tags:
                QMessageBox.critical(
                    self,
                    '快捷键设置错误',
                    f'`y`和`q`不能设置为标签快捷键！请重新配置.config文件！',
                    QMessageBox.Ok,
                    QMessageBox.Ok
                )
                exit()
  
    def _clearGridLayout(self):
        """ 清除标签映射区域 """

        logger.debug(f'Action Track: _clearGridLayout.')
        
        item_list = list(range(self.ui.gridLayout_4.count()))
        item_list.reverse()
        
        for i in item_list:
            item = self.ui.gridLayout_4.itemAt(i)
            self.ui.gridLayout_4.removeItem(item)
            if item.widget():
                item.widget().deleteLater()
                
    def _initGridLayout(self):
        """ 初始化标签映射区域 """

        logger.debug(f'Action Track: _initGridLayout.')
        
        for idx, (shortcut, e_type) in enumerate(self.pressCommand.items()):
            shortcut = shortcut.upper()
            # initialize label
            label = QLabel(self.ui.labelGroupBox)
            label.setObjectName(f'{shortcut}')
            label.setText(f'{shortcut}')
            self.ui.gridLayout_4.addWidget(label, idx, 0, 1, 1)

            # initialize lineedit
            lineEdit = QLineEdit(self.ui.labelGroupBox)
            font = QFont()
            font.setBold(True)
            font.setWeight(75)
            font.setKerning(True)
            lineEdit.setFont(font)
            lineEdit.setText(f'{e_type}')
            lineEdit.setReadOnly(True)
            lineEdit.setObjectName("lineEdit")
            self.ui.gridLayout_4.addWidget(lineEdit, idx, 1, 1, 1)

    def clearText(self):
        logger.debug(f'Clear text edit.')

        self.ui.textEdit.clear()
        
    def setFont(self):
        logger.debug(f'Action Track: setFont.')

        font, ok = QFontDialog.getFont()
        if ok:
            self.ui.textEdit.setFont(font)

    def onOpen(self):
        logger.debug(f'Action Track: onOpen.')
        
        # 生成文件对话框对象
        fileDialog = QFileDialog()

        filenames, ok = fileDialog.getOpenFileNames(
            self,
            'Open file',
            './demotext',
            'All Files (*.txt *.ann)'
        )
        
        logger.debug(f'onOpen mode: {ok}')
        if ok:
            self.allFilePathCache = list(sorted(filenames))
            self.currentFilePathIndex += 1
            self.allFileNum = len(filenames)

            self.autoLoadNewFile(self.allFilePathCache[0])
        
    def readFile(self, filename):
        logger.debug(f'Action Tracked: readFile.')
        
        self.filename = filename

        with open(filename) as fin:
            return fin.read()
        
    def writeFile(self, filename, content, scrollBarValue):
        logger.debug(f'Action Tracked: writeFile.')
        
        assert len(filename) > 0, f'Cannot write to empty file!'
        
        filename = filename if filename.endswith('.ann') \
                        else filename+'.ann'
        
        with open(filename, 'w') as fout:
            fout.write(content)
        
        # 更新文件名称  
        if not self.allFilePathCache[self.currentFilePathIndex].endswith('.ann'):
            self.allFilePathCache[self.currentFilePathIndex] += '.ann'

        self.autoLoadNewFile(filename, scrollBarValue)  
        
    def loadLastFile(self):
        logger.debug(f'Action Track: loadLastFile.')
        
        if self.currentFilePathIndex > 0:
            self.currentFilePathIndex -= 1
            self.autoLoadNewFile(self.allFilePathCache[self.currentFilePathIndex])
        elif self.currentFilePathIndex == 0:
            QMessageBox.information(
                self,
                '提示信息',
                '已经是第一个文件！',
                QMessageBox.Ok,
                QMessageBox.Ok,
            )
        else:
            QMessageBox.warning(
                self,
                '提示信息',
                '先点击open按钮加载文件！',
                QMessageBox.Ok,
                QMessageBox.Ok,
            )

    def loadNextFile(self):
        logger.debug(f'Action Track: loadNextFile.')

        if self.isContainRecommendEntity():
            QMessageBox.warning(
                self,
                '提示信息',
                '文本中包含未确认的推荐实体，请确认之后再标注下一个文件！',
                QMessageBox.Ok,
                QMessageBox.Ok,
            )
            return
        
        if self.currentFilePathIndex < self.allFileNum-1:
            self.currentFilePathIndex += 1
            self.autoLoadNewFile(self.allFilePathCache[self.currentFilePathIndex])
        else:
            QMessageBox.information(
                self,
                '提示信息',
                '已经是最后一个文件！',
                QMessageBox.Ok,
                QMessageBox.Ok,
            )

    def isContainRecommendEntity(self):
        items = list(re.finditer(TagEnum.RECOMMENDENTITY.value, self.getContent()))
        print(len(items))

        return False if len(items) == 0 else True
    
    def autoLoadNewFile(self, filename, scrollBarValue=0):
        logger.debug(f'Action Track: autoLoadNewFile.')
        
        if filename:
            content = self.readFile(filename)
            self.ui.textEdit.setText(content)
            self.ui.fileLabel.setText(f'文件位置: {filename}')
            self.ui.textEdit.verticalScrollBar().setValue(scrollBarValue)
            self.ui.progressButton.setText(f'标注进度: {self.currentFilePathIndex+1}/{self.allFileNum}')

    def splitSent(self):
        QMessageBox.information(
            self,
            '提示信息',
            '暂未实现该功能！\n如有需要，请联系https://github.com/chenchengshuai/NERAnnotator',
            QMessageBox.Ok,
            QMessageBox.Ok,
        )

    def keyPressEvent(self, event):
        logger.debug(f'Action Track: keyPressEvent.')
        
        if event.key() in self.allKey:
            self.textReturnEnter(self.allKey[event.key()])
    
    def textReturnEnter(self, pressKey):
        # https://blog.csdn.net/weixin_43717845/article/details/104159223
        pressKey = pressKey.lower()
        
        logger.debug(f'Action Track: textReturnEnter.')
        logger.debug(f'Event: {pressKey}')
        
        # 对所有内容进行备份
        self.pushToBackup()
        self.clearCommand()
        self.executeCursorCommand(pressKey)
        
        return pressKey
    
    def executeCursorCommand(self, pressKey):
        logger.debug(f'Action Track: executeCursorCommand.')
        logger.info(f'Command: {pressKey}')
        
        content = self.getContent()

        selectedContent = self.getSelectedContent()
        selectedStartIndex, selectedEndIndex = self.getSelectedContentCursorIndex()
        
        if selectedContent:
            if not self._checkSelectedContent(selectedContent):
                return 

            content = self.processContentForSelected(
                pressKey,
                content,
                selectedContent,
                selectedStartIndex,
                selectedEndIndex
            )
        else:
            content = self.processContentForNotSelected(
                pressKey,
                content,
            )
        
        # 获取滚动条位置
        scrollBarValue = self.ui.textEdit.verticalScrollBar().value()
        
        if content:
            self.writeFile(self.filename, content, scrollBarValue)

    def _checkSelectedContent(self, selectedContent):
        """不允许待标注文本内包含已标注实体

        Args:
            selectedContent (_type_): _description_
        """
        
        logger.debug(f'Action Track: _checkSelectedContent')

        if '[' in selectedContent \
            or ']' in selectedContent \
            or '\n' in selectedContent \
            or '\r' in selectedContent \
            or len(selectedContent) == 1:
            logger.warning(f'unfair selected content.')
            return None
        
        return selectedContent 
    
    def processContentForSelected(
        self, 
        pressKey, 
        content, 
        selectedContent, 
        selectedStartIndex, 
        selectedEndIndex
    ):
        """鼠标选中内容不为空
            a. 选中内容为纯文本
            b. 选中内容为人工标注过的实体
            c. 选中内容为推荐的实体

        Args:
            pressKey (_type_): _description_
            content (_type_): _description_
            selectedContent (_type_): _description_
            selectedStartIndex (_type_): _description_
            selectedEndIndex (_type_): _description_
        """
        
        logger.debug(f'Action Track: processContentForSelected.')

        aboveHalhContent = content[: selectedStartIndex]
        bellowHalfContent = content[selectedEndIndex: ]
        
        isTaggedEntity, taggedEntity = self.isTaggedEntity(selectedContent)
        
        if isTaggedEntity:
            # [@债券 市场 收益率#Fin-Concept*] or [$债券 市场 收益率#Fin-Concept*]
            selectedContent = taggedEntity.strip('[@$]').split('#')[0]
        
        if pressKey in self.pressCommand:
            # 推荐模型, 仅当选中内容为纯文本时进行推荐
            if self.isRecommendButtonChecked() and (not isTaggedEntity):
                bellowHalfContent = self.addRecommendContent(
                    selectedContent, 
                    pressKey, 
                    bellowHalfContent
                )
            selectedContent = self.replaceContent(selectedContent, pressKey)
        else:
            return

        content = ''.join([
                aboveHalhContent,
                selectedContent,
                bellowHalfContent
            ])

        return content
    
    def processContentForNotSelected(
        self, 
        pressKey,
        content,      
    ):
        """鼠标训中内容为空
            对已标注文本（人工标注或者推荐标注）进行确认或取消操作

        Args:
            pressKey (str): 快捷键
                q: 取消操作
                y: 确认操作
                在presspressCommand中的key: 替换标签操作
            content (_type_): _description_
        """
        
        logger.debug(f'Action Track: processContentForNotSelected.')
        
        # 鼠标所在的block
        currentBlock = self.ui.textEdit.textCursor().block()
        # 当前block开头文字的索引值
        currentBlockPosition = currentBlock.position()
        # 鼠标指针在当前block中的相对索引值
        cursorPositionInBlock = self.ui.textEdit.textCursor().positionInBlock()
        
        # 当前block文本内容
        currentBlockContent = currentBlock.text()
        # 当前block之前的文本内容
        aboveHalfBlockContent = content[: currentBlockPosition]
        # 当前block之后的文本内容
        bellowHalfBlockContent = content[currentBlockPosition+len(currentBlockContent): ]
        
        matchedSpan = (-1, -1)
        detectedEntity = None
        
        for item in re.finditer(TagEnum.TAGGEDENTITY.value, currentBlockContent):
            if item.start() <= cursorPositionInBlock and item.end() >= cursorPositionInBlock:
                matchedSpan = (item.start(), item.end())
                detectedEntity = TagEnum.TAGGEDENTITY
        
        if not detectedEntity:
            for item in re.finditer(TagEnum.RECOMMENDENTITY.value, currentBlockContent):
                if item.start() <= cursorPositionInBlock and item.end() >= cursorPositionInBlock:
                    matchedSpan = (item.start(), item.end())
                    detectedEntity = TagEnum.RECOMMENDENTITY 
        
        if detectedEntity:
            aboveHalhContent = currentBlockContent[: matchedSpan[0]]
            bellowHalfContent = currentBlockContent[matchedSpan[1]: ]
            selectedContent = currentBlockContent[matchedSpan[0]: matchedSpan[1]]
            
            selectedContent, entityType = selectedContent.strip('[@$*]').split('#')
 
            if pressKey == 'y' and detectedEntity is TagEnum.RECOMMENDENTITY:
                selectedContent = self.replaceContent(selectedContent, pressKey, entityType)    
            elif pressKey == 'q':
                logger.info(f'remove entity label')
            elif pressKey in self.pressCommand:
                selectedContent = self.replaceContent(selectedContent, pressKey)  
            else:
                return
        
            currentBlockContent = ''.join([
                    aboveHalhContent,
                    selectedContent,
                    bellowHalfContent
                ])
            
            content = ''.join([
                aboveHalfBlockContent,
                currentBlockContent,
                bellowHalfBlockContent,
            ])
                
            return content 
        
    def addRecommendContent(self, entity_name, pressKey, bellowHalfContent):
        """_summary_

        Args:
            entity_name (_type_): _description_
            pressKey (_type_): _description_
            bellowHalfContent (_type_): _description_

        Returns:
            _type_: _description_
        """
        
        logger.debug(f'Action Track: addRecommendContent.')
        
        if (not entity_name) or (not bellowHalfContent):
            return bellowHalfContent

        for item in sorted(re.finditer(entity_name, bellowHalfContent),
                           key=lambda x: x.span(0),
                           reverse=True):
            candidateEntity = ''.join([
                '[$',
                item.group(),
                '#',
                self.pressCommand[pressKey],
                '*]',
            ])
            bellowHalfContent = ''.join([
                bellowHalfContent[: item.start()],
                candidateEntity,
                bellowHalfContent[item.end(): ]
            ])
    
        return bellowHalfContent
        
    def REButtonInfo(self):
        """推荐模型按钮提示信息
        """

        REButtonInfo = QMessageBox.information(
            self,
            '提示',
            f'Recommend Model {"On" if self.isRecommendButtonChecked() else "Off"}',
            QMessageBox.Ok,
            QMessageBox.Ok
        )
        
        return REButtonInfo
    
    def isRecommendButtonChecked(self):
        """检测推荐模型是否开启
        """
        logger.debug(f'Action Track: isRecommendButtonChecked.')

        return True if self.ui.useREButton.isChecked() else False
    
    def isTaggedEntity(self, content):
        """检查content是否已被标注过，包括人工标注和推荐模型标注

        Args:
            content (str): 待检测字符串

        Returns:
            tuple: (是否被标注过, 标注结果)
        """
        logger.debug(f'Action Track: isTaggedEntity.')
        
        entity = re.match(
            '|'.join([TagEnum.TAGGEDENTITY.value, TagEnum.RECOMMENDENTITY.value]), 
            content.strip()
        )

        return (True, entity.group()) if entity else (False, None)
    
    def replaceContent(self, content, pressKey, entityType=''):
        """生成标注格式

        Args:
            content (str): 实体
            pressKey (str): 实体类型对应的键值
            entityType (str, optional): 实体类型. Defaults to ''.

        Returns:
            _type_: _description_
        """
        logger.debug(f'Action Track: replaceContent.')
        
        try:
            content = ''.join([
                '[@', 
                content, 
                '#', 
                self.pressCommand.get(pressKey, entityType), 
                '*]',
            ])
        except:
            logger.warning(f'Invalid command: {pressKey}!')
        
        return content
    
    def generateSequenceFile(self):
        if not self.filename:
            QMessageBox.warning(
                self,
                '提示信息',
                '先点击open按钮加载文件！',
                QMessageBox.Ok,
                QMessageBox.Ok,
            )
            return -1

        if ('.ann' not in self.filename) and ('.txt' not in self.filename):
            QMessageBox.warning(
                self,
                '提示信息',
                'Export only works on filename ended in .ann or .txt!\nPlease rename file.',
                QMessageBox.Ok,
                QMessageBox.Ok,
            )
            return -1
        
        statusCode, message = self.writeSequenceToFile()

        if statusCode == 0:
            QMessageBox.information(
                self,
                '提示信息',
                f'Exported file successfully!\nSaved to File: {message}',
                QMessageBox.Ok,
                QMessageBox.Ok,
            )
        else:
            QMessageBox.warning(
                self,
                '提示信息',
                f'{message}',
                QMessageBox.Ok,
                QMessageBox.Ok,
            )

    def writeSequenceToFile(self):
        try:
            newFilename = self.filename + 's'

            with open(self.filename) as fin, \
                open(newFilename, 'w') as fout:
                for line in fin:
                    line = line.strip()
                    
                    startIdx = 0
                    tagList = []
                    contentList = []
                    entityItems = list(re.finditer(TagEnum.TAGGEDENTITY.value, line))

                    for item in entityItems:
                        tagList.extend(['O'] * len(line[startIdx: item.start()]))
                        contentList.extend(list(line[startIdx: item.start()]))
                        
                        entityName, entityType = item.group().strip('[@*]').split('#')
                        contentList.extend(list(entityName))
                        tagList.extend([f'B-{entityType}'] + [f'I-{entityType}'] * len(entityName[1:]))

                        startIdx = item.end()
                    
                    tagList.extend(['O'] * len(line[startIdx: ]))
                    contentList.extend(list(line[startIdx: ]))

                    for token, tag in zip(contentList, tagList):
                        fout.write(' '.join([token, tag]) + '\n')
                    fout.write('\n')

            return 0, newFilename
        except Exception as e:
            return -1, e

    def clearCommand(self):
        pass
        
    def pushToBackup(self):
        """备份
        """
        logger.debug(f'Action Track: pushToBackup.')
        
        content = self.getContent()
        cursorPosition = self.getCursorIndex()
        
        self.backup.append([content, cursorPosition])
        
    def getContent(self):
        """获取编辑框文本
        """
        
        return self.ui.textEdit.toPlainText()
        
    def getCursorIndex(self):
        """获取鼠标位置
        """
        logger.debug(f'Action Track: getCursorIndex.')
        
        return self.ui.textEdit.textCursor().position()
    
    def getSelectedContent(self):
        """获取鼠标选择的文本
        """
        logger.debug(f'Action Track: getSelectedContent.')
        
        return self.ui.textEdit.textCursor().selectedText()
    
    def getSelectedContentCursorIndex(self):
        """获取选择文本的起止位置 
        """
        logger.debug(f'Action Track: getSelectedContentCursorIndex.')
        
        return (
            self.ui.textEdit.textCursor().selectionStart(),
            self.ui.textEdit.textCursor().selectionEnd()
        )

    def quit(self):
        logger.debug(f'Action Track: quit.')
        
        self.close()
 
        
        
        
app = QApplication(sys.argv)
# app.setStyle('Windows')
ner_editor = NEREditor()
ner_editor.show()
sys.exit(app.exec_())