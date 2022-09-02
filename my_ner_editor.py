#!/usr/bin/env python
# coding=utf-8
'''
Date         : 2022-08-27 09:55:05
LastEditors  : Chen Chengshuai
LastEditTime : 2022-09-02 17:44:57
FilePath     : /NERAnnotator/my_ner_editor.py
Description  : 
'''

import re
import sys
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
    QWidget,
    QAction,
    QTextEdit,
    QFontDialog,
    QMessageBox,
    QFileDialog,
    QMainWindow,
    QApplication,
)

from ui.ner_editor import Ui_NEREditor

'''
    # 检测键盘回车按键
    def keyPressEvent(self, event):
        print("按下：" + str(event.key()))
        # 举例
        if(event.key() == Qt.Key_Escape):
            print('测试：ESC')
        if(event.key() == Qt.Key_A):
            print('测试：A')
        if(event.key() == Qt.Key_1):
            print('测试：1')
        if(event.key() == Qt.Key_Enter):
            print('测试：Enter')
        if(event.key() == Qt.Key_Space):
            print('测试：Space')

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("鼠标左键点击")
        elif event.button() == Qt.RightButton:
            print("鼠标右键点击")
        elif event.button() == Qt.MidButton:
            print("鼠标中键点击")
'''

# 人工标注实体
TAGGEDENTITY = r'\[\@.*?\#.*?\*\](?!\#)'

# 人工标注重合实体标签
INSIDENESTENTITY= r'\[\@\[\@(?!\[\@).*?\#.*?\*\]\#'

# 系统推荐实体标签
RECOMMENDENTITY = r'\[\$.*?\#.*?\*\](?!\#)'

# 人工标注实体标签
goldAndrecomRe = r'\[\@.*?\#.*?\*\](?!\#)'



class FontHighlighter(QSyntaxHighlighter):
    
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
    
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        
        self.ui = Ui_NEREditor()
        self.ui.setupUi(self)
        
        self.backup = deque(maxlen=20)
        self.currentContent = deque(maxlen=1)
        
        self.pressCommand = {
            'a':"Artifical",
            'b':"Event",
            'c':"Fin-Concept",
            'd':"Location",
            'e':"Organization",
            'f':"Person",
            'g':"Sector",
            'h':"Other"
        }
        
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
        
        self.ui.textEdit.setFontFamily('黑体')
        self.ui.textEdit.setFontPointSize(18)
        self.ui.textEdit.setLineWidth(5)
        self.ui.textEdit.setPlaceholderText('文本标注区')

        self.ui.openButton.clicked.connect(self.onOpen)
        self.ui.reMapButton.clicked.connect(self.reMap)
        self.ui.quitButton.clicked.connect(self.quit)
        self.ui.fontSetButton.clicked.connect(self.setFont)
        self.ui.useREButton.stateChanged.connect(self.REButtonInfo)
        self.highlighter = FontHighlighter(self.ui.textEdit.document())

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
            'open file',
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

        aboveHalhContent = content[: selectedStartIndex]
        bellowHalfContent = content[selectedEndIndex: ]
        
        isTaggedEntity = self.isTaggedEntity(selectedContent)
        
        if isTaggedEntity:
            # [@债券 市场 收益率#Fin-Concept*]
            selectedContent = isTaggedEntity.strip('[@]').split('#')[0]
        
        if pressKey == 'q':
            logger.info(f'q: remove entity label.')
        else:
            if len(selectedContent) > 0:
                # 推荐模型
                if self.isRecommendButtonChecked():
                    bellowHalfContent = self.addRecommendContent(selectedContent, bellowHalfContent)
                
                selectedContent = self.replaceContent(selectedContent, pressKey)
        print(bellowHalfContent)   
        content = ''.join([
            aboveHalhContent,
            selectedContent,
            bellowHalfContent
        ])
        
        self.writeFile(self.filename, content)  
        
    def addRecommendContent(self, entity_name, bellowHalfContent):
        if (not entity_name) or (not bellowHalfContent):
            return bellowHalfContent
        
        print(entity_name)
        print(bellowHalfContent)
        for item in re.finditer(entity_name, bellowHalfContent):
            print(item.span())
        
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
        if self.ui.useREButton.isChecked():
            return True
        else:
            return False
    
    def isTaggedEntity(self, content):
        entity = re.match(TAGGEDENTITY, content.strip())

        return entity.group() if entity else None
    
    def replaceContent(self, content, replaceType):
        if replaceType in self.pressCommand:
            content = ''.join([
                '[@', 
                content, 
                '#', 
                self.pressCommand[replaceType], 
                '*]',
            ])
        else:
            logger.warning(f'Invalid command: {replaceType}!')
        
        return content
    
    def addRecommendContent(self, aboveHalfContent, followedHalfContent):
        pass
     
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
        
    def reMap(self):
        item_list = list(range(self.ui.gridLayout.count()))
        item_list.reverse()
        
        for i in item_list:
            item = self.ui.gridLayout.itemAt(i)
            self.ui.gridLayout.removeItem(item)
            if item.widget():
                item.widget().deleteLater()
        self.pressCommand = self.ui.initLabelMap(self, config_path='./config/my.config')
        
    def quit(self):
        self.close()
    
    
        
        
        
app = QApplication(sys.argv)
ner_editor = NEREditor()
ner_editor.show()
sys.exit(app.exec_())