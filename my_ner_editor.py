#!/usr/bin/env python
# coding=utf-8
'''
Date         : 2022-08-27 09:55:05
LastEditors  : Chen Chengshuai
LastEditTime : 2022-09-03 19:19:49
FilePath     : /NERAnnotator/my_ner_editor.py
Description  : 
'''

import os
import re
import sys
import json
from enum import Enum
from collections import deque

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



# # 人工标注实体
# TAGGEDENTITY = r'\[\@.*?\#.*?\*\](?!\#)'

# # 人工标注重合实体标签
# INSIDENESTENTITY= r'\[\@\[\@(?!\[\@).*?\#.*?\*\]\#'

# # 系统推荐实体标签
# RECOMMENDENTITY = r'\[\$.*?\#.*?\*\](?!\#)'

# 人工标注实体标签
goldAndrecomRe = r'\[\@.*?\#.*?\*\](?!\#)'


class TagEnum(Enum):
    TAGGEDENTITY     = r'\[\@.*?\#.*?\*\](?!\#)'
    RECOMMENDENTITY  = r'\[\$.*?\#.*?\*\](?!\#)'
    INSIDENESTENTITY = r'\[\@\[\@(?!\[\@).*?\#.*?\*\]\#'



class FontHighlighter(QSyntaxHighlighter):
    """字体高亮类
    """
    
    rules = []
    formats = dict()
    
    def __init__(self, parent=None):
        super(FontHighlighter, self).__init__(parent)
        
        self.initializeFormats()
        
        #! Qt 不支持 .*? 这种非贪婪匹配语法。
        #! 只要使用了 setMinimal(true) 之后，所有的匹配都会变成非贪婪的。
        self.taggedEntity = QRegExp(r'\[\@.*\#.*\*\](?!\#)')
        self.taggedEntity.setMinimal(True)
        self.recommendEntity = QRegExp(r'\[\$.*\#.*\*\](?!\#)')
        self.recommendEntity.setMinimal(True)
        
        FontHighlighter.rules.append((self.taggedEntity, 'taggedEntity'))
        FontHighlighter.rules.append((self.recommendEntity, 'recommendEntity'))

    @classmethod
    def initializeFormats(cls):
        baseFormat = QTextCharFormat()
        baseFormat.setFontFamily('黑体')
        baseFormat.setFontPointSize(18)
        
        for name, color in [
            ['taggedEntity', QColor(255, 106, 106)],
            ['recommendEntity', QColor(60, 179, 113)]
        ]:
            format = QTextCharFormat(baseFormat)
            format.setFontWeight(QFont.Bold)
            format.setBackground(color)            # 设置背景色
            # format.setForeground(QColor(color))  # 设置字体色
            format.setFontWeight(QFont.Bold)
            format.setFontItalic(True)
            cls.formats[name] = format
    
    def highlightBlock(self, text: str) -> None:
        for regex, format in FontHighlighter.rules:
            i = regex.indexIn(text)
            while i >= 0:
                length = regex.matchedLength()
                self.setFormat(
                    i,
                    length,
                    FontHighlighter.formats[format]
                )
                i = regex.indexIn(text, i + length)
                
    

class NEREditor(QWidget):
    
    configRootDir = './config'
    
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        
        self.ui = Ui_NEREditor()
        self.ui.setupUi(self)
        
        self.backup = deque(maxlen=20)
        self.currentContent = deque(maxlen=1)
        
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
        
        self.contrlCommand = {
            'q': 'unTag',
            'ctrl+z': 'undo'
        }
        
        # 设置鼠标指针样式
        self.setCursor(Qt.UpArrowCursor) 
        # 设置字体
        self.ui.textEdit.setFontFamily('黑体')
        # 设置字号
        self.ui.textEdit.setFontPointSize(18)
        self.ui.textEdit.setPlaceholderText('文本标注区')
        self.ui.configFileButton.addItems(self._loadConfigFiles())
        self.ui.textEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.highlighter = FontHighlighter(self.ui.textEdit.document())
       
        self.ui.openButton.clicked.connect(self.onOpen)
        # self.ui.reMapButton.clicked.connect(self.reMap)
        self.ui.quitButton.clicked.connect(self.quit)
        self.ui.fontSetButton.clicked.connect(self.setFont)
        self.ui.configFileButton.activated.connect(self._initConfig)
        self.ui.useREButton.stateChanged.connect(self.REButtonInfo)
        
        self._initConfig()
    
    def _initConfig(self):
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
        return os.listdir(self.configRootDir)

    def _checkConfig(self):
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
        item_list = list(range(self.ui.gridLayout.count()))
        item_list.reverse()
        
        for i in item_list:
            item = self.ui.gridLayout.itemAt(i)
            self.ui.gridLayout.removeItem(item)
            if item.widget():
                item.widget().deleteLater()
                
    def _initGridLayout(self):
        for idx, (shortcut, e_type) in enumerate(self.pressCommand.items()):
            # initialize label
            label = QLabel(self.ui.groupBox)
            label.setObjectName(f'{shortcut}')
            label.setText(f'{shortcut}')
            self.ui.gridLayout.addWidget(label, idx, 0, 1, 1)

            # initialize lineedit
            lineEdit = QLineEdit(self.ui.groupBox)
            font = QFont()
            font.setBold(True)
            font.setWeight(75)
            font.setKerning(True)
            lineEdit.setFont(font)
            lineEdit.setText(f'{e_type}')
            lineEdit.setReadOnly(True)
            lineEdit.setObjectName("lineEdit")
            self.ui.gridLayout.addWidget(lineEdit, idx, 1, 1, 1)

    def _checkSelectedContent(self, selectedContent):
        """不允许待标注文本内包含已标注实体

        Args:
            selectedContent (_type_): _description_
        """
        pass  

    def clearText(self):
        logger.debug(f'Clear text edit.')

        self.ui.textEdit.clear()
        
    def setFont(self):
        logger.debug(f'Action Track: set font.')

        font, ok = QFontDialog.getFont()
        if ok:
            self.ui.textEdit.setFont(font)

    def onOpen(self):
        logger.debug(f'Action Track: open file.')
        
        # 生成文件对话框对象
        fileDialog = QFileDialog()

        filename, filetype = fileDialog.getOpenFileName(
            self,
            'Open file',
            './demotext',
            'All Files (*.txt *.ann)'
        )

        self.autoLoadNewFile(filename)
        
    def readFile(self, filename):
        self.filename = filename

        with open(filename) as fin:
            return fin.read()
        
    def writeFile(self, filename, content):
        logger.debug(f'Action Tracked: writeFile.')
        
        assert len(filename) > 0, f'Cannot write to empty file!'
        
        filename = filename if filename.endswith('.ann') \
                        else filename+'.ann'
        
        with open(filename, 'w') as fout:
            fout.write(content)
            
        self.autoLoadNewFile(filename)  
    
    def autoLoadNewFile(self, filename):
        logger.debug(f'Action Track: autoLoadNewFile.')
        
        if filename:
            content = self.readFile(filename)
            self.ui.fileLabel.setText(f'File: {filename}')
            self.ui.textEdit.setText(content)

    def keyPressEvent(self, event):
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
            self.processContentForSelected(
                pressKey,
                content,
                selectedContent,
                selectedStartIndex,
                selectedEndIndex
            )
        else:
            self.processContentFotNotSelected(
                pressKey,
                content,
            )

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
            
        self.writeFile(self.filename, content)
    
    def processContentFotNotSelected(
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
                
            self.writeFile(self.filename, content)    
  
    def confirmTaggedEntity(self):
        pass
    
    def cancelTaggedEntity(self):
        pass
        
    def addRecommendContent(self, entity_name, pressKey, bellowHalfContent):
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
        REButtonInfo = QMessageBox.information(
            self,
            '提示',
            f'Recommend Model {"On" if self.isRecommendButtonChecked() else "Off"}',
            QMessageBox.Ok,
            QMessageBox.Ok
        )
        
        return REButtonInfo
    
    def isRecommendButtonChecked(self):
        return True if self.ui.useREButton.isChecked() else False
    
    def isTaggedEntity(self, content):
        entity = re.match(
            '|'.join([TagEnum.TAGGEDENTITY.value, TagEnum.RECOMMENDENTITY.value]), 
            content.strip()
        )

        return (True, entity.group()) if entity else (False, None)
    
    def replaceContent(self, content, pressKey, entityType=''):
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
    
    def clearCommand(self):
        pass
        
    def pushToBackup(self):
        logger.debug(f'Action Track: pushToBackup.')
        
        content = self.getContent()
        cursorPosition = self.getCursorIndex()
        
        self.backup.append([content, cursorPosition])
        
    def getContent(self):
        return self.ui.textEdit.toPlainText()
        
    def getCursorIndex(self):
        return self.ui.textEdit.textCursor().position()
    
    def getSelectedContent(self):
        return self.ui.textEdit.textCursor().selectedText()
    
    def getSelectedContentCursorIndex(self):
        return (
            self.ui.textEdit.textCursor().selectionStart(),
            self.ui.textEdit.textCursor().selectionEnd()
        )

    def quit(self):
        self.close()
 
        
        
        
app = QApplication(sys.argv)
ner_editor = NEREditor()
ner_editor.show()
sys.exit(app.exec_())